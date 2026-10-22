# Contributing

Add or refine one workflow at a time. Start with a realistic FDE request, define the outcome, then write the shortest useful skill and supporting resources. Put each new skill directly under `skills/` with a matching frontmatter `name` and a specific `description`.

Run the validation command in [README.md](README.md). Exercise the skill with a realistic example in a local scratch application; document what was verified and any platform access that was unavailable. Avoid live mutations unless the task authorizes them.

For distribution changes, follow the [distribution guide](docs/distribution.md), run catalog regression tests, and opt into isolated Codex checks where available. Keep the Codex catalog separate from the portable manifest. This catalog uses local sources resolved from the repository root; the validator deliberately rejects other source types. Document new client adapters and verify them separately. Keep shared workflows in this package and app-specific skills in the owning application's `.agents/skills/` with distinct names.

For a release, increment `plugin.json`'s version, validate the package/catalog, and record the release ref and installation evidence. Check update, pinning, rollback content, and removal in the intended client. A marketplace refresh does not prove that the installed package changed. Publishing a release and changing user client configuration are separate from running the offline checks.

For a new integration, follow [integration guidance](docs/integrations.md). Record required configuration in [team configuration](docs/team-configuration.md) without credentials. Update the workflow table in README.md and increment plugin.json's version when preparing a release.

Before a team release, choose a license/distribution policy, verify installation in the team's selected clients, and have an FDE try onboarding from a clean environment. Schema validity alone is not a usability or compatibility test.
