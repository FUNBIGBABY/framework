import { Navigate, useParams, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

/**
 * TenantRoute - Tenant Route Protection Component (Path Mode - Simplified Version)
 *
 * In path-based mode, cross-domain waiting logic is unnecessary because all content resides under the same domain.
 * - The owner can access their tenants.
 * - Members can access the joinedOrganization.
 */
function TenantRoute({ children }) {
  const { user, loading } = useAuth()
  const { tenantId } = useParams()
  const routeTenant = user?.tenantId || 'personal'

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div
            className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"
            aria-label="Loading"
          />
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (!user.tenantId) {
    return children
  }

  // Access control: Users can access their own tenant or the organization they have joined.
  const isOwner = tenantId === user.tenantId
  const isMember = tenantId === user.joinedOrganization
  const hasAccess = isOwner || isMember

  if (!hasAccess) {
    console.error(
      `❌ Access denied:\n` +
        `  - URL tenantId: ${tenantId}\n` +
        `  - User tenantId: ${user.tenantId}\n` +
        `  - User joinedOrganization: ${user.joinedOrganization || 'none'}`
    )

    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="mb-4">
            <svg
              className="mx-auto h-16 w-16 text-red-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Access Denied
          </h2>
          <p className="text-gray-600 mb-6">
            You don&apos;t have access to this organization&apos;s content.
          </p>

          <Link
            to={`/${routeTenant}/frameworks`}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors inline-block"
          >
            Go to Me
          </Link>
        </div>
      </div>
    )
  }

  // All validations passed - Render child component
  return children
}

export default TenantRoute
