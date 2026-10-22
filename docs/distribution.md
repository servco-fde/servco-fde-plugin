# Install and maintain the shared FDE plugin

The package is `servco-fde-plugin`; its marketplace is `servco-fde`. The catalog
at `.agents/plugins/marketplace.json` points to the root package. It is a Codex
extension; root `plugin.json` remains the portable manifest. No compatibility
manifest was needed in the tested CLI.

The configured Git remote is `https://github.com/servco-fde/servco-fde-plugin.git`.
The catalog is available on the `verify/shared-plugin-distribution` review
branch. GitHub installation was verified at commit
`635e2e0935f61dac0bb0a427f1442209156e6c25`; this is a verification revision,
not a declared release. The repository is public and anonymous read access was
verified. Distribution terms and ownership still need to be recorded in
[team configuration](team-configuration.md).

## Ask your agent to install it

Copy this prompt and replace the client and ref with your chosen values:

> Install the shared `servco-fde-plugin` from
> `https://github.com/servco-fde/servco-fde-plugin.git` for use across my projects
> in Codex CLI. Use Git ref `<release-tag-or-commit>`. Check my client version
> and existing repository access, add the `servco-fde` marketplace, install the
> plugin, and show how I can confirm the shared workflows in a new session.
> Reuse choices already provided. Ask for any missing ref or client information.

Use an existing Git credential helper or SSH setup for a private source. If Git
cannot read it, resolve access through the team's repository owner; that contact
is not configured yet. Do not paste access tokens into prompts or package files.
No Databricks or Azure configuration is required to install these workflows.

## Codex CLI installation

These commands were exercised with CLI **0.163.0**, using an offline Git fixture.
Start by checking `codex --version` and `codex plugin --help`. A client without
these commands needs an upgrade or the individual-skill path below.

Set `FDE_PLUGIN_REF` to an available release tag or full commit SHA; no release
tag is assumed here. Run from your application directory:

```sh
FDE_PLUGIN_SOURCE='https://github.com/servco-fde/servco-fde-plugin.git'
FDE_PLUGIN_REF='<release-tag-or-commit>'
codex plugin marketplace add "$FDE_PLUGIN_SOURCE" --ref "$FDE_PLUGIN_REF" --json
codex plugin add servco-fde-plugin@servco-fde --json
codex plugin list --json
```

Confirm the listed plugin is installed and enabled. Save the chosen ref, the
resolved commit SHA, plugin version, and client version in your installation
record. Prefer a full commit SHA when you need an immutable pin. This installs
the workflows at user scope; opening the package repository alone is not the
installation step.

Start a new Codex session in an application repository and invoke
`$servco-fde-plugin:fde-onboarding`, for example: “Help me outline an internal
app for tracking equipment requests.” Repeat discovery in a second repository.
The application brief template should be available from the installed skill.
The session still needs application choices; installation does not grant
platform access or authorize infrastructure changes.

For a local preview, use `codex plugin marketplace add /absolute/path/to/clean-clone`
instead of the Git source, then install using the same plugin selector. Use a
fresh, clean checkout containing only intended package files. In CLI 0.163.0,
a local root install copied an ignored `.env` sentinel into its cache during
testing. Do not point a local install at a working directory containing secrets.
The Git-backed fixture excluded its ignored `.env` file.

## Update, pin, roll back, and remove

`codex plugin marketplace upgrade servco-fde --json` refreshes the configured
Git catalog. In the fixture check, refreshing a catalog pinned to the first tag
and re-adding the plugin retained the first revision even after a second tag
existed. Refresh alone is not evidence that installed workflow content changed.

To move to a new ref, or roll back to a recorded earlier ref, use this tested
reinstall sequence. Keep `FDE_PLUGIN_SOURCE` set as above and set
`FDE_PLUGIN_REF` to the destination ref:

```sh
codex plugin remove servco-fde-plugin@servco-fde --json
codex plugin marketplace remove servco-fde --json
codex plugin marketplace add "$FDE_PLUGIN_SOURCE" --ref "$FDE_PLUGIN_REF" --json
codex plugin add servco-fde-plugin@servco-fde --json
codex plugin list --json
```

Inspect `installedPath` from the install result and compare the installed skill
and its resources to the chosen source revision. Start a new session. A package
version is not a substitute for checking the source ref and content. Maintainers
should increment `plugin.json`'s version for each release with changed content.
This sequence temporarily removes the plugin; it is intended for this catalog,
which contains just the one package.

For removal without replacement:

```sh
codex plugin remove servco-fde-plugin@servco-fde --json
codex plugin marketplace remove servco-fde --json
```

Confirm absence with `codex plugin list --json` and start a new session.
Removing the catalog and removing the installed plugin are separate operations.
App-local skills remain in their application repositories. If a command fails,
keep the last working ref and report the error; do not describe a partial
installation or rollback as successful.

## Shared workflows and app-local skills

Use the shared `fde-azure-devops` workflow for pipeline design, for example.
An app can add its own `equipment-release-check` skill at
`.agents/skills/equipment-release-check/SKILL.md` to identify its directories
and validation commands. Keep those names distinct. The scopes complement
each other; local skills are not a replacement mechanism for shared skills.
Shared workflow files do not need to be copied into each app.

### Install just one skill

For a client supporting skills only, select a ref and copy the **whole**
`skills/fde-onboarding/` directory from a clean checkout into the client's
documented skill location, preserving `assets/` and other resources.
For Codex, a user skill belongs at `~/.agents/skills/fde-onboarding/`; an
application-owned skill belongs under that app's `.agents/skills/`.
Check for an existing skill with the same name before installing. Start a new
session and invoke `$fde-onboarding` to verify discovery and template access.

