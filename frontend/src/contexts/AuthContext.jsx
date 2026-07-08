/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useState } from 'react'
import {
  getCurrentBackendUser,
  loginWithBackend,
  logoutWithBackend,
} from '../lib/api'

const AuthContext = createContext()

function buildBackendUser(backendUser, existingUser = {}) {
  const email = backendUser?.email || existingUser?.email

  return {
    uid: backendUser?.id || existingUser?.uid,
    id: backendUser?.id || existingUser?.id,
    backendUserId: backendUser?.id || existingUser?.backendUserId,
    email,
    username:
      backendUser?.username ||
      existingUser?.username ||
      email?.split('@')[0] ||
      'user',
    isSuperAdmin: Boolean(backendUser?.is_super_admin),
    authProvider: 'backend-cookie',
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
    let cancelled = false

    const restoreSession = async () => {
      try {
        const backendUser = await getCurrentBackendUser({
          suppressAuthRedirect: true,
        })

        if (!cancelled) {
          setUser(currentUser => buildBackendUser(backendUser, currentUser))
        }
      } catch {
        if (!cancelled) setUser(null)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    restoreSession()

    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    const handleUnauthorized = () => {
      setUser(null)
    }

    window.addEventListener('auth:unauthorized', handleUnauthorized)
    return () => {
      window.removeEventListener('auth:unauthorized', handleUnauthorized)
    }
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
      const nextUser = buildBackendUser(backendAuth.user)
      setUser(nextUser)

      return { success: true, user: nextUser }
    } catch (error) {
      console.error('Login failed:', error)

      let errorMessage = 'Login failed, please check your account and password'

      if (error.status === 401) {
        errorMessage = 'wrong email or password'
      } else if (error.status === 403) {
        errorMessage =
          'Your account has been blocked. Please contact the administrator.'
      }

      setUser(null)
      return { success: false, error: errorMessage }
    }
  }

  const logout = async () => {
    try {
      await logoutWithBackend()
      return { success: true }
    } catch (error) {
      console.error('Logout failed:', error)
      return { success: false, error: 'Logout failed, please try again.' }
    } finally {
      setUser(null)
    }
  }

  const refreshUser = async () => {
    if (!user) {
      throw new Error('No user logged in')
    }

    const backendUser = await getCurrentBackendUser()
    setUser(currentUser => buildBackendUser(backendUser, currentUser))
  }

  const value = {
    user,
    loading,
    signup,
    login,
    logout,
    refreshUser,
    isAuthenticated: !!user,
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

export default AuthContext
