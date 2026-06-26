const isolationMessage =
  'Legacy data cleanup tooling is isolated for Phase 6 SDK removal.'

export async function cleanupData() {
  return {
    success: false,
    skipped: true,
    total: 0,
    updated: 0,
    errors: 0,
    error: isolationMessage,
  }
}

export async function verifyCleanup() {
  return {
    skipped: true,
    message: isolationMessage,
    total: 0,
    hasExpertId: 0,
    hasLegacyTenant: 0,
    missingPublishedToOrg: 0,
  }
}
