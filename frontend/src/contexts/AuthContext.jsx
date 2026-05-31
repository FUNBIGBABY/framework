/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, useEffect } from 'react'
import {
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut,
} from 'firebase/auth'
import {
  doc,
  getDoc,
  setDoc,
  updateDoc,
  serverTimestamp,
} from 'firebase/firestore'
import { auth, db } from '../lib/firebase'
import { loginWithBackend } from '../lib/api'

const AuthContext = createContext()

function buildBackendUser(backendUser, fallbackEmail) {
  const email = backendUser?.email || fallbackEmail

  return {
    uid: backendUser?.id,
    id: backendUser?.id,
    backendUserId: backendUser?.id,
    email,
    username: backendUser?.username || email?.split('@')[0] || 'user',
    tenantId: null,
    joinedOrganization: null,
    roles: [],
    expertProfile: null,
    authProvider: 'backend-jwt',
  }
}

function getStoredBackendUser() {
  const token = localStorage.getItem('access_token')
  const rawUser = localStorage.getItem('user')

  if (!token || !rawUser) return null

  try {
    return JSON.parse(rawUser)
  } catch {
    localStorage.removeItem('user')
    return null
  }
}

function saveBackendSession(authData, fallbackEmail) {
  const backendUser = buildBackendUser(authData.user, fallbackEmail)

  localStorage.setItem('access_token', authData.access_token)
  localStorage.setItem('user', JSON.stringify(backendUser))

  return backendUser
}

function clearBackendSession() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
}

