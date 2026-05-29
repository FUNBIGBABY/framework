/**
 * Data migration script
 *
 * File location: frontend/src/migrate-data.js
 *
 * Purpose: To add new fields to existing users and frameworks.
 */

import { db } from './lib/firebase'
import {
  collection,
  getDocs,
  doc,
  updateDoc,
  serverTimestamp,
  setDoc,
} from 'firebase/firestore'

/**
 * Generate secure random keys
 */
function generateSecureKey(length = 32) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * Migrate existing user data
 * Add roles and expertProfile fields for all users.
 */
export async function migrateUsers() {
  console.log('🔄 Start migrating user data...')

  try {
    const usersSnapshot = await getDocs(collection(db, 'users'))
    let updatedCount = 0
    let skippedCount = 0
    const errors = []

    for (const userDoc of usersSnapshot.docs) {
      const userData = userDoc.data()

      // Check if the roles field already exists.
      if (userData.roles && Array.isArray(userData.roles)) {
        console.log(
          `⏭️  Skip User ${userDoc.id}(The roles field already exists.)`
        )
        skippedCount++
        continue
      }

      try {
        // Update user documentation
        const updates = {
          roles: ['client', 'expert'], // Assuming all existing users are experts
          expertProfile: {
            tenantId: null,
            displayName: userData.username || userData.displayName || 'Expert',
            isApproved: true,
            createdAt: serverTimestamp(),
          },
        }

        await updateDoc(doc(db, 'users', userDoc.id), updates)
        console.log(`✅ Update user ${userDoc.id}`)
        updatedCount++
      } catch (error) {
        console.error(`❌ Update user ${userDoc.id} fail:`, error)
        errors.push({ id: userDoc.id, error: error.message })
      }
    }

    console.log(`\n📊 User migration complete:`)
    console.log(`   - renew: ${updatedCount} users`)
    console.log(`   - jump over: ${skippedCount} users`)
    if (errors.length > 0) {
      console.log(`   - errors: ${errors.length} `)
      console.log('Error Details:', errors)
    }

    return {
      success: true,
      updated: updatedCount,
      skipped: skippedCount,
      errors: errors,
    }
  } catch (error) {
    console.error('❌ User migration failed:', error)
    throw error
  }
}

/**
 * Migrate existing framework data
 * Add tenantId and expertId fields to all frameworks.
 *
 * @param {string} defaultTenantId - Default tenant ID (e.g., 'legacy')
 */
export async function migrateFrameworks(defaultTenantId = 'legacy') {
  console.log('🔄 Start migrating framework data...')

  try {
    const frameworksSnapshot = await getDocs(collection(db, 'frameworks'))
    let updatedCount = 0
    let skippedCount = 0
    const errors = []

    for (const frameworkDoc of frameworksSnapshot.docs) {
      const frameworkData = frameworkDoc.data()

      // Check if tenantId and expertId already exist.
      if (frameworkData.tenantId && frameworkData.expertId) {
        console.log(
          `⏭️  Skip Frame ${frameworkDoc.id}(New field already exists)`
        )
        skippedCount++
        continue
      }

      try {
        // Update framework documentation
        const updates = {
          tenantId: defaultTenantId, // Use the default tenant ID
          expertId: frameworkData.creatorId, // expertId = creatorId
        }

        // If the isPublic field is not specified, it is set to false by default.
        if (frameworkData.isPublic === undefined) {
          updates.isPublic = false
        }

        await updateDoc(doc(db, 'frameworks', frameworkDoc.id), updates)
        console.log(`✅ Update framework ${frameworkDoc.id}`)
        updatedCount++
      } catch (error) {
        console.error(`❌ Update framework ${frameworkDoc.id} fail:`, error)
        errors.push({ id: frameworkDoc.id, error: error.message })
      }
    }

    console.log(`\n📊 Framework migration complete:`)
    console.log(`   - renew: ${updatedCount} frameworks`)
    console.log(`   - jump over: ${skippedCount} frameworks`)
    if (errors.length > 0) {
      console.log(`   - error: ${errors.length} `)
      console.log('Error details:', errors)
    }

    return {
      success: true,
      updated: updatedCount,
      skipped: skippedCount,
      errors: errors,
    }
  } catch (error) {
    console.error('❌ Framework migration failed:', error)
    throw error
  }
}

/**
 * Create a default tenant for a specific user
 *
 * @param {string} userId - User ID
 * @param {string} tenantId - Tenant ID (e.g., 'ai-readiness')
 * @param {string} displayName - Tenant display name
 */
