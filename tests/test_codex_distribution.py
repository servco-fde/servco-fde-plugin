"""Opt-in, offline Codex client checks. No model calls or user config changes.

Run with SERVCO_TEST_CODEX=1 python3 -m unittest discover -s tests -v.
Git rewrites a fixture HTTPS URL to a temporary local Git repository.
"""

import json
import os
from pathlib import Path
import select
import shutil
import subprocess
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "servco-fde-plugin@servco-fde"
SOURCE = "https://distribution-fixture.invalid/plugin.git"


@unittest.skipUnless(os.environ.get("SERVCO_TEST_CODEX") == "1" and shutil.which("codex"),
                     "opt in with SERVCO_TEST_CODEX=1 and install Codex CLI")
class CodexDistributionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="servco-client-check-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.repo = self.base / "package"
        self.repo.mkdir()
        # Allowlist package inputs: never copy .env, credentials, or user config.
        for name in ("plugin.json", "mcp.json", "skills"):
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(source, self.repo / name)
            else:
                shutil.copy2(source, self.repo / name)
        catalog = self.repo / ".agents/plugins/marketplace.json"
        catalog.parent.mkdir(parents=True)
        shutil.copy2(ROOT / ".agents/plugins/marketplace.json", catalog)
        home = self.base / "codex-home"
        home.mkdir()
        self.env = os.environ.copy()
        self.env.update(CODEX_HOME=str(home), GIT_CONFIG_COUNT="1",
                        GIT_CONFIG_KEY_0=f"url.{self.repo.as_uri()}.insteadOf",
                        GIT_CONFIG_VALUE_0=SOURCE, GIT_TERMINAL_PROMPT="0")
        self.apps = [self.base / "app-a", self.base / "app-b"]
        for app in self.apps:
            app.mkdir()
            self.run_command("git", "init", "-q", str(app))
        self.run_command("git", "init", "-q", str(self.repo))
        (self.repo / ".gitignore").write_text(".env\n")
        (self.repo / ".env").write_text("DISTRIBUTION_TEST_SENTINEL=not-a-secret\n")
        self.commit("Fixture initial package")
        self.run_command("git", "-C", str(self.repo), "tag", "fixture-v1")

    def run_command(self, *args):
        result = subprocess.run(args, cwd=self.base, env=self.env,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, f"{args}: {result.stderr}")
        return result.stdout

    def codex(self, *args):
        return json.loads(self.run_command("codex", "plugin", *args, "--json"))

    def commit(self, message):
        self.run_command("git", "-C", str(self.repo), "add", ".")
        self.run_command("git", "-C", str(self.repo), "-c", "user.name=Distribution check",
                         "-c", "user.email=check@example.invalid", "-c", "commit.gpgsign=false",
                         "commit", "-qm", message)

    def skills(self):
        process = subprocess.Popen(["codex", "app-server", "--stdio"], cwd=self.apps[0],
                                   env=self.env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, text=True, bufsize=1)

        def request(number, method, params):
            process.stdin.write(json.dumps({"id": number, "method": method, "params": params}) + "\n")
            process.stdin.flush()
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                if select.select([process.stdout], [], [], 1)[0]:
                    line = process.stdout.readline()
                    self.assertTrue(line, "Codex app-server exited")
                    reply = json.loads(line)
                    if reply.get("id") == number:
                        self.assertNotIn("error", reply)
                        return reply["result"]
            self.fail(f"Timed out waiting for {method}")

        try:
            request(1, "initialize", {"clientInfo": {"name": "servco-check", "version": "1"},
                                      "capabilities": {"experimentalApi": True}})
            process.stdin.write('{"method":"initialized"}\n')
            process.stdin.flush()
            return request(2, "skills/list", {"cwds": [str(app) for app in self.apps],
                                               "forceReload": True})["data"]
        finally:
            process.terminate()
            process.wait(timeout=10)
            process.stdin.close()
            process.stdout.close()

    def test_install_discovery_lifecycle(self):
        self.codex("marketplace", "add", SOURCE, "--ref", "fixture-v1")
        installed = self.codex("add", PLUGIN)
        cache = Path(installed["installedPath"])
        self.assertFalse((cache / ".env").exists())
        original = (cache / "skills/fde-onboarding/SKILL.md").read_text()
        self.assertEqual(original, (self.repo / "skills/fde-onboarding/SKILL.md").read_text())
        self.assertTrue((cache / "skills/fde-onboarding/assets/application-brief.md").is_file())
        self.assertEqual(len(self.codex("list")["installed"]), 1)

        local = self.apps[0] / ".agents/skills/app-release-check"
        local.mkdir(parents=True)
        (local / "SKILL.md").write_text(
            "---\nname: app-release-check\ndescription: Check this app release.\n---\nRead the app checklist.\n")
        for entry in self.skills():
            self.assertFalse(entry["errors"])
            shared = [skill for skill in entry["skills"] if skill.get("pluginId") == PLUGIN]
            self.assertEqual(len(shared), 5)
            self.assertTrue(all(skill["enabled"] and skill["scope"] == "user" for skill in shared))
            self.assertEqual(any(skill["name"] == "app-release-check" for skill in entry["skills"]),
                             entry["cwd"] == str(self.apps[0]))

        # A later source revision must not move an installation pinned to v1.
        manifest = self.repo / "plugin.json"
        data = json.loads(manifest.read_text())
        data["version"] = "0.1.1"
        manifest.write_text(json.dumps(data))
        changed = self.repo / "skills/fde-onboarding/SKILL.md"
        changed.write_text(original + "\nFixture revision two.\n")
        self.commit("Fixture second revision")
        self.run_command("git", "-C", str(self.repo), "tag", "fixture-v2")
        self.codex("marketplace", "upgrade", "servco-fde")
        self.codex("add", PLUGIN)
        self.assertEqual((cache / "skills/fde-onboarding/SKILL.md").read_text(), original)

        # Explicit reinstall makes update and rollback deterministic.
        for ref, version, expected in (("fixture-v2", "0.1.1", changed.read_text()),
                                       ("fixture-v1", "0.1.0", original)):
            self.codex("remove", PLUGIN)
            self.codex("marketplace", "remove", "servco-fde")
            self.codex("marketplace", "add", SOURCE, "--ref", ref)
            installed = self.codex("add", PLUGIN)
            self.assertEqual(installed["version"], version)
            self.assertEqual((Path(installed["installedPath"]) / "skills/fde-onboarding/SKILL.md").read_text(), expected)

        self.codex("remove", PLUGIN)
        self.assertFalse(self.codex("list")["installed"])
        for entry in self.skills():
            self.assertFalse(any(skill.get("pluginId") == PLUGIN for skill in entry["skills"]))
        self.assertTrue((local / "SKILL.md").is_file())
        self.codex("marketplace", "remove", "servco-fde")

    def test_individual_skill_resources(self):
        destination = self.apps[0] / ".agents/skills/fde-onboarding"
        shutil.copytree(self.repo / "skills/fde-onboarding", destination)
        entries = self.skills()
        onboarding = [skill for skill in entries[0]["skills"] if skill["name"] == "fde-onboarding"]
        self.assertEqual(len(onboarding), 1)
        self.assertTrue((Path(onboarding[0]["path"]).parent / "assets/application-brief.md").is_file())
        self.assertFalse(any(skill["name"] == "fde-onboarding" for skill in entries[1]["skills"]))


if __name__ == "__main__":
    unittest.main()