function buildFirebaseCompatibleUser(backendUser, firebaseUser, userData = {}) {
  return {
    ...backendUser,
    uid: firebaseUser.uid,
    firebaseUid: firebaseUser.uid,
    email: firebaseUser.email || backendUser.email,
    username:
      userData.username ||
      firebaseUser.displayName ||
      backendUser.username ||
      firebaseUser.email?.split('@')[0],
    tenantId: userData.tenantId || null,
    joinedOrganization: userData.joinedOrganization || null,
    roles: userData.roles || [],
    expertProfile: userData.expertProfile || null,
    createdAt: userData.createdAt || backendUser.createdAt,
    lastLogin: userData.lastLogin || backendUser.lastLogin,
    authProvider: 'backend-jwt+firebase-compat',
  }
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async firebaseUser => {
      const backendUser = getStoredBackendUser()

      if (!backendUser) {
        setUser(null)
        setLoading(false)
        return
      }

      if (firebaseUser) {
        try {
          const userDocRef = doc(db, 'users', firebaseUser.uid)
          const userDoc = await getDoc(userDocRef)

          if (userDoc.exists()) {
            const userData = userDoc.data()

            setUser(
              buildFirebaseCompatibleUser(backendUser, firebaseUser, userData)
            )

            await updateDoc(userDocRef, {
              lastLogin: serverTimestamp(),
            })
          } else {
            console.warn(
              'User document not found in Firestore, creating one...'
            )

            const newUserData = {
              uid: firebaseUser.uid,
              email: firebaseUser.email,
              username:
                firebaseUser.displayName || firebaseUser.email.split('@')[0],
              tenantId: null,
              joinedOrganization: null, // ✅ added
              roles: [],
              expertProfile: null,
              createdAt: serverTimestamp(),
              lastLogin: serverTimestamp(),
            }

            await setDoc(userDocRef, newUserData)

            setUser(
              buildFirebaseCompatibleUser(
                backendUser,
                firebaseUser,
                newUserData
              )
            )
          }
        } catch (error) {
          console.error('Error fetching user data from Firestore:', error)

          setUser(buildFirebaseCompatibleUser(backendUser, firebaseUser))
        }
      } else {
        setUser(backendUser)
      }

      setLoading(false)
    })

    return () => unsubscribe()
  }, [])

  const signup = async () => {
    const error =
      'Public registration is disabled. Accounts are created by an administrator.'
    console.warn(error)
    return { success: false, error }
  }

  const login = async (email, password) => {
    try {
      const backendAuth = await loginWithBackend(email, password)
      const backendUser = saveBackendSession(backendAuth, email)
      let nextUser = backendUser
      let firebaseUser = null

      try {
        const userCredential = await signInWithEmailAndPassword(
          auth,
          email,
          password
        )
        firebaseUser = userCredential.user

        const userDocRef = doc(db, 'users', firebaseUser.uid)
        const userDoc = await getDoc(userDocRef)

        if (userDoc.exists()) {
          const userData = userDoc.data()
          nextUser = buildFirebaseCompatibleUser(
            backendUser,
            firebaseUser,
            userData
          )

          await updateDoc(userDocRef, {
            lastLogin: serverTimestamp(),
          })
        } else {
          console.warn('User document not found, creating one...')

          const newUserData = {
            uid: firebaseUser.uid,
            email: firebaseUser.email,
            username:
              firebaseUser.displayName || firebaseUser.email.split('@')[0],
            tenantId: null,
            joinedOrganization: null, // ✅ added
            roles: [],
            expertProfile: null,
            createdAt: serverTimestamp(),
            lastLogin: serverTimestamp(),
          }

          await setDoc(userDocRef, newUserData)
          nextUser = buildFirebaseCompatibleUser(
            backendUser,
            firebaseUser,
            newUserData
          )
        }
      } catch (firebaseError) {
        console.warn(
          'Firebase login compatibility skipped; backend JWT login succeeded.',
          firebaseError
        )
      }

      setUser(nextUser)
      localStorage.setItem('user', JSON.stringify(nextUser))
      console.log('✅ Backend JWT login successful:', nextUser.backendUserId)

      return { success: true, user: nextUser, firebaseUser }
    } catch (error) {
      console.error('Login failed:', error)
      clearBackendSession()

      let errorMessage = 'Login failed, please check your account and password'

      if (
        error.status === 401 ||
        error.code === 'auth/user-not-found' ||
        error.code === 'auth/wrong-password' ||
        error.code === 'auth/invalid-credential'
      ) {
        errorMessage = 'wrong email or password'
      } else if (error.code === 'auth/invalid-email') {
        errorMessage = 'invalid email'
      } else if (error.code === 'auth/user-disabled') {
        errorMessage = 'account got banned'
      } else if (error.code === 'auth/too-many-requests') {
        errorMessage = 'please try later'
      }

      return { success: false, error: errorMessage }
    }
  }

  const logout = async () => {
    try {
      clearBackendSession()
      await signOut(auth)
      setUser(null)
      console.log('✅ User logged out successfully')
      return { success: true }
    } catch (error) {
      console.error('Logout failed:', error)
      setUser(null)
      return { success: false, error: 'Logout failed, please try again.' }
    }
  }

  const updateUserTenant = async (tenantId, reload = false) => {
    if (!user) {
      throw new Error('No user logged in')
    }

    try {
      const userDocRef = doc(db, 'users', user.uid)

      await updateDoc(userDocRef, {
        tenantId: tenantId,
        roles: user.roles.includes('expert')
          ? user.roles
          : [...user.roles, 'expert'],
        expertProfile: user.expertProfile || {
          displayName: user.username + ' Expert',
          isApproved: true,
        },
        updatedAt: serverTimestamp(),
      })

      setUser({
        ...user,
        tenantId: tenantId,
        roles: user.roles.includes('expert')
          ? user.roles
          : [...user.roles, 'expert'],
        expertProfile: user.expertProfile || {
          displayName: user.username + ' Expert',
          isApproved: true,
        },
      })

      console.log('✅ User tenantId updated:', tenantId)

      if (reload) {
        window.location.reload()
      }
    } catch (error) {
      console.error('Error updating user tenantId:', error)
      throw error
    }
  }

  // ✅ Added: Refresh user data
  const refreshUser = async () => {
    if (!user) {
      throw new Error('No user logged in')
    }

    try {
      const userDocRef = doc(db, 'users', user.uid)
      const userDoc = await getDoc(userDocRef)

      if (userDoc.exists()) {
        const userData = userDoc.data()

        setUser({
          ...user,
          tenantId: userData.tenantId || null,
          joinedOrganization: userData.joinedOrganization || null,
          roles: userData.roles || [],
          expertProfile: userData.expertProfile || null,
        })

        console.log('✅ User data refreshed')
      }
    } catch (error) {
      console.error('Error refreshing user data:', error)
      throw error
    }
  }

  const value = {
    user,
    loading,
    signup,
    login,
    logout,
    updateUserTenant,
    refreshUser, // ✅ added method
    isAuthenticated: !!user,
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

export default AuthContext
