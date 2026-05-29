import { initializeApp } from 'firebase/app'
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  updateProfile,
} from 'firebase/auth'
import {
  getFirestore,
  collection,
  doc,
  setDoc,
  getDoc,
  getDocs,
  addDoc,
  updateDoc,
  deleteDoc,
  query,
  where,
  orderBy,
  serverTimestamp,
  enableIndexedDbPersistence, // Offline support
  onSnapshot,
} from 'firebase/firestore'

// ============= Firebase configuration =============

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

// ============= Initialize Firebase =============

const app = initializeApp(firebaseConfig)

// Initialize service
export const auth = getAuth(app)
export const db = getFirestore(app)

// ============= Enable offline support =============

// Enable Firestore offline persistence
// This allows users to access previously loaded data even when they are offline.
enableIndexedDbPersistence(db)
  .then(() => {
    console.log('✅ Firestore offline support is now enabled.')
  })
  .catch(err => {
    if (err.code === 'failed-precondition') {
      console.warn('⚠️ Offline support failed: Multiple tabs open')
    } else if (err.code === 'unimplemented') {
      console.warn('⚠️ Offline support failed: Browser not supported.')
    }
  })

/**
 * Register a new user (Expert Side)
 *
 * Users who register on Expert Side automatically receive an expert role.
 *
 * @param {string} email - User Email
 * @param {string} password - password
 * @param {string} username - username
 * @returns {Promise<Object>} User Information
 */
export const registerUser = async (email, password, username) => {
  try {
    // 1. Create Firebase Auth user
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      email,
      password
    )
    const user = userCredential.user

    // 2. Update user displayName
    await updateProfile(user, {
      displayName: username,
    })

    // 3. Create user documents in Firestore
    // 👇 Edits: Added roles and expertProfile
    await setDoc(doc(db, 'users', user.uid), {
      uid: user.uid,
      email: email,
      username: username,
      roles: ['client', 'expert'], // 👈 Having two roles
      expertProfile: {
        // 👈 Expert Information
        tenantId: null, // Populate when creating tenants later
        displayName: username,
        isApproved: true,
        createdAt: serverTimestamp(),
      },
      createdAt: serverTimestamp(),
      lastLogin: serverTimestamp(),
    })

    console.log('✅ Expert user registered:', user.uid)

    return {
      uid: user.uid,
      email: user.email,
      username: username,
      roles: ['client', 'expert'],
    }
  } catch (error) {
    console.error('Registration error:', error)
    throw error
  }
}

/**
 * User Login
 *
 * @param {string} email - User Email
 * @param {string} password - password
 * @returns {Promise<Object>} User Information
 */
export const loginUser = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(
      auth,
      email,
      password
    )
    const user = userCredential.user

    // Update last login time
    await updateDoc(doc(db, 'users', user.uid), {
      lastLogin: serverTimestamp(),
    })

    return {
      uid: user.uid,
      email: user.email,
      username: user.displayName,
    }
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}

/**
 * User Logout
 */
export const logoutUser = async () => {
  try {
    await firebaseSignOut(auth)
  } catch (error) {
    console.error('Logout error:', error)
    throw error
  }
}

/**
 * Check if the email address already exists.
 *
 * @param {string} email - Mail
 * @returns {Promise<boolean>} Does it exist?
 */
export const checkEmailExists = async email => {
  try {
    const q = query(collection(db, 'users'), where('email', '==', email))
    const querySnapshot = await getDocs(q)
    return !querySnapshot.empty
  } catch (error) {
    console.error('Check email error:', error)
    return false
  }
}

/**
 * Check if the username already exists.
 *
 * @param {string} username - username
 * @returns {Promise<boolean>} Does it exist?
 */
export const checkUsernameExists = async username => {
  try {
    const q = query(collection(db, 'users'), where('username', '==', username))
    const querySnapshot = await getDocs(q)
    return !querySnapshot.empty
  } catch (error) {
    console.error('Username error detected:', error)
    return false
  }
}

/**
 * Monitor authentication status changes
 *
 * @param {Function} callback - State change callback
 * @returns {Function} Function to cancel listening
 */
export const onAuthChange = callback => {
  return onAuthStateChanged(auth, callback)
}

/**
 * Internal tool: Extracts artefact_variants from frameworkData and stores them in the artefacts collection.
 *
 * @param {string} frameworkId - Framework Document ID
 * @param {Object} frameworkData - Data saved to frameworks (including artefact_variants or _raw)
 */
