# How to use the Servco FDE plugin

Audience: new and returning Forward Deployed Engineers.
Recorded 2026-10-22 (Pacific/Honolulu).

The plugin gives your agent five reusable workflows for outlining an app,
building it, preparing delivery, troubleshooting, and planning Microsoft 365
integrations. You describe the outcome; the agent uses the workflow and your
application's files to produce concrete work.

This how-to uses Codex CLI, verified with version **0.163.0** and plugin
**0.1.0**. Desktop/IDE, Claude Code, and Cursor installation have not been
verified for this package. See the [distribution guide](../../docs/distribution.md)
for compatibility evidence and detailed installation/lifecycle instructions.

## 1. Install once

Have Codex CLI installed and signed in, Git available, and network access to
GitHub. You do not need to clone the plugin into each application repository.

Open Codex CLI by running `codex` in your terminal, then paste this message:

> Help me install the Servco FDE plugin so I can use it across my projects in
> Codex CLI. The repository is
> `https://github.com/servco-fde/servco-fde-plugin.git`.
> Check whether my Codex version supports plugins and whether it is already
> installed. If needed, add the `servco-fde` marketplace from this repository
> and install `servco-fde-plugin`. Use the repository's default branch.
> Confirm the plugin is installed and enabled, then show me how to start a
> new session and try the onboarding workflow. If anything prevents installation,
> explain what I need to do in plain language.

You can paste this as written; there is no version or Git reference to fill in.

Or run these commands in a terminal:

```sh
codex --version
codex plugin marketplace list --json
codex plugin marketplace add https://github.com/servco-fde/servco-fde-plugin.git --json
codex plugin add servco-fde-plugin@servco-fde --json
codex plugin list --json
```

