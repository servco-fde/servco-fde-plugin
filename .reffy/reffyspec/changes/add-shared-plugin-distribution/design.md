## Context
The repository already has a portable root manifest, five self-contained skills, bundled schemas, and a structural validator. README installation instructions defer all client-specific details. There are no canonical specs or active changes to modify.

The upstream handoff uses `servco-fde-skills` as the shared package label. The actual manifest name is `servco-fde-plugin`; Reffy's project identifier does not require a package rename.

## Goals / Non-Goals
Goals: make installation repeatable, retain portable packaging, keep shared and app-specific workflows understandable, and establish evidence for compatibility and lifecycle operations.

Non-goals: building application workflows or infrastructure, configuring identities or credentials, automatic cross-client support, and public marketplace submission.

## Decisions
### Keep one portable package with a separate catalog

Add `.agents/plugins/marketplace.json` as the Codex distribution extension and point its entry to the existing repository-root package. Use the official catalog format and path resolution rules verified during implementation. The catalog does not replace root `plugin.json`. Do not add client-specific keys to the portable manifest. If the selected client requires compatibility files, keep them in documented client extensions and validate identity/version consistency.

Use the repository root as the source so the catalog can be authored without inventing a remote URL. GitHub-backed onboarding uses the actual URL supplied by the user or team. Do not rename the plugin or hardcode the Reffy project ID as its installation identity.

### Verify Codex first and describe client limits explicitly

Codex is the initial implementation and verification target because the handoff identifies a Codex marketplace path. Select and record the specific client surface and version during implementation. Keep Claude Code and Cursor unverified unless their own documented flows are exercised. Avoid a custom installer that edits client files or copies shared workflows into application repositories.

Official documentation rechecked on 2026-10-22 describes Git-backed marketplaces and a catalog separate from the portable manifest. Client surfaces and supported operations can differ:

- [OpenAI plugin packaging and marketplace documentation](https://developers.openai.com/plugins/build/plugins)
- [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference)

### Separate shared installation from app-local skills

The full plugin should be available across repositories through the client's supported user installation scope. An app owns its specific workflows under `.agents/skills/<skill-name>/SKILL.md`. Documentation must explain distinct names and show a shared workflow plus a complementary app-local workflow, without assuming name-based override behavior.

Retain individual-skill installation for clients that support skills only. Explain that this does not install the complete plugin or bundled integrations. Preserve each skill's resources within its own directory.

### Document lifecycle and access using actual client capabilities

`docs/distribution.md` will contain installation prompts, prerequisites, client/version evidence, update, pinning, rollback, removal, and troubleshooting. Distinguish catalog refresh from plugin update or activation; do not assume refreshing a marketplace updates installed workflows. Record the Git ref and plugin version used for reproducibility, and prove that rollback restores the prior workflow content. Where a requested lifecycle operation is unavailable, state the limitation and a tested supported alternative.

Use existing user repository access for private sources. Explain access failures without capturing tokens in documentation, prompts, or logs. Keep unknown URLs, ownership, distribution terms, and access processes explicit in team configuration. Installation does not authorize changes to an application's infrastructure or permissions.

### Validate structure locally and behavior in the client

Extend `scripts/validate.py` to check required catalog fields, unique plugin identity, source resolution and package containment for this repository, and consistency with the root manifest. Reuse existing validation and pin/bundle any schema needed for offline checks. Use temporary fixture cases for meaningful catalog failures without retaining duplicate plugin trees.

Record manual verification in `docs/distribution.md`, including client/version, source ref, steps, outcome, and limitations. Test a clean installation, discovery and invocation from two scratch repositories, a complementary app-local skill, individual-skill resource access, and lifecycle operations. A private-source check requires a real accessible private source; report unavailable access as unverified. Static validation alone cannot establish client support.

## Risks and Mitigations

- Catalog and client support may evolve: cite official guidance, record tested versions, and recheck at implementation time.
- Cached installs may hide stale workflows: inspect installed content during update and rollback checks and document required reloads.
- GitHub location and access are unresolved: use explicit inputs and avoid claiming end-to-end verification before they are available.
- Duplicate names can cause ambiguous routing: demonstrate distinct shared/app-local names and avoid override promises.

## Reffy Inputs
- shared-fde-plugin-distribution.md

## Open Questions
- The configured Git remote supplies `https://github.com/servco-fde/servco-fde-plugin.git`; what distribution/access policy will the team use, and which published ref should receive rollout verification?
- Initial verification used installed Codex CLI 0.163.0. Desktop/IDE and other client surfaces remain unverified.
- Who maintains releases and owns the team access/support process?

These choices are needed for rollout evidence; they do not prevent authoring the local catalog and draft documentation with clearly identified inputs.

## Implementation Evidence

Implemented the catalog with root-relative `./`, validation, distribution guide, and CI regression checks. Native CLI installation accepted the existing portable manifest without a compatibility adapter. `docs/distribution.md` records results and reproduction commands.

Thirteen tests passed, including opt-in offline CLI checks using a temporary `CODEX_HOME`, two scratch application repositories, and a local Git fixture behind an HTTPS URL rewrite. App-server discovery confirmed all five shared skills at user scope, app-local coexistence, individual-skill template access, and removal. Lifecycle checks confirmed a pinned source stayed pinned, explicit reinstall updated content, and rollback restored earlier content.

A local-root install copied an ignored `.env` sentinel; a Git-backed install excluded it. Local previews therefore require a clean checkout. No real environment file was read or copied in these checks.

Follow-up verification published review branch `verify/shared-plugin-distribution` and tested the real GitHub source at `635e2e0935f61dac0bb0a427f1442209156e6c25`. Anonymous access, installed skill/resource content, discovery in two scratch repositories, pinned refresh, and removal passed. GitHub reports the repository as public, so private-source checks are not applicable to the current distribution.

The change remains open for an FDE's actual agent invocation. Discovery and file access are recorded separately from agent behavior. The user's installed plugins were not changed, and no release, merge, or Reffy remote sync was performed.