const createArtefactsForFramework = async (frameworkId, frameworkData) => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    if (!frameworkData) return

    let variants = null

    // 1. Prioritize using the top-level `artefact_variants` (if you'll be passing them in directly later).
    if (Array.isArray(frameworkData.artefact_variants)) {
      variants = frameworkData.artefact_variants
    } else if (frameworkData._raw) {
      // 2. Parse from _raw (_raw is now a JSON string)
      let raw = null
      if (typeof frameworkData._raw === 'string') {
        try {
          raw = JSON.parse(frameworkData._raw)
        } catch (e) {
          console.warn('Parsing frameworkData._raw failed:', e)
        }
      } else if (typeof frameworkData._raw === 'object') {
        raw = frameworkData._raw
      }

      if (raw) {
        // 2.1 Artefact_variants at the top level
        if (Array.isArray(raw.artefact_variants)) {
          variants = raw.artefact_variants
        }
        // 2.2 Artefact_variants under the framework (as returned by llm_global)
        else if (
          raw.framework &&
          Array.isArray(raw.framework.artefact_variants)
        ) {
          variants = raw.framework.artefact_variants
        }
      }
    }

    if (!variants || variants.length === 0) return

    const frameworkTitle =
      (frameworkData.metadata && frameworkData.metadata.title) ||
      frameworkData.title ||
      ''

    const tasks = []

    for (const variant of variants) {
      if (!variant || !variant.name) continue

      tasks.push(
        addDoc(collection(db, 'artefacts'), {
          frameworkId,
          frameworkTitle,
          variantId: variant.id || null,
          name: variant.name,
          summary: variant.summary || '',
          when_to_use: Array.isArray(variant.when_to_use)
            ? variant.when_to_use
            : [],
          sections: Array.isArray(variant.sections) ? variant.sections : [],
          risk_register: Array.isArray(variant.risk_register)
            ? variant.risk_register
            : [],
          creatorId: user.uid,
          createdAt: serverTimestamp(),
          updatedAt: serverTimestamp(),
        })
      )
    }

    if (tasks.length > 0) {
      await Promise.all(tasks)
    }
  } catch (error) {
    // Do not throw an exception to avoid affecting the Framework creation process.
    console.error('Error creating Artefact library:', error)
  }
}

// ============= Framework CRUD functions =============

/**
 * Create a new Framework
 *
 * Modification: Automatically add tenantId and expertId
 *
 * @param {Object} frameworkData - Framework data
 * @returns {Promise<string>} Framework ID
 */
export const createFramework = async frameworkData => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    // ✅ Add these 3 lines (your new code)
    const userRef = doc(db, 'users', user.uid)
    const userDoc = await getDoc(userRef)
    const userData = userDoc.data()

    // ✅ Add this line (your new code)
    const organization = userData.joinedOrganization || userData.tenantId

    // ✅ Modify this section and add a new field.
    const frameworkRef = await addDoc(collection(db, 'frameworks'), {
      ...frameworkData,
      tenantId: userData.tenantId,
      creatorId: user.uid,
      organization: organization,
      publishedToOrganization: false,
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
    })

    // ✅
    await createArtefactsForFramework(frameworkRef.id, frameworkData)

    return frameworkRef.id
  } catch (error) {
    console.error('Framework creation error:', error)
    throw error
  }
}

/**
 * Get all Frameworks for the current user
 *
 * @returns {Promise<Array>} Frameworks list
 */
export const getMyFrameworks = async () => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    const q = query(
      collection(db, 'frameworks'),
      where('creatorId', '==', user.uid),
      orderBy('createdAt', 'desc')
    )

    const querySnapshot = await getDocs(q)
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
    }))
  } catch (error) {
    console.error('Error retrieving Frameworks:', error)
    throw error
  }
}

/**
 * Get a single Framework
 *
 * @param {string} frameworkId - Framework ID
 * @returns {Promise<Object>} Framework data
 */
export const getFramework = async frameworkId => {
  try {
    const docRef = doc(db, 'frameworks', frameworkId)
    const docSnap = await getDoc(docRef)

    if (docSnap.exists()) {
      return { id: docSnap.id, ...docSnap.data() }
    } else {
      throw new Error('Framework does not exist.')
    }
  } catch (error) {
    console.error('Framework error:', error)
    throw error
  }
}

/**
 * Update Framework
 *
 * @param {string} frameworkId - Framework ID
 * @param {Object} updates - Updated data
 */
export const updateFramework = async (frameworkId, updates) => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    const frameworkRef = doc(db, 'frameworks', frameworkId)
    await updateDoc(frameworkRef, {
      ...updates,
      updatedAt: serverTimestamp(),
    })
  } catch (error) {
    console.error('Framework update error:', error)
    throw error
  }
}

/**
 * Remove Framework
 *
 * @param {string} frameworkId - Framework ID
 */
export const deleteFramework = async frameworkId => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    await deleteDoc(doc(db, 'frameworks', frameworkId))
  } catch (error) {
    console.error('Framework deletion error:', error)
    throw error
  }
}

// ============= Real-time monitoring function=============

/**
 * Real-time monitoring of the current user's Frameworks
 *
 * @param {Function} callback - Data change callback
 * @returns {Function} Function to cancel listening
 */
export const onFrameworksChange = callback => {
  const user = auth.currentUser
  if (!user) {
    console.warn('The user is not logged in and cannot listen to Frameworks.')
    return () => {}
  }

  const q = query(
    collection(db, 'frameworks'),
    where('creatorId', '==', user.uid),
    orderBy('createdAt', 'desc')
  )

  // Returns a function to cancel listening.
  return onSnapshot(q, querySnapshot => {
    const frameworks = querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
    }))
    callback(frameworks)
  })
}

