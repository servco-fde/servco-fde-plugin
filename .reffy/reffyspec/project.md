# Project Context

## Purpose

Build a reusable agent helper for Servco Forward Deployed Engineers (FDEs), including colleagues without a full-stack engineering background. Package practical onboarding, application development, delivery, and support workflows using the Agent Skills and Agent Plugins standards.

The initial delivery platform is Databricks Apps, with Azure DevOps for CI/CD. Microsoft Graph is a future integration: the current skill supports planning, not a configured connector. Success means FDEs can turn an internal workflow into a reviewable, validated application and understand how to deploy and support it.

This repository currently contains a plugin scaffold, not an application or deployed infrastructure.

## Tech Stack

- Agent Plugins 1.0.0: root `plugin.json`, immediate skill directories under `skills/`, and optional root `mcp.json`.
- Agent Skills: YAML frontmatter and Markdown instructions in each `SKILL.md`, with optional `references/` and `assets/` resources.
- Python 3.11+ for local structural validation, using PyYAML and jsonschema from `requirements-dev.txt`.
- Bundled JSON Schema files under `schemas/` for offline manifest validation.
- Azure Pipelines YAML for validation of this plugin repository.
- Reffy / ReffySpec for repository-local ideation, specifications, and change planning. Initialized with Reffy 1.9.5.
- Databricks Apps and Azure DevOps are target workflow platforms. Application frameworks, runtime versions, and deployment identities are chosen in each application repository; this plugin does not prescribe one universal stack.

## Project Conventions

### Code Style

- Use plain language, concrete actions, and short skill entrypoints suitable for non-technical FDEs.
- Name skills and directories in lowercase kebab-case; frontmatter `name` must match its directory. Descriptions explain both capability and activation context.
- Keep conditional detail in `references/` and reusable output templates in `assets/`; use relative Markdown links.
- Keep skill resources inside their owning skill so individual skill installation remains possible.
- Use valid JSON for portable manifests and schemas, YAML for pipeline configuration and skill frontmatter, and readable Python for deterministic validation.
- Do not add speculative scaffolding, duplicated vendor manuals, credentials, or tenant data.
- Follow root `AGENTS.md` and `CONTRIBUTING.md` for contributor guidance. No formatter or linter configuration has been established.

### Architecture Patterns

- The repository root is the portable plugin root; root `plugin.json` is authoritative. Portable component discovery uses fixed locations rather than custom manifest fields.
- Five starter skills cover onboarding, Databricks Apps, Azure DevOps CI/CD, app support, and Microsoft Graph integration planning.
- Skills are instructional workflows with self-contained resources. Installed official product skills may provide specialized guidance; they are not bundled or automatically installed dependencies.
- `mcp.json` currently contains an empty `mcpServers` object. Register integrations only after choosing an actual provider and authentication method.
- Application code and application deployment pipelines belong in the selected application repository. Root `azure-pipelines.yml` validates this plugin package.
- Record team-specific rollout decisions in `docs/team-configuration.md`; do not invent workspace, organization, tenant, identity, or access settings.
- Keep Reffy artifacts in `.reffy/artifacts/`, canonical requirements in `.reffy/reffyspec/specs/`, and proposed deltas in `.reffy/reffyspec/changes/`. Use the generated Reffy instructions for their lifecycle.

### Testing Strategy

- Install `requirements-dev.txt` and run `python3 scripts/validate.py` after package changes. It checks manifests against bundled schemas, skill metadata and discovery placement, ordinary inline local Markdown links, and package path containment.
- Root Azure Pipelines runs the same validation using Python 3.11. Azure Repos PR enforcement requires a configured build-validation branch policy.
- For changed skills, walk through realistic FDE requests to assess routing, missing inputs, useful outcomes, and authorization boundaries. Structural validation does not prove agent behavior or client compatibility.
- Verify executable helpers with meaningful valid and invalid inputs. Initial validator checks confirmed rejection of nonstandard manifest fields, mismatched skill names, missing references, escaping symlinks, and invalid MCP command paths.
- Before team rollout, test installation in the selected client and onboarding from a clean environment. These runtime/client checks have not yet been completed.
- For Reffy artifact or planning changes, use the corresponding Reffy skill and validation command. Do not create live cloud resources merely to test this scaffold.

### Git Workflow

- No Git repository, remote, primary branch, branching policy, or commit convention was configured when this scaffold was initialized. Do not assume any of these choices.
- Keep contributions focused on one workflow or capability. Update documentation and validate affected files before preparing a release.
- Use ReffySpec proposals for new capabilities, breaking changes, or architectural shifts. Inspect current specs and active changes first; preserve archived changes as an append-only history.
- Increment the plugin version when preparing a release. Publication, remote configuration, and external pipeline changes require scope established by the user or existing project instructions.

## Domain Context

FDEs translate internal business processes into applications and need help across discovery, implementation, delivery, and support. The helper should reduce setup friction while making necessary decisions understandable. Produce concrete, reviewable work and reuse explicit session choices rather than repeatedly requesting confirmation.

Databricks Apps is the first application hosting target. Distinguish analytical reads from operational persistence and resolve actual data access needs before adding a database or other resources. Azure DevOps supplies application CI/CD workflows, but no organization or project is configured here.

Microsoft Graph requires its own identity, permission, and consent decisions; Databricks access does not imply Graph access. Future platform integrations should follow the same focused-skill and verified-provider approach.

## Important Constraints

- Conform to the published Agent Skills and Agent Plugins formats; keep client-specific behavior in documented extensions rather than nonstandard core manifest fields.
- Never auto-select a Databricks profile. Present available profiles/workspace URLs when a choice is needed, preserve explicit session selections, and pass `--profile` on workspace commands.
- Do not hardcode personal profiles, workspace IDs, tenant IDs, service connections, credentials, or resource permissions into distributed workflows.
- Keep secrets in approved storage and out of source control, generated evidence, and browser code.
- Consult current official product documentation or available official skills before relying on platform commands and APIs.
- Do not infer authorization to create infrastructure, publish packages, send messages, grant permissions, or connect remote workspaces from installation of this plugin.
- Report local checks, platform runs, and deployed verification accurately; a schema-valid package is not necessarily a working application or supported client installation.
- Supported clients, license/distribution terms, maintainers, environment mapping, access processes, and production release policies remain unresolved in `docs/team-configuration.md`.

## External Dependencies

- Agent Skills specification: https://agentskills.io/specification
- Agent Plugins specification and versioned schemas: https://agent-plugins.org/specification
- A user-selected agent client supporting plugins or individual skills; compatibility must be verified before rollout.
- Python packages PyYAML and jsonschema for local/CI validation. Manifest schema validation itself uses bundled files without network retrieval.
- Databricks CLI, authenticated user-selected workspaces, and applicable platform resources when an application workflow actually requires access. No workspace is connected by this scaffold.
- Azure DevOps organization, project, repository, pipeline agents, identities, and branch policies for CI/CD rollout; these remain unconfigured.
- Microsoft Entra application identity and Microsoft Graph endpoint permissions for future integrations; no provider or connector is registered.
- Locally installed Reffy CLI for SDD workflows. No remote Reffy/Paseo workspace is configured.