`servco-fde` is the marketplace name; `servco-fde-plugin` is the package name.
Confirm `installed` and `enabled` are true in the plugin listing. This uses the
repository's default branch. Choosing a specific tag or commit is optional. If this
marketplace is already configured at another source/ref, use the distribution
guide's reinstall procedure rather than assuming the add command changes it.
The command reference is the [official Codex CLI documentation](https://learn.chatgpt.com/docs/cli/reference).

The repository is currently public, so reading the plugin needs no GitHub token.
Installation does not set up Databricks, Azure DevOps, or Microsoft credentials.
For local previews, use a clean checkout: the tested CLI copied ignored `.env`
files when installing from a local working directory.

## 2. Open your application and start a fresh session

Open a terminal in the application repository you want to work on and run
`codex`. Start a new session after installation so the shared skills are loaded.
Create application files in that application's repository.

For a first local exercise, you can create a scratch repository:

```sh
mkdir equipment-request-demo
cd equipment-request-demo
git init
codex
```

Send this as a chat message inside Codex:

```text
$servco-fde-plugin:fde-onboarding Help me outline an internal app for tracking equipment requests. Save an application brief using your bundled template. Keep this exercise local; do not deploy or create cloud resources.
```

Expected result: a saved brief covering users, the workflow, data, access,
acceptance criteria, and the next useful milestone. The agent should fill known
details and identify unresolved choices. This exact exercise passed in two
independent scratch repositories, with all 13 template fields included.

## 3. Choose a workflow

You can describe what you need in plain language. To select a workflow
explicitly in Codex, put its full skill name at the start of the message:

| What you need | Skill to invoke | Useful output |
| --- | --- | --- |
| Turn an idea into a first step | `$servco-fde-plugin:fde-onboarding` | App brief, setup gaps, next milestone |
| Build or improve an application | `$servco-fde-plugin:fde-databricks-apps` | Implemented slice, local checks, delivery evidence when deployment is in scope |
| Prepare a delivery pipeline | `$servco-fde-plugin:fde-azure-devops` | Application pipeline files and release checklist |
| Investigate something broken | `$servco-fde-plugin:fde-app-support` | Focused diagnosis, fix/recovery evidence, incident handoff |
| Scope Microsoft 365 integration | `$servco-fde-plugin:fde-microsoft-graph` | Integration brief, identity/permission decisions, validation approach |

Example requests you can copy and adapt:

```text
$servco-fde-plugin:fde-databricks-apps Implement the first workflow from our application brief. Inspect the existing stack, clarify data and storage choices, and validate locally. Leave deployment for a later request.
```

```text
$servco-fde-plugin:fde-azure-devops Prepare CI/CD for this application using its existing build and test commands. Reuse documented organization and environment choices, and identify missing external settings. Save a release checklist.
```

```text
$servco-fde-plugin:fde-app-support The application worked before the last change and now fails at startup. Inspect recent changes and the error below, diagnose it, and verify a focused fix. [Paste a sanitized error and identify the affected environment.]
```

```text
$servco-fde-plugin:fde-microsoft-graph Plan how this app could read a signed-in user's calendar. Identify the identity flow, required permissions, consent decisions, and a minimal validation plan. Save an integration brief.
```

The Graph workflow currently provides integration planning; no Graph connector
is configured in this plugin. The Databricks workflow can use separately
installed official product skills or current documentation; those skills are
not bundled or automatically installed by this package.

## 4. Give the agent the decisions that matter

Explain the user/business task, the application repository, the first useful
outcome, and what work is in scope. For an existing app, point to its brief,
README, failing behavior, or existing pipeline.

For platform work, supply the selected target and known team settings. The
agent should reuse explicit choices, ask for missing information that changes
the result, and keep progressing on independent local work. Databricks workspace
operations require your explicit profile choice; the agent should not choose
`DEFAULT` automatically. Azure DevOps and Microsoft identity settings are
separate decisions, not values inferred from Databricks access.

Say whether the task is local planning/building, deployment, or recovery. An
installation or app idea alone does not grant infrastructure or permission
changes. Keep credentials in the chosen secret storage and use sanitized logs.

After work, expect the changed files, checks actually run, deployment status
where relevant, and remaining dependencies. A passing local build does not
establish that a deployed user workflow works.

## 5. Keep application-specific instructions with the app

Shared FDE workflows are installed in the client and can be used across
repositories. Instructions unique to one app belong in that app, for example:

```text
equipment-request-app/
  .agents/skills/equipment-release-check/SKILL.md
```

That local skill could identify the app's infrastructure directories, test
commands, and release checks. Use a distinct name so it complements the shared
workflow; do not rely on a local skill overriding a shared skill with the same
name. Application configuration, customer data, and secrets stay with their
appropriate application/configuration stores.

If your client supports individual skills only, copy a selected skill's entire
directory, including its references and assets, using the separate installation
path in the distribution guide. That does not install the full plugin.

## 6. Update or recover your installation

Ask your agent to check for updates when you need them. Refreshing the marketplace
alone does not confirm that the installed workflows changed. A specific tag or
commit is optional; use one when you need to reproduce or restore a version.

You can ask:

> Help me update the Servco FDE plugin from its GitHub repository's default
> branch. Check my current installation, save the current source commit so we
> can restore it if needed, and follow the distribution guide to install the
> updated workflows. Confirm what changed and tell me when to start a new session.

Use the [distribution guide](../../docs/distribution.md) for the exact update,
rollback, and removal commands. Start a fresh session after a change.

| Symptom | First action |
| --- | --- |
| Plugin commands are unavailable | Check `codex --version` and `codex plugin --help`; use a compatible CLI or the individual-skill path |
| Skill is missing from chat | Check `codex plugin list --json`, confirm installed/enabled state, then start a new session in the application repository |
| Marketplace uses an unexpected source/ref | Inspect `codex plugin marketplace list --json` and follow the documented reinstall sequence |
| Source cannot be read | Check repository/network access; if visibility becomes private, use existing approved Git access |
| Agent cannot reach an application platform | Resolve that platform's profile, target, and permissions separately from plugin installation |

## Further reference

- [Installation, lifecycle commands, and verification evidence](../../docs/distribution.md)
- [Available workflows and repository overview](../../README.md)
- [Team settings and outstanding rollout decisions](../../docs/team-configuration.md)
- [Bundled application brief template](../../skills/fde-onboarding/assets/application-brief.md)

Treat this as a dated usage reference. Check the distribution guide and current
client documentation when versions or client support change.
