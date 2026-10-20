---
name: fde-databricks-apps
description: Plan, build, validate, or deliver an internal application on Databricks Apps. Use for custom app development and Databricks Apps deployment, including app resources and data access choices.
---

# Databricks Apps delivery

Use [the delivery reference](references/delivery.md) for platform decisions and validation evidence.

1. Inspect the target application's instructions and stack. Preserve an existing framework and package manager unless the task calls for changing them. Confirm the intended users, first workflow, data sources, and whether persistent writes are needed.
2. When available, load official `databricks-core` first, then `databricks-apps`; also load the matching design, Python, Lakebase, or bundle skill when the work requires it. These are optional installed capabilities, not files bundled here. If absent, consult current official Databricks Apps documentation before choosing commands or APIs.
3. Before workspace operations, have the user select a profile from available profiles and workspace URLs. Reuse an explicitly selected session profile; include `--profile` on commands. Determine required CLI features from the installed CLI's help and current documentation.
4. Resolve data access and storage with the user before scaffolding. Use platform-generated scaffolding when supported; inspect its current manifest/options rather than inventing feature names or resource keys. Keep generated app source in the selected application repository.
5. Implement the requested slice, including meaningful loading, empty, and error states. Keep credentials server-side and bind resources through the platform's supported configuration. Validate locally with the project's actual checks and update smoke tests to match the app.
6. If deployment is in scope and authorized, validate configuration, deploy to the selected target, and verify running status and the user workflow. Otherwise leave a concrete reviewed change and state what deployment still needs. Use `fde-azure-devops` when CI/CD is requested.

Report what works, checks run, deployment status, and remaining dependencies. Never describe an unexecuted deployment as successful.