An individual skill does not install the plugin, its other skills, or MCP
integrations. Record its source commit separately. Update or roll back by
replacing that entire skill directory with the selected revision after reviewing
local edits; remove only the installed directory when uninstalling it.

## Verification record

Checked **2026-10-22, Pacific/Honolulu**, on macOS with Codex CLI **0.163.0**.
The tests use a temporary `CODEX_HOME`, two scratch Git repositories, and an
allowlist of package files. No user client configuration is changed. An HTTPS
fixture URL is rewritten by Git to a temporary local repository: these are
offline transport checks, not GitHub authentication evidence.

| Check | Result |
| --- | --- |
| Root catalog and local CLI install | Passed; existing portable manifest accepted |
| Git fixture clean install | Passed; installed package matches first source revision, ignored `.env` excluded |
| Cross-repository discovery | Passed; app-server `skills/list` returns all five enabled skills at user scope in both repositories |
| App-local coexistence | Passed; `app-release-check` appears alongside shared skills in its owning app only |
| Individual-skill resources | Passed at repo scope; onboarding skill discovered and its template readable |
| Pin, update, rollback | Passed using fixture tags `fixture-v1` and `fixture-v2`; installed content and package versions checked |
| Removal | Passed; shared skills disappear, app-local skill remains |
| Onboarding prompt review | Reviewed manually: source/ref/client gaps are requested, app work stays in the app repo, platform choices remain explicit |
| Actual agent invocation and FDE onboarding | Passed in two independent fresh `codex exec` sessions against the real GitHub commit. Each read the installed skill and bundled template, then saved `application-brief.md` with all 13 template fields, local scope, and explicitly unresolved choices |
| Real GitHub installation | Passed at `635e2e0935f61dac0bb0a427f1442209156e6c25`, package 0.1.0; all ten installed skill/resource files matched source and all five skills appeared at user scope in both scratch repositories |
| Real GitHub pin refresh and removal | Passed; refresh/reinstall retained the pinned version, removal cleared installed-plugin state and shared discovery |
| Private-source success/failure | Not applicable to the current public repository; anonymous GitHub access passed with credential helpers and global/system Git configuration disabled. Repeat access checks if visibility changes |
| Desktop/IDE surfaces, Claude Code, Cursor | Unverified; do not assume the CLI result applies to these clients |

Run the checks with development dependencies installed:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
SERVCO_TEST_CODEX=1 python3 -m unittest discover -s tests -v
```

The last command opts into client checks and requires Codex CLI and Git. It
makes no model calls. CI runs the structural checks and catalog regressions;
it skips the opt-in client checks. The validator covers this repository's local
catalog format, required metadata, identity consistency, and source containment;
it does not validate every Codex catalog source type.

For future releases, record an accessible GitHub ref, repeat the clean install
and lifecycle checks against it, exercise private-access success/failure if
applicable, and repeat onboarding in two app repositories. Record
client/version, source/ref/resolved SHA, steps, expected and actual results,
required reloads, and limitations here without credentials or customer data.

### Reproduce the onboarding walkthrough

The walkthrough passed on 2026-10-22 using two independent non-interactive
Codex CLI 0.163.0 sessions, each in a separate scratch Git repository with no
shared skill copies. The source was the verified GitHub revision above. Both
sessions exited successfully and produced a usable brief from the installed
template. Session IDs were `01a165a1-fe2f-7f31-8108-d2e89f963d99` and
`01a165a2-966d-7430-840d-52c1ed1cfe5f`.

Each brief included all 13 template fields, a proposed request workflow and
observable acceptance criteria, explicitly unresolved ownership/access choices,
and a local-only next milestone. Command traces confirmed both sessions read
the cached `fde-onboarding/SKILL.md` and `assets/application-brief.md`. No
deployment or cloud operations occurred. The temporary authentication copy was
deleted after testing; user plugin configuration was not changed. These results
verify CLI agent behavior, not desktop/IDE compatibility or a human usability
study.

Install the verified revision in your regular Codex CLI environment:

```sh
codex --version
codex plugin marketplace add https://github.com/servco-fde/servco-fde-plugin.git --ref 635e2e0935f61dac0bb0a427f1442209156e6c25 --json
codex plugin add servco-fde-plugin@servco-fde --json
codex plugin list --json
```

If `servco-fde` is already configured from another source/ref, inspect
`codex plugin marketplace list --json` first and use the documented reinstall
sequence to select the verified revision; do not assume an existing entry moved.

Start a fresh Codex session in a scratch application repository and send:

> $servco-fde-plugin:fde-onboarding Help me outline an internal app for tracking
> equipment requests. Save an application brief using your bundled template.
> Keep this exercise local; do not deploy or create cloud resources.

Confirm that the skill is found, the saved brief uses the bundled template,
and questions concern real missing application choices. Repeat in a second
scratch application repository without copying the shared skills. Report your
client/version and whether each invocation produced the brief, with any error
text and output file paths. Do not include credentials or real customer data.
Use this procedure to recheck onboarding after future client or skill changes.

## Official documentation

Consulted on 2026-10-22; recheck when client support changes:

- [Plugin packaging and catalog format](https://developers.openai.com/plugins/build/plugins)
- [CLI plugin and marketplace commands](https://learn.chatgpt.com/docs/cli/reference)
- [Local skill locations](https://learn.chatgpt.com/docs/build-skills)