// ============= Tenant Management Functions =============

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
 * Create a new tenant
 *
 * @param {Object} tenantData - Tenant data
 * @returns {Promise<Object>} { success: true, tenantId, embedKey }
 */
export const createTenant = async tenantData => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    // Generate tenant IDs (based on subdomain)
    // For example: ai-readiness.valorie.ai → ai-readiness
    const tenantId =
      tenantData.id || tenantData.subdomain.replace('.valorie.ai', '')

    // Generate embedded key
    const embedKey = `embed_${generateSecureKey()}`

    const tenantDoc = {
      id: tenantId,
      ownerId: user.uid,
      subdomain: tenantData.subdomain || `${tenantId}.valorie.ai`,
      displayName: tenantData.displayName || 'My Expert Studio',
      embedKey: embedKey,
      allowedOrigins: tenantData.allowedOrigins || [],
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
      isActive: true,
    }

    // Write to Firestore
    await setDoc(doc(db, 'tenants', tenantId), tenantDoc)

    console.log('✅ Tenant created:', tenantId)
    return { success: true, tenantId, embedKey }
  } catch (error) {
    console.error('Tenant creation error:', error)
    throw error
  }
}

/**
 * Get the current user's tenant
 *
 * @returns {Promise<Object|null>} Tenant data or null
 */
export const getMyTenant = async () => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    const q = query(collection(db, 'tenants'), where('ownerId', '==', user.uid))

    const querySnapshot = await getDocs(q)

    if (querySnapshot.empty) {
      return null
    }

    return {
      id: querySnapshot.docs[0].id,
      ...querySnapshot.docs[0].data(),
    }
  } catch (error) {
    console.error('Tenant error:', error)
    throw error
  }
}

/**
 * Update tenant information
 *
 * @param {string} tenantId - Tenant ID
 * @param {Object} updates - Updated fields
 */
export const updateTenant = async (tenantId, updates) => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    const tenantRef = doc(db, 'tenants', tenantId)
    await updateDoc(tenantRef, {
      ...updates,
      updatedAt: serverTimestamp(),
    })

    console.log('✅ Tenant updated:', tenantId)
    return { success: true }
  } catch (error) {
    console.error('Update tenant error:', error)
    throw error
  }
}

/**
 * Regenerate Embedded Key
 *
 * @param {string} tenantId - tenant ID
 * @returns {Promise<Object>} { success: true, embedKey }
 */
export const regenerateEmbedKey = async tenantId => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    const newEmbedKey = `embed_${generateSecureKey()}`

    await updateDoc(doc(db, 'tenants', tenantId), {
      embedKey: newEmbedKey,
      updatedAt: serverTimestamp(),
    })

    console.log('✅ Embed key regenerated:', tenantId)
    return { success: true, embedKey: newEmbedKey }
  } catch (error) {
    console.error('Key regeneration error:', error)
    throw error
  }
}

/**
 * Check if the user is an expert
 *
 * @returns {Promise<boolean>}
 */
export const checkIsExpert = async () => {
  try {
    const user = auth.currentUser
    if (!user) return false

    const userDoc = await getDoc(doc(db, 'users', user.uid))
    if (!userDoc.exists()) return false

    const userData = userDoc.data()
    return userData.roles && userData.roles.includes('expert')
  } catch (error) {
    console.error('Check expert status error:', error)
    return false
  }
}

/**
 * Upgrade user to expert
 *
 * @returns {Promise<Object>} { success: true }
 */
export const upgradeToExpert = async () => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    const userRef = doc(db, 'users', user.uid)
    const userDoc = await getDoc(userRef)

    if (!userDoc.exists()) {
      throw new Error('User does not exist.')
    }

    const userData = userDoc.data()

    // Check if you are already an expert
    if (userData.roles && userData.roles.includes('expert')) {
      return { success: true, message: 'Already an expert' }
    }

    // Add expert role
    const currentRoles = userData.roles || ['client']
    await updateDoc(userRef, {
      roles: [...currentRoles, 'expert'],
      expertProfile: {
        tenantId: null,
        displayName: userData.username || userData.displayName,
        isApproved: true,
        createdAt: serverTimestamp(),
      },
    })

    console.log('✅ User upgraded to expert:', user.uid)
    return { success: true, message: 'Upgraded to expert' }
  } catch (error) {
    console.error('Upgrade Expert Error:', error)
    throw error
  }
}

// ============= Organization member management functions (add to firebase.js)=============

/**
 * Generate random tokens
 */
const generateToken = (prefix = 'inv') => {
  const characters =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = `${prefix}_`
  for (let i = 0; i < 32; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length))
  }
  return result
}

/**
 * Generate invitation link
 *
 * @param {Object} options - Invitation link option
 * @param {number} options.maxUses - Maximum number of uses (1 = single use, -1 = unlimited uses)
 * @param {number} options.expiresInDays - Validity period (in days)
 * @returns {Promise<Object>} { success: true, token, inviteLink }
 */
