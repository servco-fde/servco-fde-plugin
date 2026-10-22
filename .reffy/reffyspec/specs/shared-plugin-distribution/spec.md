# shared-plugin-distribution Specification

## Purpose
Distribute reusable FDE workflows through a portable plugin and a verified Codex catalog, with repeatable installation, lifecycle operations, and complementary application-local skills.

## Requirements

### Requirement: Catalog preserves portable package identity
The repository SHALL provide a Codex distribution catalog at `.agents/plugins/marketplace.json` that resolves to the existing root plugin using the documented catalog format. The root `plugin.json` SHALL retain the `servco-fde-plugin` identity and standard portable fields, with skills at immediate `skills/<name>/SKILL.md` locations.

#### Scenario: Client resolves the catalog entry
- **WHEN** a supported client reads the repository's catalog
- **THEN** the entry resolves to the root plugin and its self-contained skill resources
- **AND** client-specific metadata is kept outside the portable manifest

### Requirement: Repeatable full-plugin onboarding
The documentation SHALL provide a copyable agent prompt and a verified installation flow from a supplied GitHub source using the client's supported user scope, with prerequisites, activation steps, and a workflow invocation to confirm discovery.

#### Scenario: FDE installs shared workflows
- **GIVEN** an accessible source and a client/version recorded as verified
- **WHEN** the FDE follows the full-plugin installation guide
- **THEN** shared workflows can be discovered and used in two separate application repositories
- **AND** neither application requires a copied shared-skill tree

#### Scenario: Source or client information is missing
- **WHEN** the install request omits required source or client information that is absent from the session and team configuration
- **THEN** the guidance directs the agent to request those missing inputs before dependent installation steps
- **AND** does not invent a repository URL or claim unsupported compatibility

### Requirement: Shared and app-specific workflow scopes
The documentation SHALL distinguish centrally installed shared workflows from app-owned skills in `.agents/skills/<skill-name>/SKILL.md`. It SHALL demonstrate distinct names without relying on local skills overriding plugin skills.

#### Scenario: Application adds a complementary workflow
- **GIVEN** the shared plugin is installed
- **WHEN** an application adds a skill with a distinct name for its infrastructure directories and validation commands
- **THEN** the shared workflow and the app-specific workflow remain discoverable and usable
- **AND** the guide explains which scope owns each workflow

### Requirement: Individual-skill installation remains available
The documentation SHALL provide a separate installation path for clients supporting individual skills and SHALL explain its scope relative to full-plugin installation. Required skill resources SHALL remain inside the owning skill.

#### Scenario: FDE installs one workflow
- **WHEN** an FDE follows the individual-skill installation path
- **THEN** the selected skill can resolve its packaged references and assets
- **AND** the instructions do not imply that the full plugin or its integrations were installed

### Requirement: Documented plugin lifecycle
The distribution guide SHALL cover update, version pinning, rollback, and removal with verified client operations or explicit limitations and tested supported alternatives. It SHALL distinguish marketplace refresh from changes to an installed plugin and identify source refs, package versions, and required activation steps.

#### Scenario: FDE updates and restores an earlier version
- **GIVEN** a verified client and two identified source revisions
- **WHEN** the FDE follows the update and rollback procedures
- **THEN** installed workflow content can be checked against each intended revision
- **AND** the guide explains how to keep a selected revision pinned

#### Scenario: FDE removes the plugin
- **WHEN** the FDE follows the verified removal procedure and required reload steps
- **THEN** the client's installed-plugin state reflects removal
- **AND** app-owned skills remain available

### Requirement: Private-source prerequisites and configuration boundaries
The guide SHALL explain existing repository access requirements and missing-access recovery for private sources. Distributed files and verification records SHALL exclude credentials and application/customer configuration. Installing the plugin SHALL NOT imply permission to create infrastructure or grant access.

#### Scenario: Private repository access is unavailable
- **WHEN** installation cannot retrieve a private source with the user's existing access
- **THEN** the guidance identifies the access prerequisite and directs the FDE to the documented access process when available
- **AND** does not request tokens in committed files or claim installation succeeded

### Requirement: Local catalog validation
The repository validator SHALL check required catalog fields, duplicate plugin identity, local source resolution and containment, and consistency with the root manifest without requiring live platform resources or remote schema retrieval.

#### Scenario: Catalog points to an invalid package
- **WHEN** a catalog fixture has a missing required field, duplicate identity, missing or escaping source, or inconsistent manifest identity
- **THEN** local validation fails with an actionable error

#### Scenario: Valid package and catalog pass
- **WHEN** the repository catalog resolves to the intended portable package with valid metadata
- **THEN** local validation passes alongside existing manifest, skill, and link checks

### Requirement: Evidence-based client compatibility
The distribution guide SHALL record client surface/version, source ref, verification steps, outcomes, and limitations for clean installation, cross-repository use, app-local coexistence, individual-skill resources, and lifecycle operations. Codex SHALL be the first client evaluated; additional clients SHALL remain explicitly unverified until independently exercised.

#### Scenario: Structural checks pass without a client run
- **WHEN** local validation succeeds but installation or lifecycle checks have not run
- **THEN** documentation distinguishes structural validity from verified client behavior
- **AND** unavailable private-source or client checks remain visibly unverified
