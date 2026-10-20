---
name: fde-azure-devops
description: Create or troubleshoot Azure DevOps CI/CD for an internal application, especially delivery to Databricks Apps. Use for Azure Pipelines YAML, build validation, release environments, and deployment identity setup.
---

# Azure DevOps delivery

Inspect the application repository, pipeline definitions, package manager, and delivery conventions first. The plugin repository's root pipeline validates the plugin only; do not copy it as an application deployment pipeline without adapting it.

1. Resolve the organization, project, repository, branch policy, agent pool, and intended environments from existing configuration or user input. Prepare local pipeline files while unresolved external settings are being identified.
2. Use the application's build and test commands. Keep CI validation separate from release stages so pull-request checks do not deploy. For Azure Repos, verify build-validation branch policies rather than assuming YAML `pr` triggers configure them.
3. Determine the target workspace and deployment identity for each environment. Use approved secret storage or supported federation, verifying the chosen Azure DevOps-to-Databricks authentication flow in current documentation. Do not assume an Azure service connection automatically authenticates the Databricks CLI. Pass an explicitly configured profile on workspace commands.
4. If using Databricks bundles, load available `databricks-core` and `databricks-dabs` skills, or consult official bundle documentation. Validate before deploying and tie releases to a known revision/artifact.
5. Use [the release checklist](assets/release-checklist.md) to capture target, checks, verification, and recovery. Respect configured environment checks and existing authorization; do not invent additional approval steps.
6. Validate the YAML locally where possible. Publish, queue, or change external pipeline settings only within the user's authorized scope. Distinguish local syntax checks from a successful Azure Pipelines run.

Use current [Azure Pipelines documentation](https://learn.microsoft.com/en-us/azure/devops/pipelines/) and [Databricks CI/CD guidance](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/). End with changes made, validation evidence, and any organization-specific setup still required.
