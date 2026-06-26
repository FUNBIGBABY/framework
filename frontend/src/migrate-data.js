const isolationMessage =
  'Legacy client-side migration tooling is isolated for Phase 6 SDK removal.'

export async function checkMigrationStatus() {
  return {
    isolated: true,
    message: isolationMessage,
    users: {
      total: 0,
      migrated: 0,
      needMigration: 0,
    },
    frameworks: {
      total: 0,
      migrated: 0,
      needMigration: 0,
    },
  }
}

export async function runFullMigration() {
  return {
    success: false,
    skipped: true,
    message: isolationMessage,
    users: {
      updated: 0,
      skipped: 0,
      errors: [],
    },
    frameworks: {
      updated: 0,
      skipped: 0,
      errors: [],
    },
  }
}