export const generateInviteLink = async ({
  maxUses = 1,
  expiresInDays = 7,
  inviteEmail = null,
}) => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    // Get the current user's tenant
    const tenant = await getMyTenant()
    if (!tenant) throw new Error('No tenant found')

    // Check if the user is the owner
    const member = tenant.members?.find(m => m.userId === user.uid)
    if (!member || member.role !== 'owner') {
      throw new Error('Only owners can generate invite links')
    }

    // generate token
    const token = generateToken('inv')

    // Calculate expiration time
    const expiresAt = new Date()
    expiresAt.setDate(expiresAt.getDate() + expiresInDays)

    // Create an invitation link object
    const inviteLink = {
      token: token,
      tenantId: tenant.id,
      createdBy: user.uid,
      createdAt: new Date().toISOString(),
      expiresAt: expiresAt.toISOString(),
      expiresInDays: expiresInDays,
      isActive: true,
      maxUses: maxUses, // 1 = one time, -1 = an infinite number of times
      usedCount: 0,
      usedBy: [],
      inviteEmail: inviteEmail ? inviteEmail.toLowerCase() : null, // ✅ Added: Invitation Email
    }

    // Get the current inviteLinks array
    const currentInviteLinks = tenant.inviteLinks || []

    // Add new link
    const tenantRef = doc(db, 'tenants', tenant.id)
    await updateDoc(tenantRef, {
      inviteLinks: [...currentInviteLinks, inviteLink],
      updatedAt: serverTimestamp(),
    })

    // Generate complete invitation link URL
    const baseUrl = window.location.origin
    const fullInviteLink = `${baseUrl}/invite/${token}`

    console.log('✅ Invite link generated:', token)
    return {
      success: true,
      token,
      inviteLink: fullInviteLink,
      expiresAt: expiresAt.toISOString(),
      maxUses,
    }
  } catch (error) {
    console.error('Invitation link generated incorrect:', error)
    throw error
  }
}

/**
 * Get invitation link information
 *
 * @param {string} token - Invitation token
 * @returns {Promise<Object>} Invitation link information
 */
export const getInviteLink = async token => {
  try {
    // Query all tenants and find the tenant that contains this token.
    const tenantsRef = collection(db, 'tenants')
    const tenantsSnapshot = await getDocs(tenantsRef)

    for (const tenantDoc of tenantsSnapshot.docs) {
      const tenantData = tenantDoc.data()
      const inviteLinks = tenantData.inviteLinks || []

      const inviteLink = inviteLinks.find(link => link.token === token)

      if (inviteLink) {
        // Check if the link is valid.
        const now = new Date()
        const expiresAt = new Date(inviteLink.expiresAt)

        return {
          ...inviteLink,
          tenantId: tenantDoc.id,
          tenantName: tenantData.displayName,
          isExpired: now > expiresAt,
          isMaxUsesReached:
            inviteLink.maxUses !== -1 &&
            inviteLink.usedCount >= inviteLink.maxUses,
        }
      }
    }

    throw new Error('Invite link not found')
  } catch (error) {
    console.error('Invitation link error:', error)
    throw error
  }
}

/**
 * @param {string} token - Invitation token
 * @returns {Promise<Object>} { success: true, tenantId: string }
 */
export const acceptInvite = async token => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    // Get invitation link information
    const inviteInfo = await getInviteLink(token)

    // ✅ Added: Verify invitation email address
    if (inviteInfo.inviteEmail) {
      const userEmail = user.email.toLowerCase()
      const inviteEmail = inviteInfo.inviteEmail.toLowerCase()

      if (userEmail !== inviteEmail) {
        throw new Error(
          `This invitation is for ${inviteInfo.inviteEmail}. ` +
            `You are logged in as ${user.email}. ` +
            `Please log in with the correct account or contact the organization owner.`
        )
      }

      console.log('✅ Email verification passed:', userEmail)
    }

    // Verify invitation link
    if (!inviteInfo.isActive) {
      throw new Error('This invite link has been revoked')
    }

    if (inviteInfo.isExpired) {
      throw new Error('This invite link has expired')
    }

    if (inviteInfo.isMaxUsesReached) {
      throw new Error('This invite link has reached its maximum number of uses')
    }

    // Check if the user is already in this tenant.
    const tenantRef = doc(db, 'tenants', inviteInfo.tenantId)
    const tenantDoc = await getDoc(tenantRef)

    if (!tenantDoc.exists()) {
      throw new Error('Organization not found')
    }

    const tenantData = tenantDoc.data()

    const existingMember = tenantData.members?.find(m => m.userId === user.uid)
    if (existingMember) {
      throw new Error('You are already a member of this organization')
    }

    // Obtaining user information
    const userRef = doc(db, 'users', user.uid)
    const userDoc = await getDoc(userRef)

    if (!userDoc.exists()) {
      throw new Error('User document not found')
    }

    const userData = userDoc.data()

    // ✅ Added: Check if the user has joined another organization.
    if (
      userData.joinedOrganization &&
      userData.joinedOrganization !== inviteInfo.tenantId
    ) {
      throw new Error(
        'You are already a member of another organization. Please leave your current organization first.'
      )
    }

    // Add users to tenant members
    const newMember = {
      userId: user.uid,
      email: user.email,
      username: userData.username || user.email.split('@')[0],
      role: 'member',
      joinedAt: new Date().toISOString(),
    }

    const updatedMembers = [...(tenantData.members || []), newMember]

    // Update the number of times the invitation link has been used.
    const updatedInviteLinks = tenantData.inviteLinks.map(link => {
      if (link.token === token) {
        return {
          ...link,
          usedCount: link.usedCount + 1,
          usedBy: [
            ...(link.usedBy || []),
            { userId: user.uid, usedAt: new Date().toISOString() },
          ],
        }
      }
      return link
    })

    // Update tenant document
    await updateDoc(tenantRef, {
      members: updatedMembers,
      inviteLinks: updatedInviteLinks,
      updatedAt: serverTimestamp(),
    })

    // ✅ Fix: Instead of overwriting tenantId, set joinedOrganization.
    await updateDoc(userRef, {
      joinedOrganization: inviteInfo.tenantId, // ✅
      joinedAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
    })

    // ✅ Added: Update the organization field for all frameworks of the user.
    const frameworksQuery = query(
      collection(db, 'frameworks'),
      where('creatorId', '==', user.uid),
      where('tenantId', '==', userData.tenantId)
    )

    const frameworksSnapshot = await getDocs(frameworksQuery)

    const updatePromises = frameworksSnapshot.docs.map(docSnapshot => {
      return updateDoc(doc(db, 'frameworks', docSnapshot.id), {
        organization: inviteInfo.tenantId, // Updated to a new organization
        updatedAt: serverTimestamp(),
      })
    })

    await Promise.all(updatePromises)

    console.log('✅ User joined organization:', inviteInfo.tenantId)
    console.log(`✅ Updated ${frameworksSnapshot.size} frameworks`)

    return {
      success: true,
      tenantId: inviteInfo.tenantId,
      frameworksUpdated: frameworksSnapshot.size,
    }
  } catch (error) {
    console.error('Invitation accepted incorrectly:', error)
    throw error
  }
}

