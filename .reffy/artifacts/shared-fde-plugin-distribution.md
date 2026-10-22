# Shared FDE plugin distribution handoff

Source: workspace `servco-fde`, project `servco-fde-starter`, remote artifact
`.reffy/artifacts/shared-fde-plugin-distribution.md`, titled “Shared FDE plugin
structure and distribution”, recorded 2026-10-21 (Pacific/Honolulu).
Read from the shared workspace on 2026-10-21. This local note summarizes the
developers' handoff; it is not a claim that distribution is configured.

## Intended experience

An FDE asks their agent: “Install our shared FDE plugin from <GitHub repository
URL> for use across my projects.” The agent uses the client's supported flow
and existing repository access for private repositories.

## Handoff direction

- Distribute reusable workflows centrally through the shared plugin, installed
  in the agent client rather than copied into every application repository.
- Commit app-specific workflows under the app's
  `.agents/skills/<skill-name>/SKILL.md`. Shared and local skills complement
  each other; use distinct names instead of relying on overrides.
- Preserve root `plugin.json`, immediate `skills/<name>/SKILL.md` packages,
  self-contained skill resources, and optional root `mcp.json`.
- Add and validate a GitHub-backed distribution catalog, proposed at
  `.agents/plugins/marketplace.json`, separately from the portable manifest.
- Document full-plugin and individual-skill installation separately, with
  copyable prompts, updates, version pinning, rollback, and removal.
- Verify packaging and discovery in selected clients independently. Codex,
  Claude Code, and Cursor must not be assumed interchangeable.
- Exercise clean-client installation, use across repositories, coexistence
  with app-local skills, and private-repository access where applicable.
- Keep credentials and application/customer configuration outside the package.

The source calls the shared package `servco-fde-skills`; this repository's
portable manifest identifies it as `servco-fde-plugin`. The handoff does not
require renaming the plugin. Microsoft identity/Terraform is mentioned as a
future shared workflow candidate, with module ownership undecided.

## Documentation referenced by the developers

- [Plugin packaging and marketplaces](https://developers.openai.com/plugins/build/plugins)
- [Local skill discovery](https://learn.chatgpt.com/docs/build-skills)
- [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference)

Verify current client behavior when implementing; the handoff is planning
context, not installation evidence.
