import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import PrivateRoute from './components/PrivateRoute'
import TenantRoute from './components/TenantRoute'
import Navbar from './components/Navbar'
import Login from './components/Login'
import YourFrameworks from './components/YourFrameworks'
import CreateFramework from './components/CreateFramework'
import FrameworkEditor from './components/FrameworkEditor'
import Library from './components/Library'
import MigrationTool from './components/MigrationTool'
import TenantSettings from './components/TenantSettings'
import InviteAccept from './components/InviteAccept'
import YourOrganization from './components/YourOrganization'
import AdminPanel from './components/AdminPanel'

const PERSONAL_ROUTE_TENANT = 'personal'

/**
 * RootRedirect - root path redirection component.
 * The tenant path segment is a legacy UI routing shim during Phase 6.
 */
function RootRedirect() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  const routeTenant = user.tenantId || PERSONAL_ROUTE_TENANT
  return <Navigate to={`/${routeTenant}/frameworks`} replace />
}

function AppContent() {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/admin" element={<AdminPanel />} />
        <Route
          path="/library"
          element={
            <PrivateRoute>
              <Library />
            </PrivateRoute>
          }
        />
        <Route path="/migrate" element={<MigrationTool />} />
        <Route path="/invite/:token" element={<InviteAccept />} />

        <Route
          path="/:tenantId/frameworks"
          element={
            <TenantRoute>
              <YourFrameworks />
            </TenantRoute>
          }
        />
        <Route
          path="/:tenantId/organization"
          element={
            <TenantRoute>
              <YourOrganization />
            </TenantRoute>
          }
        />
        <Route
          path="/:tenantId/create"
          element={
            <TenantRoute>
              <CreateFramework />
            </TenantRoute>
          }
        />
        <Route
          path="/:tenantId/editor/:id"
          element={
            <TenantRoute>
              <FrameworkEditor />
            </TenantRoute>
          }
        />
        <Route
          path="/:tenantId/settings"
          element={
            <TenantRoute>
              <TenantSettings />
            </TenantRoute>
          }
        />

        <Route path="/" element={<RootRedirect />} />
        <Route
          path="*"
          element={
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
              <div className="text-center">
                <h2 className="text-2xl font-semibold text-gray-800 mb-3">
                  Page Not Found
                </h2>
                <p className="text-gray-600 mb-6">
                  The page you're looking for doesn't exist.
                </p>
                <a
                  href="/"
                  className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Go to Home
                </a>
              </div>
            </div>
          }
        />
      </Routes>
    </>
  )
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  )
}

export default App