/**
 * Leave the organization - New function
 *
 * ✅ Function:
 * - Remove user from organization member list
 * - Clear the user's joinedOrganization field
 * - Restore the organization of all user frameworks to their own tenantId.
 * - Cancel the publishedToOrganization status for all frameworks.
 *
 * @param {string} organizationId - Organization ID to leave
 * @returns {Promise<Object>} { success: true }
 */
export const leaveOrganization = async organizationId => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    // Obtaining user information
    const userRef = doc(db, 'users', user.uid)
    const userDoc = await getDoc(userRef)

    if (!userDoc.exists()) {
      throw new Error('User document not found')
    }

    const userData = userDoc.data()

    // Verify if the user is in the organization
    if (userData.joinedOrganization !== organizationId) {
      throw new Error('You are not a member of this organization')
    }

    // Obtain organizational information
    const tenantRef = doc(db, 'tenants', organizationId)
    const tenantDoc = await getDoc(tenantRef)

    if (!tenantDoc.exists()) {
      throw new Error('Organization not found')
    }

    const tenantData = tenantDoc.data()

    // Remove user from member list
    const updatedMembers = (tenantData.members || []).filter(
      m => m.userId !== user.uid
    )

    // Update organization document
    await updateDoc(tenantRef, {
      members: updatedMembers,
      updatedAt: serverTimestamp(),
    })

    // Clear the user's joinedOrganization field
    await updateDoc(userRef, {
      joinedOrganization: null,
      leftOrganizationAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
    })

    // Update all user frameworks: Restore to your own organization, cancel publish status.
    const frameworksQuery = query(
      collection(db, 'frameworks'),
      where('creatorId', '==', user.uid),
      where('organization', '==', organizationId)
    )

    const frameworksSnapshot = await getDocs(frameworksQuery)

    const updatePromises = frameworksSnapshot.docs.map(docSnapshot => {
      return updateDoc(doc(db, 'frameworks', docSnapshot.id), {
        organization: userData.tenantId, // Restore to its own tenant
        publishedToOrganization: false, // Cancel release
        updatedAt: serverTimestamp(),
      })
    })

    await Promise.all(updatePromises)

    console.log('✅ User left organization:', organizationId)
    console.log(`✅ Restored ${frameworksSnapshot.size} frameworks`)

    return {
      success: true,
      frameworksRestored: frameworksSnapshot.size,
    }
  } catch (error) {
    console.error('Error leaving organization:', error)
    throw error
  }
}

/**
 * Deploying the framework to the organization - Adding functions
 *
 * @param {string} frameworkId - Frame ID
 * @returns {Promise<Object>} { success: true }
 */
