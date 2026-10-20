# servco-fde-plugin

A starter agent plugin for Forward Deployed Engineers building and supporting internal applications. It packages reusable workflows as skills, with Databricks Apps as the initial delivery platform and Azure DevOps as the CI/CD platform. Microsoft Graph integration starts as a planning workflow.

## What is an agent plugin?

An agent plugin packages reusable capabilities into a portable directory that a compatible agent client can discover and load. The [Agent Plugins v1 specification](https://agent-plugins.org/specification) defines two component types: skills and MCP servers.

- **`plugin.json`** (required, at the root): identifies the plugin and its target specification through `$schema` and `name`, with optional metadata such as version and description.
- **`skills/<name>/SKILL.md`** (optional): gives the agent instructions for a particular workflow. Each skill sits directly under `skills/` and follows the [Agent Skills specification](https://agentskills.io/specification), with optional scripts, references, and assets alongside it.
- **`mcp.json`** (optional, at the root): configures Model Context Protocol servers that expose tools and context to the agent.

The client discovers components at these fixed locations. This plugin uses skills to share FDE workflows; its MCP configuration is currently empty.

## Start here

1. Clone or download this repository into a trusted local directory.
2. In an agent client that supports [Agent Plugins v1](https://agent-plugins.org/specification), use that client's documented local-plugin installation flow and select this directory as the plugin root. Installation commands and support vary by client; this scaffold includes no client-specific installer or marketplace adapter.
3. Ask: **“Help me get started as an FDE and build my first internal app.”** The `fde-onboarding` skill guides intake and environment setup.

If your client supports only [Agent Skills](https://agentskills.io/specification), install the individual directories under `skills/` using its documented skill installation flow. Each skill keeps its own required references and templates. Opening this repository alone does not guarantee skill discovery.

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
skills/
  fde-onboarding/             SKILL.md + application brief template
  fde-databricks-apps/        SKILL.md + delivery reference
  fde-azure-devops/           SKILL.md + release checklist
  fde-app-support/            SKILL.md + incident template
  fde-microsoft-graph/        SKILL.md + integration brief template
docs/                        Team configuration and extension guidance
scripts/validate.py          Local structural checks
schemas/                     Bundled official plugin/MCP schemas
azure-pipelines.yml          CI for this plugin repository
```

## Validate changes

Python 3.11 or newer:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

Validation checks the manifests against bundled schemas, skill metadata, local Markdown links, and package path containment. It does not establish agent behavior, deployment readiness, or runtime client compatibility. The Azure pipeline runs the same checks; for Azure Repos pull requests, configure a build-validation branch policy. It does not deploy applications.

Before team rollout, fill in [team configuration](docs/team-configuration.md), select a supported client, and follow [contributing guidance](CONTRIBUTING.md). No license or repository URL is assumed; maintainers should choose distribution terms before wider publication.
