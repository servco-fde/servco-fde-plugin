## 1. Package and catalog
- [x] 1.1 Verify current official Codex catalog, installation-scope, and lifecycle documentation; record the selected client surface/version and outstanding rollout inputs in team configuration.
- [x] 1.2 Add `.agents/plugins/marketplace.json` with an entry for the repository-root `servco-fde-plugin` using the documented source resolution rules.
- [x] 1.3 Add documented client compatibility files only if required; preserve root portable manifests, plugin identity, skill layout, and self-contained resources. Native CLI accepted the portable manifest; no adapter needed.
- [x] 1.4 Extend `scripts/validate.py` for catalog structure, duplicate identity, local source containment/resolution, and manifest consistency; exercise valid and invalid fixture cases.

## 2. FDE and maintainer guidance
- [x] 2.1 Add `docs/distribution.md` with a full-plugin onboarding prompt, real-input prerequisites, installation scope, activation/reload steps, verification, and private-source troubleshooting.
- [x] 2.2 Document individual-skill installation separately and demonstrate distinct shared and app-local skill names with app workflows under `.agents/skills/`.
- [x] 2.3 Document update, pinning, rollback, and removal using verified client operations; explain catalog refresh versus installed-plugin changes and any unavailable operations.
- [x] 2.4 Link the guide from README and CONTRIBUTING; record source URL, access/distribution policy, maintenance owner, and compatibility status in team configuration without inventing unresolved values.

## 3. Verification and release readiness
- [x] 3.1 Run `python3 scripts/validate.py` with `requirements-dev.txt` installed and confirm meaningful invalid catalog fixtures fail.
- [ ] 3.2 In a clean selected client, install from the real Git-backed catalog and verify shared workflow discovery and use from two scratch application repositories without copying shared skills into them.
- [x] 3.3 Verify a distinct app-local skill coexists with the shared plugin and that an individually installed skill can access its packaged resources.
- [x] 3.4 Exercise update, a pinned ref, rollback to prior workflow content, and removal; record client/version, source ref, steps, outcomes, and reload requirements. Completed against offline Git fixture tags; actual GitHub verification remains in 3.2.
- [ ] 3.5 Check private-source installation and missing-access behavior where applicable; record unavailable checks and keep untested clients explicitly unverified.
- [x] 3.6 Walk through the onboarding prompt as an FDE, checking routing, missing inputs, and authorization boundaries; record evidence in the distribution guide. Completed as a manual instruction review; actual agent invocation remains in 3.2.
- [x] 3.7 Run `reffy validate` and `reffy plan validate add-shared-plugin-distribution`; review acceptance scenarios against recorded evidence before marking implementation complete.

## Remaining rollout verification

Local implementation and offline CLI checks are complete. Tasks 3.2 and 3.5 remain open until the catalog is available at a real accessible GitHub ref and the FDE/client walkthrough and applicable private-access checks are performed. Record that evidence in `docs/distribution.md`; do not archive this change or claim full rollout verification yet.
