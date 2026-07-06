import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import PrivateRoute from './components/PrivateRoute'
import Navbar from './components/Navbar'
import Login from './components/Login'
import YourFrameworks from './components/YourFrameworks'
import CreateFramework from './components/CreateFramework'
import FrameworkEditor from './components/FrameworkEditor'
import Library from './components/Library'
import AdminPanel from './components/AdminPanel'

/**
 * RootRedirect - root path redirection component.
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

  return <Navigate to="/frameworks" replace />
}

function AppContent() {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/admin"
          element={
            <PrivateRoute>
              <AdminPanel />
            </PrivateRoute>
          }
        />
        <Route
          path="/library"
          element={
            <PrivateRoute>
              <Library />
            </PrivateRoute>
          }
        />

        <Route
          path="/frameworks"
          element={
            <PrivateRoute>
              <YourFrameworks />
            </PrivateRoute>
          }
        />
        <Route
          path="/frameworks/create"
          element={
            <PrivateRoute>
              <CreateFramework />
            </PrivateRoute>
          }
        />
        <Route
          path="/frameworks/:id"
          element={
            <PrivateRoute>
              <FrameworkEditor />
            </PrivateRoute>
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
