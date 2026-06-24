import { useCallback, useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  APIError,
  createAdminUser,
  disableAdminUser,
  enableAdminUser,
  getAdminUsers,
} from '../lib/api'

const emptyUserForm = {
  email: '',
  username: '',
  password: '',
}

function formatDate(value) {
  if (!value) return 'Never'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return 'Unknown'
  return date.toLocaleString()
}

function getErrorMessage(error, fallback) {
  if (error instanceof APIError) {
    if (error.status === 403) {
      return 'Admin access is enforced by the backend. This account cannot manage users.'
    }
    if (error.status === 401) {
      return 'Sign in is required before opening the admin panel.'
    }
  }

  return error?.message || fallback
}

const AdminPanel = () => {
  const navigate = useNavigate()
  const [users, setUsers] = useState([])
  const [newUser, setNewUser] = useState(emptyUserForm)
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [accessState, setAccessState] = useState('ready')

  const loadUsers = useCallback(async () => {
    setLoading(true)
    setError('')
    setSuccessMessage('')

    try {
      const backendUsers = await getAdminUsers({ suppressAuthRedirect: true })
      setUsers(Array.isArray(backendUsers) ? backendUsers : [])
      setAccessState('ready')
    } catch (err) {
      console.error('Admin users load failed:', err)
      setUsers([])
      if (err instanceof APIError && err.status === 403) {
        setAccessState('forbidden')
      } else if (err instanceof APIError && err.status === 401) {
        setAccessState('unauthenticated')
      } else {
        setAccessState('error')
      }
      setError(getErrorMessage(err, 'Failed to load admin users.'))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadUsers()
  }, [loadUsers])

  const filteredUsers = useMemo(() => {
    const search = searchTerm.trim().toLowerCase()
    if (!search) return users

    return users.filter(user => {
      return (
        user.email?.toLowerCase().includes(search) ||
        user.username?.toLowerCase().includes(search) ||
        user.id?.toLowerCase().includes(search)
      )
    })
  }, [searchTerm, users])

  const activeCount = users.filter(user => !user.is_disabled).length
  const disabledCount = users.filter(user => user.is_disabled).length

  const handleCreateUser = async event => {
    event.preventDefault()
    setError('')
    setSuccessMessage('')

    if (!newUser.email.trim() || !newUser.password) {
      setError('Email and password are required.')
      return
    }

    try {
      setSubmitting(true)
      const createdUser = await createAdminUser(
        {
          email: newUser.email.trim(),
          username: newUser.username.trim(),
          password: newUser.password,
        },
        { suppressAuthRedirect: true }
      )
      setNewUser(emptyUserForm)
      await loadUsers()
      setSuccessMessage(`Created user ${createdUser.email}.`)
    } catch (err) {
      console.error('Admin user creation failed:', err)
      setError(getErrorMessage(err, 'Failed to create user.'))
    } finally {
      setSubmitting(false)
    }
  }

  const handleToggleDisabled = async user => {
    const action = user.is_disabled ? 'enable' : 'disable'
    if (!window.confirm(`Are you sure you want to ${action} ${user.email}?`)) {
      return
    }

    setError('')
    setSuccessMessage('')

    try {
      setSubmitting(true)
      const updatedUser = user.is_disabled
        ? await enableAdminUser(user.id, { suppressAuthRedirect: true })
        : await disableAdminUser(user.id, { suppressAuthRedirect: true })

      setUsers(currentUsers =>
        currentUsers.map(currentUser =>
          currentUser.id === updatedUser.id ? updatedUser : currentUser
        )
      )
      setSuccessMessage(
        `${updatedUser.email} is now ${
          updatedUser.is_disabled ? 'disabled' : 'enabled'
        }.`
      )
    } catch (err) {
      console.error('Admin user status update failed:', err)
      setError(getErrorMessage(err, `Failed to ${action} user.`))
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading admin users...</p>
        </div>
      </div>
    )
  }

  const showAccessBlock =
    accessState === 'forbidden' || accessState === 'unauthenticated'
  const accessStatus = accessState === 'forbidden' ? '403' : '401'

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Admin Users
            </h1>
            <p className="text-gray-600">
              Backend-managed account access. Public registration remains
              disabled.
            </p>
          </div>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={loadUsers}
              className="px-4 py-2 border border-gray-300 bg-white text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Reload
            </button>
            {accessState === 'unauthenticated' && (
              <button
                type="button"
                onClick={() => navigate('/login')}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Sign in
              </button>
            )}
          </div>
        </div>

        {successMessage && (
          <div className="mb-6 bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg flex items-center justify-between">
            <span>{successMessage}</span>
            <button
              type="button"
              onClick={() => setSuccessMessage('')}
              className="text-green-700 hover:text-green-900"
              aria-label="Dismiss success message"
            >
              Close
            </button>
          </div>
        )}

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg flex items-center justify-between gap-4">
            <span>{error}</span>
            <button
              type="button"
              onClick={() => setError('')}
              className="text-red-700 hover:text-red-900"
              aria-label="Dismiss error message"
            >
              Close
            </button>
          </div>
        )}

        {showAccessBlock ? (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Admin access unavailable
            </h2>
            <p className="text-gray-600">
              The backend returned {accessStatus}, so user management is not
              available for this session.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 xl:grid-cols-[420px_1fr] gap-8">
            <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Create User
              </h2>
              <form onSubmit={handleCreateUser} className="space-y-4">
                <div>
                  <label
                    htmlFor="admin-email"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Email
                  </label>
                  <input
                    id="admin-email"
                    type="email"
                    value={newUser.email}
                    onChange={event =>
                      setNewUser(current => ({
                        ...current,
                        email: event.target.value,
                      }))
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    autoComplete="email"
                  />
                </div>

                <div>
                  <label
                    htmlFor="admin-username"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Username
                  </label>
                  <input
                    id="admin-username"
                    type="text"
                    value={newUser.username}
                    onChange={event =>
                      setNewUser(current => ({
                        ...current,
                        username: event.target.value,
                      }))
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    autoComplete="username"
                  />
                </div>

                <div>
                  <label
                    htmlFor="admin-password"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Temporary Password
                  </label>
                  <input
                    id="admin-password"
                    type="password"
                    value={newUser.password}
                    onChange={event =>
                      setNewUser(current => ({
                        ...current,
                        password: event.target.value,
                      }))
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    autoComplete="new-password"
                  />
                </div>

                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-300 transition-colors font-medium"
                >
                  Create User
                </button>
              </form>

              <div className="mt-6 border-t border-gray-200 pt-4">
                <h3 className="text-sm font-semibold text-gray-900 mb-1">
                  Domain Policy
                </h3>
                <p className="text-sm text-gray-600">
                  Domain management is not part of the accepted Phase 5 admin
                  REST contract.
                </p>
              </div>
            </section>

            <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-900">
                  User Management
                </h2>
                <input
                  type="search"
                  value={searchTerm}
                  onChange={event => setSearchTerm(event.target.value)}
                  placeholder="Search users"
                  className="w-full lg:w-72 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="mb-4 grid grid-cols-3 gap-2 text-sm">
                <div className="bg-gray-50 p-3 rounded text-center">
                  <div className="font-semibold text-gray-900">
                    {users.length}
                  </div>
                  <div className="text-gray-600 text-xs">Total</div>
                </div>
                <div className="bg-green-50 p-3 rounded text-center">
                  <div className="font-semibold text-green-700">
                    {activeCount}
                  </div>
                  <div className="text-gray-600 text-xs">Enabled</div>
                </div>
                <div className="bg-red-50 p-3 rounded text-center">
                  <div className="font-semibold text-red-700">
                    {disabledCount}
                  </div>
                  <div className="text-gray-600 text-xs">Disabled</div>
                </div>
              </div>

              <div className="max-h-[32rem] overflow-y-auto space-y-2">
                {filteredUsers.length === 0 ? (
                  <p className="text-gray-500 text-sm italic">
                    No users found
                  </p>
                ) : (
                  filteredUsers.map(user => (
                    <div
                      key={user.id}
                      className={`p-4 border rounded-lg ${
                        user.is_disabled
                          ? 'bg-red-50 border-red-200'
                          : 'bg-gray-50 border-gray-200'
                      }`}
                    >
                      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                        <div className="min-w-0">
                          <div className="flex flex-wrap items-center gap-2">
                            <p className="font-medium text-gray-900 truncate">
                              {user.username || user.email}
                            </p>
                            {user.is_super_admin && (
                              <span className="px-2 py-0.5 bg-purple-100 text-purple-800 text-xs font-semibold rounded">
                                SUPER ADMIN
                              </span>
                            )}
                            {user.is_disabled && (
                              <span className="px-2 py-0.5 bg-red-100 text-red-800 text-xs font-semibold rounded">
                                DISABLED
                              </span>
                            )}
                          </div>
                          <p className="text-sm text-gray-600 truncate">
                            {user.email}
                          </p>
                          <p className="text-xs text-gray-400 font-mono truncate">
                            {user.id}
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            Last login: {formatDate(user.last_login)}
                          </p>
                        </div>

                        {user.is_super_admin ? (
                          <button
                            type="button"
                            disabled
                            className="px-3 py-1 bg-gray-200 text-gray-500 text-sm rounded cursor-not-allowed"
                          >
                            Protected
                          </button>
                        ) : (
                          <button
                            type="button"
                            onClick={() => handleToggleDisabled(user)}
                            disabled={submitting}
                            className={`px-3 py-1 text-white text-sm rounded transition-colors disabled:opacity-60 ${
                              user.is_disabled
                                ? 'bg-green-600 hover:bg-green-700'
                                : 'bg-red-600 hover:bg-red-700'
                            }`}
                          >
                            {user.is_disabled ? 'Enable' : 'Disable'}
                          </button>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </section>
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminPanel
