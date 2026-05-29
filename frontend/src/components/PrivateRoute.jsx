import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

/**
 * PrivateRoute - Protect routes that require authentication (path pattern - simplified version)
 *
 * In path-based mode, cross-domain waiting logic is unnecessary because all content resides under the same domain.
 */
function PrivateRoute({ children }) {
  const { loading, isAuthenticated } = useAuth()

  // Waiting for authentication status to load
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // Unverified, redirected to the login page
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  // Authenticated, rendering child components
  return children
}

export default PrivateRoute
