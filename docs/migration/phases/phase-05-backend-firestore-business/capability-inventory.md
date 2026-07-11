# Phase 05 Historical Firebase Capability Disposition

## Purpose and source

This matrix reconciles the historical `frontend/src/lib/firebase.js` surface at implementation baseline `742f1e79f3fb71d44ce21284999e64ca76c5060f`. The historical file blob is unchanged from that commit's parent, so it is an inventory source rather than proof that Phase 5 rewrote the frontend. This is a capability-disposition record, not a reviewer verdict. Commit `742f1e79f3fb71d44ce21284999e64ca76c5060f` is the Phase 5 backend implementation commit; `a2115042771d9e91e9410cf5597031f3c78bee9a` added later status wording. Neither commit proves reviewer acceptance.

Every historical item uses exactly one disposition:

- `REST parity`
- `intentional deletion`
- `configuration replacement`
- `conditional data reconciliation`

The current review verdict remains in `docs/migration/REVIEW_LEDGER.md`.

## Capability matrix

| Historical item | Historical behavior / consumer | Disposition | Current contract and evidence | Status / condition |
|---|---|---|---|---|
| Firebase app initialization and `firebaseConfig` | Loaded `VITE_FIREBASE_*` and initialized the client SDK. | `configuration replacement` | Backend REST base URL and app naming are configured through current env/templates; Phase 6 removed Firebase package/env/runtime imports. See Phase 6 report and verification. | Complete as configuration replacement; not reviewer acceptance. |
| `auth` export | Exposed Firebase Auth to frontend consumers. | `configuration replacement` | Backend JWT cookie session through `/api/users/*`; `AuthContext.jsx` holds only in-memory user state. | Complete as configuration replacement. |
| `db` export | Exposed Firestore directly to frontend consumers. | `configuration replacement` | Backend-owned Postgres REST contracts; frontend no longer receives a database client. | Complete as configuration replacement. |
| `enableIndexedDbPersistence` | Enabled Firestore offline cache. | `intentional deletion` | Phase 6 explicitly removed Firebase offline persistence; current MVP has no equivalent offline database contract. | Intentionally absent. |
| `registerUser` | Public/self-service account creation entry point, already throwing in the historical baseline. | `intentional deletion` | Public registration remains disabled; first admin uses `backend_py/scripts/seed_admin.py`, later accounts use admin-only `/api/admin/users`. | Intentionally absent from the frontend. |
| `loginUser` | Firebase email/password login and last-login update. | `REST parity` | `POST /api/users/login` sets 1h access and 30d refresh httpOnly cookies; backend owns last-login updates. | Covered by Phase 6 cookie-session evidence. |
| `logoutUser` | Firebase sign-out. | `REST parity` | `POST /api/users/logout` clears cookies and advances refresh-session version when possible. | Covered by Phase 6 cookie-session evidence. |
| `onAuthChange` | Firebase auth-state subscription. | `REST parity` | `AuthContext` restores through `GET /api/users/me` and refreshes through `POST /api/users/refresh`; no Firebase subscription remains. | Session parity; transport intentionally changed. |
| `checkEmailExists` | Queried Firestore for email existence. | `REST parity` | Authenticated `GET /api/users/check-email/{email}` performs the backend query; admin creation also enforces uniqueness. | Backend-owned and authenticated. |
| `checkUsernameExists` | Queried Firestore for username existence. | `REST parity` | Authenticated `GET /api/users/check-username/{username}` performs the backend query; admin creation also enforces uniqueness. | Backend-owned and authenticated. |
| `createArtefactsForFramework` (internal) | Parsed `artefact_variants` / `_raw` and wrote child artefact documents after framework creation. | `conditional data reconciliation` | Current child-resource CRUD is `/api/frameworks/{framework_id}/artefacts`; current generation may also retain embedded `frameworks.artefacts_json`. No historical backfill/synchronization is claimed. | Open evidence condition; see “Historical artefact data condition” below. |
| `createFramework` | Created a framework from caller-provided framework data; loaded `tenantId` from the signed-in user's Firestore profile, derived `organization` from profile `joinedOrganization` with `tenantId` as fallback, and forced `creatorId` from Firebase Auth `user.uid`. These identity fields were not client-supplied. | `REST parity` | `POST /api/frameworks` and generation persistence create rows; owner comes from the backend JWT cookie, not the body. Tenant/org fields were intentionally excluded from parity. | Core capability covered by Phase 5 owner/generation tests. |
| Tenant/org side effects within historical framework creation | Added `tenantId`, `organization`, and `publishedToOrganization` to new rows. | `intentional deletion` | The personal-use schema and current REST contract do not recreate tenant/organization ownership or sharing. This is a decomposed side effect, not a second disposition for the `createFramework` export. | Intentionally absent. |
| `getMyFrameworks` | Listed the signed-in user's frameworks. | `REST parity` | `GET /api/frameworks/my-frameworks` with backend owner filtering. | Covered by Phase 5 owner CRUD tests. |
| `getFramework` | Loaded one framework without a reliable backend ownership boundary. | `REST parity` | `GET /api/frameworks/{framework_id}` with backend owner filtering and cross-user 404 behavior. | Covered by Phase 5 owner CRUD tests. |
| `updateFramework` | Updated a Firestore framework document. | `REST parity` | `PUT /api/frameworks/{framework_id}` with owner filtering and sparse frontend patches. | Covered by Phase 5/6 tests. |
| `deleteFramework` | Deleted a Firestore framework document. | `REST parity` | `DELETE /api/frameworks/{framework_id}` with owner filtering. | Covered by Phase 5 owner CRUD tests. |
| `onFrameworksChange` | Realtime Firestore subscription for owner frameworks. | `intentional deletion` | Owner list uses request-driven backend REST snapshots. No realtime or offline-subscription parity is claimed. | Realtime subscription intentionally absent. |
| `generateSecureKey` (internal) | Generated tenant embed keys. | `intentional deletion` | Tenant embed keys are outside the personal-use architecture. | Intentionally absent. |
| `createTenant` | Created tenant/subdomain/embed-key state. | `intentional deletion` | Phase 7 removed tenant route/state residue; no workspace replacement was introduced. | Intentionally absent. |
| `getMyTenant` | Loaded the current user's tenant. | `intentional deletion` | Personal routes and backend user ownership replace tenant routing; no tenant API exists. | Intentionally absent. |
| `updateTenant` | Updated tenant settings. | `intentional deletion` | No tenant/settings contract in the personal-use application. | Intentionally absent. |
| `regenerateEmbedKey` | Rotated a tenant embed key. | `intentional deletion` | No public embed/tenant capability in scope. | Intentionally absent. |
| `checkIsExpert` | Read a Firebase `roles` array. | `intentional deletion` | The personal-use backend has no expert-role product boundary. | Intentionally absent. |
| `upgradeToExpert` | Self-upgraded a user and created expert profile fields. | `intentional deletion` | Self-service role escalation is not part of the backend auth model. | Intentionally absent. |
| `generateToken` (internal) | Generated invitation tokens. | `intentional deletion` | Invitation flows were removed; no replacement invite system was added. | Intentionally absent. |
| `generateInviteLink` | Created tenant invitation links. | `intentional deletion` | Invite and organization sharing are outside the personal-use boundary. | Intentionally absent. |
| `getInviteLink` | Resolved an invite token across tenants. | `intentional deletion` | Invite routes/components were removed in Phase 7. | Intentionally absent. |
| `acceptInvite` | Joined an organization and rewrote framework organization fields. | `intentional deletion` | No tenant/org membership or invite acceptance contract exists. | Intentionally absent. |
| `leaveOrganization` | Removed membership and rewrote organization publication state. | `intentional deletion` | Organization membership and sharing were removed. | Intentionally absent. |
| `publishFrameworkToOrganization` | Published a framework to a tenant organization. | `intentional deletion` | Organization publishing was removed. Authenticated personal Library publishing is a different implemented REST capability; this wording is not reviewer acceptance. | Intentionally absent. |
| `unpublishFrameworkFromOrganization` | Removed organization publication state. | `intentional deletion` | Organization publication was removed. Personal Library unpublish uses `/api/frameworks/{id}/unpublish`. | Intentionally absent. |
| `getOrganizationFrameworks` | Listed frameworks shared to an organization. | `intentional deletion` | No organization library exists; authenticated personal Library uses `GET /api/frameworks/public`. | Intentionally absent. |
| `revokeInviteLink` | Revoked a tenant invitation. | `intentional deletion` | Invite system removed. | Intentionally absent. |
| `removeMember` | Removed a tenant member and changed their frameworks. | `intentional deletion` | Tenant membership removed; no replacement member API exists. | Intentionally absent. |
| `getTenantMembers` | Loaded tenant members and user profiles. | `intentional deletion` | Tenant/member UI and API removed. | Intentionally absent. |
| Hard-coded `SUPER_ADMIN_EMAIL` and `isSuperAdmin` | Trusted a frontend hard-coded address. | `configuration replacement` | `SUPER_ADMIN_EMAIL` is an env-controlled backend authorization boundary; frontend display checks are convenience only. | Backend-authoritative replacement. |
| `getWhitelistDomains` | Read mutable Firestore domain policy and created legacy defaults. | `intentional deletion` | No dynamic domain-policy admin API exists; the UI records it as unsupported. | Intentionally absent. |
| `addWhitelistDomain` | Mutated Firestore domain allowlist. | `intentional deletion` | No dynamic domain allowlist management surface exists. | Intentionally absent. |
| `removeWhitelistDomain` | Mutated Firestore domain allowlist. | `intentional deletion` | No dynamic domain allowlist management surface exists. | Intentionally absent. |
| `checkEmailDomainWhitelisted` | Applied client-side domain admission rules. | `configuration replacement` | Backend `ENABLE_PUBLIC_REGISTER=false` and exact `ALLOWED_EMAILS` configuration own admission; admin-created users use the admin-only contract. | Backend configuration replacement. |
| `getAllUsers` | Listed Firestore users for a client-side admin gate. | `REST parity` | `GET /api/admin/users`; backend checks `SUPER_ADMIN_EMAIL` and omits password hashes. | Covered by Phase 5 admin tests. |
| `blockUser` | Set Firestore `isBlocked`. | `REST parity` | `POST /api/admin/users/{user_id}/disable`; disabled users are rejected on login, access, and refresh. | Covered by Phase 5/6 auth-admin tests. |
| `unblockUser` | Cleared Firestore `isBlocked`. | `REST parity` | `POST /api/admin/users/{user_id}/enable`. | Covered by Phase 5 admin tests. |
| `checkUserBlocked` | Read client-side block status. | `REST parity` | Only admin `/api/admin/users*` responses expose `is_disabled`. Ordinary user/auth responses do not expose that field; backend login, authenticated access, and refresh enforcement reject disabled users. | Backend enforcement replaces client trust. |
| Firebase module default export | Aggregated SDK objects and Firestore helpers for direct component use. | `configuration replacement` | `frontend/src/lib/api.js` and `AuthContext` expose REST/session helpers; no SDK object is exported. | Complete as module-boundary replacement. |

