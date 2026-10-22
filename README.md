# servco-fde-plugin

A starter agent plugin for Forward Deployed Engineers building and supporting internal applications. It packages reusable workflows as skills, with Databricks Apps as the initial delivery platform and Azure DevOps as the CI/CD platform. Microsoft Graph integration starts as a planning workflow.

## What is an agent plugin?

An agent plugin packages reusable capabilities into a portable directory that a compatible agent client can discover and load. The [Agent Plugins v1 specification](https://agent-plugins.org/specification) defines two component types: skills and MCP servers.

- **`plugin.json`** (required, at the root): identifies the plugin and its target specification through `$schema` and `name`, with optional metadata such as version and description.
- **`skills/<name>/SKILL.md`** (optional): gives the agent instructions for a particular workflow. Each skill sits directly under `skills/` and follows the [Agent Skills specification](https://agentskills.io/specification), with optional scripts, references, and assets alongside it.
- **`mcp.json`** (optional, at the root): configures Model Context Protocol servers that expose tools and context to the agent.

The client discovers components at these fixed locations. This plugin uses skills to share FDE workflows; its MCP configuration is currently empty.

## Start here

1. Follow the [distribution guide](docs/distribution.md) to install the full plugin from a selected source ref. It includes a copyable onboarding prompt and Codex CLI commands, plus the verification status and remaining rollout checks.
2. Start a new session in your application repository and confirm the shared skills are available. The catalog is named `servco-fde`; the plugin is `servco-fde-plugin`.
3. Ask: **“Help me get started as an FDE and build my first internal app.”** The `fde-onboarding` skill guides intake and environment setup.

If your client supports only [Agent Skills](https://agentskills.io/specification), use the guide's individual-skill installation path. Keep each skill's resources together. Application-specific workflows belong in that application's `.agents/skills/` with distinct names. Opening this repository alone does not guarantee skill discovery.

## Included workflows

| Skill | Example request | Starter capability |
| --- | --- | --- |
| `fde-onboarding` | “Help me turn this process into an app.” | Intake, environment discovery, next steps |
| `fde-databricks-apps` | “Build and deploy an internal Databricks app.” | App planning, platform setup, validation and delivery guidance |
| `fde-azure-devops` | “Set up CI/CD for this app.” | Pipeline design, target and identity configuration, release handoff |
| `fde-app-support` | “My app stopped working after deployment.” | Triage, evidence collection, recovery and handoff |
| `fde-microsoft-graph` | “Connect this app to Microsoft 365.” | Integration and permissions planning; no connector is configured |

These are initial team workflows, not a prebuilt application or authenticated integration. The Databricks skill can use installed official Databricks product skills; when absent, it directs the agent to current official documentation. No external skills are bundled or automatically installed.

## Package layout

```text
plugin.json                  Portable plugin manifest
mcp.json                     Empty integration registration point
.agents/plugins/marketplace.json  Codex catalog pointing to this root package
skills/
  fde-onboarding/             SKILL.md + application brief template
  fde-databricks-apps/        SKILL.md + delivery reference
  fde-azure-devops/           SKILL.md + release checklist
  fde-app-support/            SKILL.md + incident template
  fde-microsoft-graph/        SKILL.md + integration brief template
docs/                        Team configuration and extension guidance
scripts/validate.py          Local structural checks
tests/                       Catalog regressions and opt-in Codex checks
schemas/                     Bundled official plugin/MCP schemas
azure-pipelines.yml          CI for this plugin repository
```

## Validate changes

Python 3.11 or newer:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
```

Validation checks the manifests against bundled schemas, the local catalog, skill metadata, local Markdown links, and package path containment. It does not establish agent behavior or deployment readiness. The [distribution guide](docs/distribution.md) records isolated CLI verification and how to run opt-in client checks. The Azure pipeline runs structural validation and catalog regression tests; for Azure Repos pull requests, configure a build-validation branch policy. It does not deploy applications.

Before team rollout, fill in [team configuration](docs/team-configuration.md), complete the selected client's installation checks, and follow [contributing guidance](CONTRIBUTING.md). The guide uses the configured Git remote; maintainers still need to establish distribution terms and access/support ownership.
