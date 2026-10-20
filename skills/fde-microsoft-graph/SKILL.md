---
name: fde-microsoft-graph
description: Plan a Microsoft Graph integration for an internal application, including identity, endpoint selection, permissions, and consent requirements. Use when scoping Microsoft 365 data or actions; this starter skill does not provide a configured connector.
---

# Microsoft Graph integration planning

Prepare an implementable integration brief using [the template](assets/integration-brief.md). Inspect existing app authentication and available tools before proposing a new connector.

1. Establish the user workflow, Microsoft 365 resource, read/write operations, and intended audience. Do not infer tenant IDs, application registrations, or consent from Databricks access.
2. Distinguish delegated access on behalf of a signed-in user from application access without a signed-in user. Verify the specific endpoint supports the chosen access model and identify its documented least-privileged permissions.
3. Consult current official [Graph authentication guidance](https://learn.microsoft.com/en-us/graph/auth/auth-concepts) and [permissions overview](https://learn.microsoft.com/en-us/graph/permissions-overview), then the endpoint documentation. Record API version, consent needs, tenant restrictions, pagination, throttling, and applicable data boundaries.
4. Identify the backend identity flow and credential storage. Databricks application authentication does not by itself supply a Microsoft Graph token. Keep confidential-client credentials out of browser code.
5. Return the brief, required owner decisions, and a minimal validation plan. If implementation is requested, implement only the selected operation with the actual supported SDK/API and authentication method; do not register an invented MCP endpoint or assume permissions have been granted.

This package currently registers no Graph MCP server. Explain whether a proposed integration uses a direct API, an already available tool, or a new connector, and what remains to configure. Respect the user's existing authorization for external actions.