export const publishFrameworkToOrganization = async frameworkId => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    // Get user data
    const userRef = doc(db, 'users', user.uid)
    const userDoc = await getDoc(userRef)

    if (!userDoc.exists()) {
      throw new Error('User not found')
    }

    const userData = userDoc.data()

    // Check if the user has joined an organization
    if (!userData.joinedOrganization) {
      throw new Error('You are not a member of any organization')
    }

    // ✅ Get Organization ID
    const organizationId = userData.joinedOrganization

    // Get the framework
    const frameworkRef = doc(db, 'frameworks', frameworkId)
    const frameworkDoc = await getDoc(frameworkRef)

    if (!frameworkDoc.exists()) {
      throw new Error('Framework not found')
    }

    const frameworkData = frameworkDoc.data()

    // Verify framework ownership
    if (frameworkData.creatorId !== user.uid) {
      throw new Error('You can only publish your own frameworks')
    }

    // ✅ Core fix: Added organization field
    await updateDoc(frameworkRef, {
      organization: organizationId, // ✅
      publishedToOrganization: true,
      publishedAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
    })

    console.log(
      '✅ Framework published to organization:',
      frameworkId,
      'org:',
      organizationId
    )

    // ✅ Return organization ID
    return {
      success: true,
      organizationId: organizationId,
    }
  } catch (error) {
    console.error('Framework deployment error:', error)
    throw error
  }
}
/**
 * Cancel Release Framework - Add Function
 *
 * @param {string} frameworkId - Frame ID
 * @returns {Promise<Object>} { success: true }
 */
export const unpublishFrameworkFromOrganization = async frameworkId => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    const frameworkRef = doc(db, 'frameworks', frameworkId)
    const frameworkDoc = await getDoc(frameworkRef)

    if (!frameworkDoc.exists()) {
      throw new Error('Framework not found')
    }

    const frameworkData = frameworkDoc.data()

    if (frameworkData.creatorId !== user.uid) {
      throw new Error('You can only unpublish your own frameworks')
    }

    // ✅ Core fix: Clear the organization field
    await updateDoc(frameworkRef, {
      organization: null, // ✅
      publishedToOrganization: false,
      unpublishedAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
    })

    console.log('✅ Framework unpublished from organization:', frameworkId)
    return { success: true }
  } catch (error) {
    console.error('Cancel release framework error:', error)
    throw error
  }
}

/**
 * Get all shared frames in the organization - New function
 *
 * @param {string} organizationId - Organization ID
 * @returns {Promise<Array>} Frame list
 */
export const getOrganizationFrameworks = async organizationId => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    // Query all frameworks published to this organization
    const q = query(
      collection(db, 'frameworks'),
      where('organization', '==', organizationId),
      where('publishedToOrganization', '==', true),
      orderBy('updatedAt', 'desc')
    )

    const snapshot = await getDocs(q)

    const frameworks = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
    }))

    console.log(`✅ Found ${frameworks.length} organization frameworks`)
    return frameworks
  } catch (error) {
    console.error('Error retrieving organizational framework:', error)
    throw error
  }
}

/**
 * Cancel Invitation Link
 */
export const revokeInviteLink = async token => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    const userRef = doc(db, 'users', user.uid)
    const userDoc = await getDoc(userRef)
    const userData = userDoc.data()
    const tenantId = userData.tenantId

    if (!tenantId) {
      throw new Error('User does not have a tenant')
    }

    const tenantRef = doc(db, 'tenants', tenantId)
    const tenantDoc = await getDoc(tenantRef)

    if (!tenantDoc.exists()) {
      throw new Error('Tenant not found')
    }

    const tenantData = tenantDoc.data()

    const isOwner = tenantData.members?.some(
      m => m.userId === user.uid && m.role === 'owner'
    )

    if (!isOwner) {
      throw new Error('Only tenant owner can revoke invite links')
    }

    const updatedInviteLinks = (tenantData.inviteLinks || []).map(link => {
      if (link.token === token) {
        return {
          ...link,
          isActive: false,
          revokedAt: new Date().toISOString(),
          revokedBy: user.uid,
        }
      }
      return link
    })

    await updateDoc(tenantRef, {
      inviteLinks: updatedInviteLinks,
      updatedAt: serverTimestamp(),
    })

    console.log('✅ Invite link revoked:', token)
    return { success: true }
  } catch (error) {
    console.error('Revoke invite link error:', error)
    throw error
  }
}

/**
 * Remove member
 */
export const removeMember = async (tenantId, userId) => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    const tenantRef = doc(db, 'tenants', tenantId)
    const tenantDoc = await getDoc(tenantRef)

    if (!tenantDoc.exists()) {
      throw new Error('Tenant not found')
    }

    const tenantData = tenantDoc.data()

    const isOwner = tenantData.members?.some(
      m => m.userId === user.uid && m.role === 'owner'
    )

    if (!isOwner) {
      throw new Error('Only tenant owner can remove members')
    }

    const memberToRemove = tenantData.members?.find(m => m.userId === userId)
    if (memberToRemove?.role === 'owner') {
      throw new Error('Cannot remove the tenant owner')
    }

    const updatedMembers = (tenantData.members || []).filter(
      m => m.userId !== userId
    )

    await updateDoc(tenantRef, {
      members: updatedMembers,
      updatedAt: serverTimestamp(),
    })

    const removedUserRef = doc(db, 'users', userId)
    await updateDoc(removedUserRef, {
      joinedOrganization: null,
      leftOrganizationAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
    })

    const frameworksQuery = query(
      collection(db, 'frameworks'),
      where('creatorId', '==', userId),
      where('organization', '==', tenantId),
      where('publishedToOrganization', '==', true)
    )

    const frameworksSnapshot = await getDocs(frameworksQuery)

    const updatePromises = frameworksSnapshot.docs.map(docSnapshot => {
      return updateDoc(doc(db, 'frameworks', docSnapshot.id), {
        publishedToOrganization: false,
        unpublishedAt: serverTimestamp(),
        updatedAt: serverTimestamp(),
      })
    })

    await Promise.all(updatePromises)

    console.log('✅ Member removed:', userId)
    console.log(`✅ Unpublished ${frameworksSnapshot.size} frameworks`)

    return {
      success: true,
      unpublishedCount: frameworksSnapshot.size,
    }
  } catch (error) {
    console.error('Remove member error:', error)
    throw error
  }
}

