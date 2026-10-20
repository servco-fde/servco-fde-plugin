---
name: fde-app-support
description: Diagnose and recover an existing internal app or delivery pipeline. Use for failed Databricks Apps deployments, broken workflows, access errors, or Azure DevOps build and release failures.
---

# Application support

Start with impact, environment, last known working behavior, and the failing step. Use [the incident note](assets/incident-note.md) when the investigation needs a durable handoff; fill known details without delaying useful diagnostics.

1. Inspect project instructions, current changes, the failing error, and recent deployment/configuration changes. Separate local build, CI, deployment, runtime, data access, and external API failures.
2. Use read-only status and bounded logs first. Reuse the user's selected Databricks profile, or present profiles/workspace URLs and obtain their choice. Load available platform skills or current official documentation for commands.
3. Identify a testable hypothesis and run the smallest useful check. Redact tokens and sensitive records; do not dump whole environments or tenant datasets.
4. Make a focused fix within the authorized scope, then repeat the failing check and relevant regression checks. For recovery, assess whether a rollback is compatible with persistent data and configuration before applying it.
5. If access or an external owner blocks progress, provide the precise missing permission/resource and sanitized evidence. Do not send escalation messages unless instructed.

Report observed facts separately from hypotheses, what changed, evidence of recovery, and unresolved impact. Do not claim recovery based only on a passing build or an app reporting a running state.
