import { useNavigate, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { APP_INITIAL, APP_NAME } from '../lib/appConfig'

/**
 * Navbar - Global navigation bar component (path mode)
 *
 * ✅ Retain all original functionality, only modify the path logic.
 * Personal route mode is active for framework navigation.
 */
function Navbar() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout, isAuthenticated } = useAuth()
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [showFrameworksMenu, setShowFrameworksMenu] = useState(false)
  const isAdmin = Boolean(user?.isSuperAdmin)

  const frameworkListPath = '/frameworks'
  const createFrameworkPath = '/frameworks/create'

  const handleCreateClick = () => {
    navigate(createFrameworkPath)
  }

  const handleComingSoon = feature => {
    alert(`${feature} - Coming soon!`)
  }

  // Logout logic - Path pattern
  const handleLogout = () => {
    logout()
    setShowUserMenu(false)
    navigate('/login')
  }

  // Library redirection - path mode (no longer cross-domain)
  const handleLibraryClick = () => {
    navigate('/library')
  }

  const isActive = path => {
    return location.pathname === path || location.pathname.includes(path)
  }

  if (location.pathname === '/login') {
    return null
  }

  if (!isAuthenticated) {
    return null
  }

  const showNavigation = true

  return (
    <nav className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
      <div className="flex items-center justify-between px-4 py-2">
        {/* Left section */}
        <div className="flex items-center space-x-6">
          <button
            className="p-2 hover:bg-gray-100 rounded"
            onClick={() => handleComingSoon('Menu')}
          >
            <svg
              className="w-5 h-5 text-gray-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <rect x="3" y="3" width="4" height="4" />
              <rect x="8" y="3" width="4" height="4" />
              <rect x="13" y="3" width="4" height="4" />
              <rect x="3" y="8" width="4" height="4" />
              <rect x="8" y="8" width="4" height="4" />
              <rect x="13" y="8" width="4" height="4" />
              <rect x="3" y="13" width="4" height="4" />
              <rect x="8" y="13" width="4" height="4" />
              <rect x="13" y="13" width="4" height="4" />
            </svg>
          </button>

          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center">
              <span className="text-white font-bold text-sm">
                {APP_INITIAL}
              </span>
            </div>
            <span className="font-semibold text-gray-800">{APP_NAME}</span>
          </div>

          {showNavigation && (
            <div className="flex items-center space-x-1">
              <button
                onClick={() => navigate(createFrameworkPath)}
                className={`px-3 py-2 rounded font-medium transition-colors ${
                  isActive(createFrameworkPath)
                    ? 'text-blue-600 bg-blue-50 border-b-2 border-blue-600'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                New Framework
              </button>

              {/* Your Frameworks - Drop-down menu */}
              <div className="relative">
                <button
                  onClick={() => setShowFrameworksMenu(!showFrameworksMenu)}
                  onBlur={() =>
                    setTimeout(() => setShowFrameworksMenu(false), 200)
                  }
                  className={`px-3 py-2 rounded font-medium transition-colors flex items-center space-x-1 ${
                    isActive(frameworkListPath)
                      ? 'text-blue-600 bg-blue-50 border-b-2 border-blue-600'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <span>Me</span>
                  <svg
                    className="w-4 h-4"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                      clipRule="evenodd"
                    />
                  </svg>
                </button>

                {showFrameworksMenu && (
                  <div className="absolute left-0 mt-1 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
                    <button
                      onClick={() => {
                        navigate(frameworkListPath)
                        setShowFrameworksMenu(false)
                      }}
                      className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
                    >
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                      </svg>
                      <span>My Drafts</span>
                    </button>
                  </div>
                )}
              </div>

              {/* Library button */}
              <button
                onClick={handleLibraryClick}
                className={`px-3 py-2 rounded font-medium transition-colors ${
                  isActive('/library')
                    ? 'text-blue-600 bg-blue-50 border-b-2 border-blue-600'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                Marketplace
              </button>

              <button
                onClick={() => handleComingSoon('Dashboards')}
                className="px-3 py-2 rounded font-medium text-gray-700 hover:bg-gray-100"
              >
                Dashboards
              </button>
            </div>
          )}
        </div>

        {/* Right section */}
        <div className="flex items-center space-x-3">
          <button
            onClick={handleCreateClick}
            className="px-4 py-2 rounded-lg font-medium transition-colors bg-blue-600 text-white hover:bg-blue-700"
          >
            Create
          </button>

          <div className="relative">
            <input
              type="text"
              placeholder="Search"
              className="w-64 pl-9 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              onFocus={() => handleComingSoon('Search')}
            />
            <svg
              className="w-4 h-4 text-gray-400 absolute left-3 top-2.5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                clipRule="evenodd"
              />
            </svg>
          </div>

          <button
            className="p-2 hover:bg-gray-100 rounded"
            onClick={() => handleComingSoon('Help')}
          >
            <svg
              className="w-5 h-5 text-gray-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z"
                clipRule="evenodd"
              />
            </svg>
          </button>

          <button
            className="p-2 hover:bg-gray-100 rounded"
            onClick={() => handleComingSoon('Settings')}
          >
            <svg
              className="w-5 h-5 text-gray-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                clipRule="evenodd"
              />
            </svg>
          </button>

          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center hover:ring-2 hover:ring-gray-300 focus:outline-none"
            >
              <span className="text-white font-medium text-sm">
                {user?.username?.[0]?.toUpperCase() || 'U'}
              </span>
            </button>

            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
                <div className="px-4 py-3 border-b border-gray-100">
                  <p className="text-sm font-medium text-gray-900">
                    {user?.username}
                  </p>
                  <p className="text-xs text-gray-500 truncate">
                    {user?.email}
                  </p>
                </div>

                {showNavigation && (
                  <>
                    <button
                      onClick={() => {
                        setShowUserMenu(false)
                        navigate(frameworkListPath)
                      }}
                      className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
                    >
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                      </svg>
                      <span>My Drafts</span>
                    </button>

                    {/* Library link */}
                    <button
                      onClick={() => {
                        setShowUserMenu(false)
                        handleLibraryClick()
                      }}
                      className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
                    >
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"
                        />
                      </svg>
                      <span>Marketplace</span>
                    </button>
                    <div className="border-t border-gray-100 my-1"></div>
                  </>
                )}

                {/* Admin 按钮 - 仅超级管理员可见 */}
                {isAdmin && (
                  <>
                    <button
                      onClick={() => navigate('/admin')}
                      className="w-full text-left px-4 py-2 text-sm text-purple-600 hover:bg-purple-50 flex items-center space-x-2"
                    >
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                        />
                      </svg>
                      <span>Admin Panel</span>
                    </button>
                    <div className="border-t border-gray-100 my-1"></div>
                  </>
                )}

                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2"
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                    />
                  </svg>
                  <span>Logout</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
