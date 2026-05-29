/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, useEffect } from 'react'
import {
  onAuthStateChanged,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  updateProfile,
} from 'firebase/auth'
import {
  doc,
  getDoc,
  setDoc,
  updateDoc,
  serverTimestamp,
} from 'firebase/firestore'
import { auth, db } from '../lib/firebase'

const AuthContext = createContext()

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
      if (firebaseUser) {
        try {
          const userDocRef = doc(db, 'users', firebaseUser.uid)
          const userDoc = await getDoc(userDocRef)

          if (userDoc.exists()) {
            const userData = userDoc.data()

            setUser({
              uid: firebaseUser.uid,
              email: firebaseUser.email,
              username:
                userData.username ||
                firebaseUser.displayName ||
                firebaseUser.email.split('@')[0],
              tenantId: userData.tenantId || null,
              joinedOrganization: userData.joinedOrganization || null, // ✅ added
              roles: userData.roles || [],
              expertProfile: userData.expertProfile || null,
              createdAt: userData.createdAt,
              lastLogin: userData.lastLogin,
            })

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

            setUser({
              uid: firebaseUser.uid,
              email: firebaseUser.email,
              username: newUserData.username,
              tenantId: null,
              joinedOrganization: null, // ✅ added
              roles: [],
              expertProfile: null,
            })
          }
        } catch (error) {
          console.error('Error fetching user data from Firestore:', error)

          setUser({
            uid: firebaseUser.uid,
            email: firebaseUser.email,
            username:
              firebaseUser.displayName || firebaseUser.email.split('@')[0],
            tenantId: null,
            joinedOrganization: null, // ✅ added
            roles: [],
            expertProfile: null,
          })
        }
      } else {
        setUser(null)
      }

      setLoading(false)
    })

    return () => unsubscribe()
  }, [])

  const signup = async (email, password, username) => {
    try {
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        email,
        password
      )
      const firebaseUser = userCredential.user

      await updateProfile(firebaseUser, {
        displayName: username,
      })

      const userDocRef = doc(db, 'users', firebaseUser.uid)
      const newUserData = {
        uid: firebaseUser.uid,
        email: firebaseUser.email,
        username: username,
        tenantId: null,
        joinedOrganization: null, // ✅ added
        roles: [],
        expertProfile: null,
        createdAt: serverTimestamp(),
        lastLogin: serverTimestamp(),
      }

      await setDoc(userDocRef, newUserData)

      console.log('✅ User registered successfully:', firebaseUser.uid)

      setUser({
        uid: firebaseUser.uid,
        email: firebaseUser.email,
        username: username,
        tenantId: null,
        joinedOrganization: null, // ✅ added
        roles: [],
        expertProfile: null,
      })

      return { success: true }
    } catch (error) {
      console.error('Registration failed:', error)

      let errorMessage = 'Registration failed, please try again.'

      if (error.code === 'auth/email-already-in-use') {
        errorMessage = 'This email address has already been registered.'
      } else if (error.code === 'auth/weak-password') {
        errorMessage = 'The password is not strong enough (at least 6 bits).'
      } else if (error.code === 'auth/invalid-email') {
        errorMessage = 'Incorrect email format'
      }

      return { success: false, error: errorMessage }
    }
  }

  const login = async (email, password) => {
    try {
      const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
      )
      const firebaseUser = userCredential.user

      const userDocRef = doc(db, 'users', firebaseUser.uid)
      const userDoc = await getDoc(userDocRef)

      if (userDoc.exists()) {
        const userData = userDoc.data()

        setUser({
          uid: firebaseUser.uid,
          email: firebaseUser.email,
          username:
            userData.username ||
            firebaseUser.displayName ||
            firebaseUser.email.split('@')[0],
          tenantId: userData.tenantId || null,
          joinedOrganization: userData.joinedOrganization || null, // ✅ added
          roles: userData.roles || [],
          expertProfile: userData.expertProfile || null,
        })

        await updateDoc(userDocRef, {
          lastLogin: serverTimestamp(),
        })

        console.log('✅ User logged in successfully:', firebaseUser.uid)
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

        setUser({
          uid: firebaseUser.uid,
          email: firebaseUser.email,
          username: newUserData.username,
          tenantId: null,
          joinedOrganization: null, // ✅ added
          roles: [],
          expertProfile: null,
        })
      }

      return { success: true }
    } catch (error) {
      console.error('Login failed:', error)

      let errorMessage = 'Login failed, please check your account and password'

      if (
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
      await signOut(auth)
      setUser(null)
      console.log('✅ User logged out successfully')
      return { success: true }
    } catch (error) {
      console.error('Logout failed:', error)
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