/**
 * Get tenant member list
 */
export const getTenantMembers = async tenantId => {
  try {
    const user = auth.currentUser
    if (!user) throw new Error('User not logged in')

    const tenantRef = doc(db, 'tenants', tenantId)
    const tenantDoc = await getDoc(tenantRef)

    if (!tenantDoc.exists()) {
      throw new Error('Tenant not found')
    }

    const tenantData = tenantDoc.data()
    const members = tenantData.members || []

    const membersWithDetails = await Promise.all(
      members.map(async member => {
        try {
          const userRef = doc(db, 'users', member.userId)
          const userDoc = await getDoc(userRef)

          if (userDoc.exists()) {
            const userData = userDoc.data()
            return {
              userId: member.userId,
              email: userData.email || member.email,
              username:
                userData.username ||
                member.username ||
                userData.email?.split('@')[0] ||
                'Unknown',
              role: member.role || 'member',
              joinedAt: member.joinedAt,
            }
          }

          return {
            userId: member.userId,
            email: member.email || 'Unknown',
            username:
              member.username || member.email?.split('@')[0] || 'Unknown',
            role: member.role || 'member',
            joinedAt: member.joinedAt,
          }
        } catch (error) {
          console.error(`Error fetching member ${member.userId}:`, error)
          return {
            userId: member.userId,
            email: member.email || 'Unknown',
            username: member.username || 'Unknown',
            role: member.role || 'member',
            joinedAt: member.joinedAt,
          }
        }
      })
    )

    console.log(
      `✅ Fetched ${membersWithDetails.length} members for tenant ${tenantId}`
    )
    return membersWithDetails
  } catch (error) {
    console.error('Get tenant members error:', error)
    throw error
  }
}

// ============================================
// Admin whitelisst function
// ============================================

//ADMIN EMAIL
const SUPER_ADMIN_EMAIL = 'webmaster@valorie.ai'

/**
 *check current user is admin or not
 * @returns {boolean}
 */
export const isSuperAdmin = () => {
  const user = auth.currentUser
  return user?.email === SUPER_ADMIN_EMAIL
}

/**
 * get all whitelist domain
 * @returns {Promise<Array>} domain list
 */
export const getWhitelistDomains = async () => {
  try {
    const user = auth.currentUser
    if (!user || user.email !== SUPER_ADMIN_EMAIL) {
      throw new Error('Unauthorized: Admin access required')
    }

    const configRef = doc(db, 'config', 'whitelist')
    const configDoc = await getDoc(configRef)

    if (configDoc.exists()) {
      const data = configDoc.data()
      return data.domains || []
    }

    // 如果不存在，创建初始配置
    const initialDomains = ['ad.unsw.edu.au', 'valorie.ai']
    await setDoc(configRef, {
      domains: initialDomains,
      updatedAt: serverTimestamp(),
      updatedBy: user.uid,
    })

    return initialDomains
  } catch (error) {
    console.error('获取白名单域名错误:', error)
    throw error
  }
}

/**
 * add whitelist domain
 * @param {string} domain - domain name(with out @)
 * @returns {Promise<Object>}
 */
export const addWhitelistDomain = async domain => {
  try {
    const user = auth.currentUser
    if (!user || user.email !== SUPER_ADMIN_EMAIL) {
      throw new Error('Unauthorized: Admin access required')
    }

    // clear the domain name
    const cleanDomain = domain.replace('@', '').trim().toLowerCase()

    if (!cleanDomain) {
      throw new Error('Invalid domain')
    }

    const configRef = doc(db, 'config', 'whitelist')
    const configDoc = await getDoc(configRef)

    let currentDomains = []
    if (configDoc.exists()) {
      currentDomains = configDoc.data().domains || []
    }

    // check is exits or not
    if (currentDomains.includes(cleanDomain)) {
      throw new Error('Domain already exists in whitelist')
    }

    // add new domain name
    const updatedDomains = [...currentDomains, cleanDomain]

    await setDoc(configRef, {
      domains: updatedDomains,
      updatedAt: serverTimestamp(),
      updatedBy: user.uid,
    })

    console.log('✅ Domain added to whitelist:', cleanDomain)
    return { success: true, domain: cleanDomain }
  } catch (error) {
    console.error('add domain in whitelist error:', error)
    throw error
  }
}

