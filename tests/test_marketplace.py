"""Regression checks for catalog mistakes that can hide or misdirect a plugin."""

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate", ROOT / "scripts/validate.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class MarketplaceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        self.plugin = json.loads((ROOT / "plugin.json").read_text())
        (self.root / "plugin.json").write_text(json.dumps(self.plugin))
        self.path = self.root / ".agents/plugins/marketplace.json"
        self.path.parent.mkdir(parents=True)
        self.patch = patch.object(validator, "ROOT", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def validate(self):
        self.path.write_text(json.dumps(self.catalog))
        validator.marketplace(self.plugin)

    def test_root_source_resolves_from_repository_not_catalog_directory(self):
        self.validate()

    def test_missing_catalog(self):
        with self.assertRaises(FileNotFoundError):
            validator.marketplace(self.plugin)

    def test_missing_required_metadata(self):
        cases = (((), "name"), ((), "interface"), ((), "plugins"),
                 (("plugins", 0), "name"), (("plugins", 0), "source"),
                 (("plugins", 0), "policy"), (("plugins", 0), "category"),
                 (("plugins", 0, "policy"), "installation"),
                 (("plugins", 0, "policy"), "authentication"))
        original = copy.deepcopy(self.catalog)
        for path, key in cases:
            with self.subTest(path=path, key=key):
                self.catalog = copy.deepcopy(original)
                target = self.catalog
                for part in path:
                    target = target[part]
                del target[key]
                with self.assertRaises(ValueError):
                    self.validate()

    def test_malformed_metadata_reports_value_error(self):
        original = copy.deepcopy(self.catalog)
        cases = (None, [], {"name": []}, {**original, "plugins": [None]},
                 {**original, "interface": {"displayName": " "}})
        for value in cases:
            with self.subTest(value=value):
                self.catalog = value
                with self.assertRaises(ValueError):
                    self.validate()

    def test_duplicate_identity(self):
        self.catalog["plugins"].append(copy.deepcopy(self.catalog["plugins"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate plugin name"):
            self.validate()

    def test_catalog_manifest_name_mismatch(self):
        self.catalog["plugins"][0]["name"] = "wrong-plugin"
        with self.assertRaisesRegex(ValueError, "does not match source manifest"):
            self.validate()

    def test_invalid_source_paths(self):
        for path in ("../outside", "./../outside", "/tmp", ".", "skills", "./missing",
                     "./skills\\other", None):
            with self.subTest(path=path):
                self.catalog["plugins"][0]["source"]["path"] = path
                with self.assertRaises(ValueError):
                    self.validate()

    def test_source_without_manifest(self):
        (self.root / "empty").mkdir()
        self.catalog["plugins"][0]["source"]["path"] = "./empty"
        with self.assertRaisesRegex(ValueError, "no plugin.json"):
            self.validate()

    def test_source_symlink_cannot_escape(self):
        (self.root / "escape").symlink_to(self.root.parent, target_is_directory=True)
        self.catalog["plugins"][0]["source"]["path"] = "./escape"
        with self.assertRaisesRegex(ValueError, "escapes plugin root"):
            self.validate()

    def test_manifest_symlink_cannot_escape(self):
        (self.root / "package").mkdir()
        (self.root / "package/plugin.json").symlink_to(self.root.parent / "plugin.json")
        self.catalog["plugins"][0]["source"]["path"] = "./package"
        with self.assertRaisesRegex(ValueError, "escapes plugin root"):
            self.validate()

    def test_bad_policy_or_source_kind(self):
        entry = self.catalog["plugins"][0]
        for field, value in (("policy", []), ("source", "https://example.invalid"),
                             ("category", "")):
            with self.subTest(field=field):
                original = entry[field]
                entry[field] = value
                with self.assertRaises(ValueError):
                    self.validate()
                entry[field] = original
        entry["policy"]["installation"] = "AUTOMATIC"
        with self.assertRaisesRegex(ValueError, "policy.installation"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
