# Delivery reference

## Before implementation

Separate analytics reads from operational state. A SQL warehouse can serve analytical queries; persistent forms and transactional workflows may need Lakebase or another approved store. Discuss latency, writes, access boundaries, and operational ownership before adding infrastructure. A request for filtering alone does not imply a new database.

Record the selected workspace/profile, app name, resource IDs, data-access identity, and environment. App runtime configuration and resource provisioning are distinct concerns: `app.yaml` configures the app process; a deployment bundle may manage workspace resources. Derive both from current platform tooling/docs and the actual project.

## Verification and handoff

- Run the project's build, type checks, and meaningful tests; verify the platform validation command supported by the installed CLI.
- Verify the runtime port/bind settings and resource declarations against Databricks Apps requirements.
- After an authorized deployment, check deployment/app state and exercise the primary workflow with an appropriately permitted identity. A running process alone does not prove data access works.
- Record the URL, revision, target environment, configuration dependencies, support owner, and recovery procedure. Redact credentials and user data from evidence.
- For CI/CD, determine one deployment mechanism for each target and avoid having local tooling and pipelines independently own conflicting resource state.

## Sources

- [Databricks Apps documentation](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/)
- [Azure Databricks Apps documentation](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-apps/)
- [Databricks CLI documentation](https://docs.databricks.com/aws/en/dev-tools/cli/)

Choose documentation for the workspace's actual cloud. Recheck commands, supported frameworks, and authentication when implementing; this reference deliberately does not pin an application stack or deployment identity.
