# Extending integrations

The initial package provides skills and an empty MCP registry. Databricks and Azure DevOps workflows can use tools already available in the user's client or locally installed CLIs. Installing this package grants no platform access.

For another platform:

1. Add a focused skill only when there is a concrete workflow to support. Include a self-contained brief or reference where useful.
2. Identify the real tool or API provider, owner, authentication method, needed operations, and permissions. Verify these against its official documentation.
3. If using MCP, register an actual server in root `mcp.json` following the [Agent Plugins MCP configuration](https://agent-plugins.org/specification#721-discovery-and-configuration). Use the specified transport and fields; do not assume a REST API URL is an MCP endpoint.
4. Configure credentials through the selected client's supported authentication mechanism. The portable specification defines `PLUGIN_ROOT` and `PLUGIN_DATA` placeholders; do not assume arbitrary environment-variable interpolation is portable.
5. Verify discovery and a minimal operation in each supported client. Document behavior when credentials, consent, network access, or the server are unavailable.

Microsoft Graph is currently a planning skill. Do not add speculative server URLs, tenant-wide scopes, or fake credentials. Add a working connector only after the team chooses a provider and access model.

Agent Plugins v1 discovers skills and MCP servers at fixed locations. Client-specific hooks, commands, agents, or installation adapters need the client's documented extension mechanism; they are not portable core components. Keep root `plugin.json` authoritative.
