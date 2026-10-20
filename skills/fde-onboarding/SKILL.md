---
name: fde-onboarding
description: Guide a new or returning FDE through local setup and turn an internal application idea into a concrete brief. Use for getting started, onboarding, or deciding the first development steps.
---

# FDE onboarding

Help the FDE reach a useful first development milestone. Explain unfamiliar terms briefly and keep questions tied to the next decision.

1. Read the project's instructions and existing implementation. Reuse known team and session choices. If the request is still an idea, use [the application brief](assets/application-brief.md) to capture users, the task, data, success criteria, and an initial slice. Fill known details and mark unresolved items; do not make the user answer every field before doing useful work.
2. Check local tools needed for that slice, existing repository access, and platform authentication without printing tokens. Report actual gaps and setup commands; do not install unrelated tooling.
3. For Databricks, list available profiles and workspace URLs, then let the user choose before any workspace operation. Preserve that choice and pass it explicitly. Do not select `DEFAULT` automatically.
4. Establish the application repository and development environment. This plugin repository is not the default destination for generated app source.
5. For app implementation, use the available `fde-databricks-apps` skill; for delivery pipelines, use `fde-azure-devops`. If these are unavailable, continue with current official documentation and disclose the missing capability.

Produce a saved application brief when useful, the first runnable or reviewable milestone within the request's scope, and a short explanation of what remains. Do not treat onboarding as authorization to create cloud resources or send messages.
