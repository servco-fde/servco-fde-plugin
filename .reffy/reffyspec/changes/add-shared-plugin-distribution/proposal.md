# Change: Add shared FDE plugin distribution

## Why
FDEs currently receive generic instructions to clone the repository and follow an unspecified client installation flow. There is no distribution catalog, verified client path, or documented update and recovery procedure. An FDE asking “Install our shared FDE plugin from <GitHub repository URL> for use across my projects” needs a reproducible route to the shared workflows.

## What Changes
- Add a Codex distribution catalog at `.agents/plugins/marketplace.json` pointing to the existing root plugin. Preserve `servco-fde-plugin` as the package identity.
- Document a client installation flow, starting with Codex, with copyable onboarding prompts and a separate individual-skill fallback.
- Explain shared plugin installation across application repositories and app-specific skills under each application's `.agents/skills/`, using distinct skill names.
- Document update, version pinning, rollback, removal, private-repository prerequisites, and recovery from unavailable access or unsupported clients.
- Extend local validation for the catalog and record clean-client compatibility evidence before claiming support. Keep other clients unverified until separately exercised.

## Scope
This proposal covers packaging, distribution documentation, local validation, and client verification. It does not add a Terraform or identity workflow, configure MCP providers, rename the package, choose a GitHub organization/repository, or publish/install anything as part of creating the change.

## Impact
- Affected specs: `shared-plugin-distribution`
- Affected files: new `.agents/plugins/marketplace.json` and `docs/distribution.md`; updates to `README.md`, `CONTRIBUTING.md`, `docs/team-configuration.md`, and `scripts/validate.py`; client compatibility metadata only if required by verified client behavior.
- Existing root manifest, skill layout, self-contained resources, and empty MCP configuration remain the portable package baseline.
- Implementation needs a real source URL and selected client/version for end-to-end verification. These values must come from explicit session choices or documented team configuration.

## Supersedes
None

## Reffy References
- `shared-fde-plugin-distribution.md` - local summary of the developers' handoff from workspace `servco-fde`, project `servco-fde-starter`; informs package layout, installation scopes, lifecycle guidance, and verification requirements.
