#!/usr/bin/env python3
"""Validate this starter package locally without retrieving remote schemas."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError


ROOT = Path(__file__).resolve().parents[1]
FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def contained(path):
    if not path.resolve().is_relative_to(ROOT):
        raise ValueError(f"Package path escapes plugin root: {path}")
    return path


def manifest(filename, schema_name):
    data = json.loads(contained(ROOT / filename).read_text())
    schema = json.loads(contained(ROOT / "schemas" / schema_name).read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(data)
    return data


def marketplace(plugin):
    """Check this repository's local catalog subset, not every Codex source type."""
    catalog_path = contained(ROOT / ".agents/plugins/marketplace.json")
    catalog = json.loads(catalog_path.read_text())

    def require(condition, message):
        if not condition:
            raise ValueError(f"Marketplace: {message}")

    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    require(isinstance(catalog, dict), "expected an object")
    require(isinstance(catalog.get("name"), str) and re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", catalog["name"]), "invalid name")
    interface = catalog.get("interface")
    require(isinstance(interface, dict) and nonempty(interface.get("displayName")),
            "interface.displayName is required")
    entries = catalog.get("plugins")
    require(isinstance(entries, list) and bool(entries), "plugins must be a nonempty list")
    names = set()
    roots = set()
    for entry in entries:
        require(isinstance(entry, dict), "plugin entry must be an object")
        name = entry.get("name")
        require(nonempty(name), "plugin name is required")
        require(name not in names, f"duplicate plugin name: {name}")
        names.add(name)
        source = entry.get("source")
        require(isinstance(source, dict) and source.get("source") == "local",
                f"{name}: this catalog requires a local source object")
        relative = source.get("path")
        require(isinstance(relative, str) and relative.startswith("./")
                and "\\" not in relative and ".." not in Path(relative).parts,
                f"{name}: source.path must start with ./ and stay inside the package")
        package = contained(ROOT / relative).resolve()
        require(package.is_dir(), f"{name}: source directory does not exist")
        require(package not in roots, f"{name}: duplicate plugin source")
        roots.add(package)
        package_manifest = contained(package / "plugin.json")
        require(package_manifest.is_file(), f"{name}: source has no plugin.json")
        target = json.loads(package_manifest.read_text())
        require(isinstance(target, dict) and target.get("name") == name,
                f"{name}: catalog name does not match source manifest")
        require(package == ROOT.resolve() and name == plugin["name"],
                f"{name}: this catalog must point to the repository-root plugin")
        policy = entry.get("policy")
        require(isinstance(policy, dict), f"{name}: policy is required")
        require(policy.get("installation") in (
            "AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"),
            f"{name}: invalid policy.installation")
        require(policy.get("authentication") in ("ON_INSTALL", "ON_USE"),
                f"{name}: invalid policy.authentication")
        require(nonempty(entry.get("category")), f"{name}: category is required")
    require(plugin["name"] in names, "root plugin entry is required")


def skill(path):
    text = contained(path).read_text()
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")
    data = yaml.safe_load(match[1])
    if not isinstance(data, dict) or set(data) - FIELDS:
        raise ValueError(f"{path}: invalid frontmatter fields")
    name = data.get("name")
    if (not isinstance(name, str) or len(name) > 64
            or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
            or name != path.parent.name):
        raise ValueError(f"{path}: invalid name or directory mismatch")
    for field, limit in (("description", 1024), ("compatibility", 500)):
        if field == "description" or field in data:
            value = data.get(field)
            if not isinstance(value, str) or not value.strip() or len(value) > limit:
                raise ValueError(f"{path}: invalid {field}")
    for field in ("license", "allowed-tools"):
        if field in data and not isinstance(data[field], str):
            raise ValueError(f"{path}: {field} must be a string")
    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict) or any(
        not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items()
    ):
        raise ValueError(f"{path}: metadata must map strings to strings")
    if not text[match.end():].strip():
        raise ValueError(f"{path}: missing instructions")


def markdown_links(path):
    # Check ordinary inline local links used by this package, not all Markdown syntax.
    for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", path.read_text()):
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        linked = contained(path.parent / unquote(parsed.path))
        if not linked.exists():
            raise ValueError(f"{path}: missing linked resource {target}")


def mcp_paths(config):
    for name, server in config["mcpServers"].items():
        if server["type"] != "stdio":
            continue
        command = server["command"]
        if command.startswith("./"):
            if not contained(ROOT / command).is_file():
                raise ValueError(f"MCP server {name}: missing executable {command}")
        elif "/" in command or "\\" in command or re.search(r"\s", command):
            raise ValueError(f"MCP server {name}: invalid executable token")
        cwd = server.get("cwd")
        if cwd is None:
            continue
        if cwd.startswith("./"):
            contained(ROOT / cwd)
        elif cwd == "${PLUGIN_ROOT}" or cwd.startswith("${PLUGIN_ROOT}/"):
            contained(ROOT / cwd.removeprefix("${PLUGIN_ROOT}").lstrip("/"))
        elif cwd == "${PLUGIN_DATA}" or cwd.startswith("${PLUGIN_DATA}/"):
            # The actual client-managed data directory is unavailable during package validation.
            relative = Path(cwd.removeprefix("${PLUGIN_DATA}").lstrip("/"))
            if ".." in relative.parts or "\\" in cwd:
                raise ValueError(f"MCP server {name}: unsafe data-directory path")
        else:
            raise ValueError(f"MCP server {name}: invalid working directory")


def main():
    plugin = manifest("plugin.json", "plugin.schema.json")
    marketplace(plugin)
    mcp_path = ROOT / "mcp.json"
    if mcp_path.exists():
        config = manifest("mcp.json", "mcp.schema.json")
        mcp_paths(config)
    skills = contained(ROOT / "skills")
    found = []
    if skills.exists():
        if not skills.is_dir():
            raise ValueError("skills must be a directory")
        for directory in sorted(skills.iterdir()):
            contained(directory)
            entry = directory / "SKILL.md"
            if directory.is_dir() and entry.exists():
                skill(entry)
                found.append(entry)
        discovered = {path.resolve() for path in found}
        for path in skills.rglob("SKILL.md"):
            if path.resolve() not in discovered:
                raise ValueError(f"Skill outside immediate discovery location: {path}")
    documents = list(ROOT.glob("*.md"))
    for folder in ("skills", "docs", "scripts", "schemas"):
        base = contained(ROOT / folder)
        if base.exists():
            for path in base.rglob("*"):
                contained(path)
                if path.is_file() and path.suffix == ".md":
                    documents.append(path)
    for path in documents:
        markdown_links(contained(path))
    print(f"Validated plugin manifest, marketplace, MCP scaffold, {len(found)} skills, and local Markdown links.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, yaml.YAMLError, ValidationError, SchemaError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