/**
 * remove domain in whitelist
 * @param {string} domain - domain name
 * @returns {Promise<Object>}
 */
export const removeWhitelistDomain = async domain => {
  try {
    const user = auth.currentUser
    if (!user || user.email !== SUPER_ADMIN_EMAIL) {
      throw new Error('Unauthorized: Admin access required')
    }

    const configRef = doc(db, 'config', 'whitelist')
    const configDoc = await getDoc(configRef)

    if (!configDoc.exists()) {
      throw new Error('Whitelist configuration not found')
    }

    const currentDomains = configDoc.data().domains || []
    const updatedDomains = currentDomains.filter(d => d !== domain)

    await setDoc(configRef, {
      domains: updatedDomains,
      updatedAt: serverTimestamp(),
      updatedBy: user.uid,
    })

    console.log('✅ Domain removed from whitelist:', domain)
    return { success: true, domain }
  } catch (error) {
    console.error('remove domain name in whitelist error:', error)
    throw error
  }
}

/**
 * check the email in whitelist or not
 * @param {string} email - email address
 * @returns {Promise<boolean>}
 */
export const checkEmailDomainWhitelisted = async email => {
  try {
    const domain = email.split('@')[1]?.toLowerCase()
    if (!domain) return false

    const configRef = doc(db, 'config', 'whitelist')
    const configDoc = await getDoc(configRef)

    if (!configDoc.exists()) {
      // if didn't exit, use deault
      return domain === 'ad.unsw.edu.au'
    }

    const whitelistDomains = configDoc.data().domains || []
    return whitelistDomains.includes(domain)
  } catch (error) {
    console.error('check email whitelist error:', error)
    // if error, return false as safty reason
    return false
  }
}

/**
 * get all user( admin sue only)
 * @returns {Promise<Array>}
 */
export const getAllUsers = async () => {
  try {
    const user = auth.currentUser
    if (!user || user.email !== SUPER_ADMIN_EMAIL) {
      throw new Error('Unauthorized: Admin access required')
    }

    const usersQuery = query(
      collection(db, 'users'),
      orderBy('createdAt', 'desc')
    )

    const snapshot = await getDocs(usersQuery)

    const users = snapshot.docs.map(doc => ({
      uid: doc.id,
      ...doc.data(),
      //make sure isBlock exits
      isBlocked: doc.data().isBlocked || false,
    }))

    console.log(`✅ Fetched ${users.length} users`)
    return users
  } catch (error) {
    console.error('get user list error:', error)
    throw error
  }
}

/**
 * Block user
 * @param {string} userId - user ID
 * @returns {Promise<Object>}
 */
export const blockUser = async userId => {
  try {
    const user = auth.currentUser
    if (!user || user.email !== SUPER_ADMIN_EMAIL) {
      throw new Error('Unauthorized: Admin access required')
    }

    const userRef = doc(db, 'users', userId)
    await updateDoc(userRef, {
      isBlocked: true,
      blockedAt: serverTimestamp(),
      blockedBy: user.uid,
    })

    console.log('✅ User blocked:', userId)
    return { success: true, userId }
  } catch (error) {
    console.error('Block user error:', error)
    throw error
  }
}

/**
 * Unblock user
 * @param {string} userId - user ID
 * @returns {Promise<Object>}
 */
export const unblockUser = async userId => {
  try {
    const user = auth.currentUser
    if (!user || user.email !== SUPER_ADMIN_EMAIL) {
      throw new Error('Unauthorized: Admin access required')
    }

    const userRef = doc(db, 'users', userId)
    await updateDoc(userRef, {
      isBlocked: false,
      unblockedAt: serverTimestamp(),
      unblockedBy: user.uid,
    })

    console.log('✅ User unblocked:', userId)
    return { success: true, userId }
  } catch (error) {
    console.error('Unblock user error:', error)
    throw error
  }
}

/**
 * check user is block or not
 * @param {string} userId - user ID
 * @returns {Promise<boolean>}
 */
export const checkUserBlocked = async userId => {
  try {
    const userRef = doc(db, 'users', userId)
    const userDoc = await getDoc(userRef)

    if (!userDoc.exists()) {
      return false
    }

    return userDoc.data().isBlocked || false
  } catch (error) {
    console.error('check user block state error:', error)
    return false
  }
}

// expor firebase.js to default export

export default {
  auth,
  db,
  registerUser,
  loginUser,
  logoutUser,
  checkEmailExists,
  checkUsernameExists,
  onAuthChange,
  createFramework,
  getMyFrameworks,
  getFramework,
  updateFramework,
  deleteFramework,
  onFrameworksChange,
  createTenant,
  getMyTenant,
  updateTenant,
  regenerateEmbedKey,
  checkIsExpert,
  upgradeToExpert,
  generateInviteLink,
  getInviteLink,
  acceptInvite,
  revokeInviteLink,
  removeMember,
  getTenantMembers,
  isSuperAdmin,
  getWhitelistDomains,
  addWhitelistDomain,
  removeWhitelistDomain,
  checkEmailDomainWhitelisted,
  getAllUsers,
  blockUser,
  unblockUser,
  checkUserBlocked,
}