## Adjacent Phase 5 surfaces

These items were not named exports of `firebase.js`, but they were part of the same Firestore-to-backend boundary and are retained here so the disposition is not lost.

| Surface | Disposition | Current contract and evidence | Status |
|---|---|---|---|
| Direct Firestore public-Library query and publish UI | `REST parity` | Authenticated `GET /api/frameworks/public`, `POST /api/frameworks/{id}/publish`, and `POST /api/frameworks/{id}/unpublish`; see `frameworks_public.py` and Phase 5 publish/public tests. | Backend contract implemented; frontend REST wiring recorded in Phase 6. |
| `sync-library`, `push-framework`, and `log-event` active external sync paths | `REST parity` | The route names remain authenticated and return documented HTTP 501 quarantine responses; real indexing/retrieval remains Phase 9. | Contract parity is the authenticated deferred response, not successful vector indexing. |

## Historical artefact data condition

Current status is **not run**, not “not applicable.” This docs-only repair did not start Postgres or inspect live data.

- Owner: `Data Reconciliation Owner`.
- Trigger: before importing legacy Firebase/framework rows; before deleting the embedded artefact fallback; or when an audit finds non-empty `frameworks.artefacts_json` without child rows or any partial/count/identity mismatch between embedded artefacts and child rows.
- SQL limitation: the query below detects only frameworks with non-empty embedded artefacts and zero child rows. It does not compare embedded artefact counts or identities with existing child rows, so a zero result alone cannot establish that the whole reconciliation is `not applicable`.
- Evidence needed for `not applicable`: dated evidence tied to the review candidate and database/snapshot identities that compares embedded artefact counts and identities with child rows, or an equivalent shape-aware audit with documented sampling and data-source provenance.
- If the limited query result is non-zero or any partial/count/identity mismatch exists: keep `conditional data reconciliation`, obtain separate authorization, define backup/rollback, and reconcile data outside this docs-only repair.

Limited evidence query template (zero-child case only):

```sql
SELECT count(*) AS embedded_without_child_rows
FROM frameworks AS f
WHERE COALESCE(f.artefacts_json, '{}'::jsonb) NOT IN ('{}'::jsonb, '[]'::jsonb)
  AND NOT EXISTS (
    SELECT 1
    FROM artefacts AS a
    WHERE a.framework_id = f.id
  );
```

## Focused reviewer attention

- Materials ownership: focused Migration Reviewer attention only. The reviewer should inspect the absence of an owner/user foreign key on `Material` and the current material routes' ownership behavior. No implementation change is authorized by this inventory.
- Legacy `vector_sync` request fields: focused Migration Reviewer attention only. The authenticated 501 schemas still retain legacy request concepts such as project/API/token/vector-store/organization inputs. Phase 9 owns any later API re-shaping. This inventory does not change the authenticated 501/deferred behavior.
