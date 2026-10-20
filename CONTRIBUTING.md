# Contributing

Add or refine one workflow at a time. Start with a realistic FDE request, define the outcome, then write the shortest useful skill and supporting resources. Put each new skill directly under `skills/` with a matching frontmatter `name` and a specific `description`.

Run the validation command in [README.md](README.md). Exercise the skill with a realistic example in a local scratch application; document what was verified and any platform access that was unavailable. Avoid live mutations unless the task authorizes them.

For a new integration, follow [integration guidance](docs/integrations.md). Record required configuration in [team configuration](docs/team-configuration.md) without credentials. Update the workflow table in README.md and increment plugin.json's version when preparing a release.

Before a team release, choose a license/distribution policy, verify installation in the team's selected clients, and have an FDE try onboarding from a clean environment. Schema validity alone is not a usability or compatibility test.