export async function createDefaultTenant(userId, tenantId, displayName) {
  console.log(`🏢 For users ${userId} Create a default tenant...`)

  try {
    const embedKey = `embed_${generateSecureKey()}`

    const tenantDoc = {
      id: tenantId,
      expertId: userId,
      subdomain: `${tenantId}.valorie.ai`,
      displayName: displayName,
      embedKey: embedKey,
      allowedOrigins: ['https://valorie.ai'],
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
      isActive: true,
    }

    await setDoc(doc(db, 'tenants', tenantId), tenantDoc)
    console.log(`✅ Tenant created successfully: ${tenantId}`)
    console.log(`   Embed Key: ${embedKey}`)

    return { success: true, tenantId, embedKey }
  } catch (error) {
    console.error('❌ Tenant creation failed:', error)
    throw error
  }
}

/**
 * Complete migration process
 * Perform all migration steps in sequence.
 */
export async function runFullMigration() {
  console.log('🚀 Begin the complete data migration...\n')

  try {
    // 1. Migrate users
    console.log('=== Step 1/2: Migrate Users ===')
    const usersResult = await migrateUsers()

    // 2. Migration Framework
    console.log('\n=== Step 2/2: Migration Framework ===')
    const frameworksResult = await migrateFrameworks('legacy')

    console.log('\n🎉 The migration was a complete success!')
    console.log('\n📊 Summarize:')
    console.log(
      `   users: ${usersResult.updated} have been updated, ${usersResult.skipped} have been skipped.`
    )
    console.log(
      `   Frameworks: ${frameworksResult.updated} have been updated, ${frameworksResult.skipped} have been skipped.`
    )

    if (usersResult.errors.length > 0 || frameworksResult.errors.length > 0) {
      console.log('\n⚠️  Some errors occurred:')
      if (usersResult.errors.length > 0) {
        console.log(`   User error:${usersResult.errors.length} `)
      }
      if (frameworksResult.errors.length > 0) {
        console.log(`   Framework errors: ${frameworksResult.errors.length}`)
      }
    }

    console.log('\n⚠️  Note: All old frames now belong to the "legacy" tenant.')
    console.log(
      '   You can manually move the frame to the correct tenant later.'
    )

    return {
      success: true,
      users: usersResult,
      frameworks: frameworksResult,
    }
  } catch (error) {
    console.error('❌ Complete migration failed:', error)
    throw error
  }
}

/**
 * Check data status
 * Check how much data needs to be migrated.
 */
export async function checkMigrationStatus() {
  console.log('🔍 Check data migration status...\n')

  try {
    // Check user
    const usersSnapshot = await getDocs(collection(db, 'users'))
    let usersNeedMigration = 0
    let usersAlreadyMigrated = 0

    usersSnapshot.docs.forEach(doc => {
      const data = doc.data()
      if (!data.roles || !Array.isArray(data.roles)) {
        usersNeedMigration++
      } else {
        usersAlreadyMigrated++
      }
    })

    // Inspection Frame
    const frameworksSnapshot = await getDocs(collection(db, 'frameworks'))
    let frameworksNeedMigration = 0
    let frameworksAlreadyMigrated = 0

    frameworksSnapshot.docs.forEach(doc => {
      const data = doc.data()
      if (!data.tenantId || !data.expertId) {
        frameworksNeedMigration++
      } else {
        frameworksAlreadyMigrated++
      }
    })

    console.log('📊 Migration Status Report:\n')
    console.log('user:')
    console.log(`   ✅ Migrated: ${usersAlreadyMigrated}`)
    console.log(
      `   ⏳ Number of users needing migration: ${usersNeedMigration}`
    )
    console.log('\nframe:')
    console.log(`   ✅ Migrated: ${frameworksAlreadyMigrated}`)
    console.log(
      `   ⏳ Number of migrations required: ${frameworksNeedMigration}`
    )

    if (usersNeedMigration === 0 && frameworksNeedMigration === 0) {
      console.log('\n🎉 All data migration is complete!')
    } else {
      console.log('\n💡 You need to run the migration tool to update the data.')
    }

    return {
      users: {
        needMigration: usersNeedMigration,
        migrated: usersAlreadyMigrated,
        total: usersNeedMigration + usersAlreadyMigrated,
      },
      frameworks: {
        needMigration: frameworksNeedMigration,
        migrated: frameworksAlreadyMigrated,
        total: frameworksNeedMigration + frameworksAlreadyMigrated,
      },
    }
  } catch (error) {
    console.error('❌ Check failed:', error)
    throw error
  }
}

// Export all functions
export default {
  migrateUsers,
  migrateFrameworks,
  createDefaultTenant,
  runFullMigration,
  checkMigrationStatus,
}
