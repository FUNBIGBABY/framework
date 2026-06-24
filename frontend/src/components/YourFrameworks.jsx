import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import FrameworkCard from './FrameworkCard'
import UpdateFrameworksButton from './UpdateFrameworksButton'
import { getCurrentTenantId, getMyFrameworks } from '../lib/api'

function YourFrameworks() {
  const navigate = useNavigate()
  const { user } = useAuth()

  const [frameworks, setFrameworks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [expandedFamilies, setExpandedFamilies] = useState({})
  const [filter, setFilter] = useState('all')
  const tenantShim = user?.tenantId || getCurrentTenantId() || 'personal'

  useEffect(() => {
    let cancelled = false

    if (!user) {
      setLoading(false)
      return
    }

    async function loadFrameworks() {
      try {
        setLoading(true)
        const frameworksList = await getMyFrameworks()

        if (!cancelled) {
          setFrameworks(frameworksList)
          setError(null)
        }
      } catch (err) {
        console.error('Error fetching frameworks:', err)
        if (!cancelled) {
          setError('Failed to load frameworks. Please try again.')
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadFrameworks()

    return () => {
      cancelled = true
    }
  }, [user])

  const filteredFrameworks = useMemo(() => {
    switch (filter) {
      case 'drafts':
        return frameworks.filter(f => !f.isPublic && !f.publishedToOrganization)
      case 'library':
        return frameworks.filter(f => f.isPublic)
      case 'organization':
        return frameworks.filter(f => f.publishedToOrganization)
      case 'all':
      default:
        return frameworks
    }
  }, [filter, frameworks])

  const filteredGroupedFrameworks = useMemo(
    () =>
      filteredFrameworks.reduce((acc, framework) => {
        const family = framework.family || 'Other'
        if (!acc[family]) acc[family] = []
        acc[family].push(framework)
        return acc
      }, {}),
    [filteredFrameworks]
  )

  useEffect(() => {
    if (
      filteredFrameworks.length > 0 &&
      Object.keys(expandedFamilies).length === 0
    ) {
      const initialExpanded = {}
      Object.keys(filteredGroupedFrameworks).forEach(family => {
        initialExpanded[family] = true
      })
      setExpandedFamilies(initialExpanded)
    }
  }, [expandedFamilies, filteredFrameworks, filteredGroupedFrameworks])

  const toggleFamily = family => {
    setExpandedFamilies(prev => ({
      ...prev,
      [family]: !prev[family],
    }))
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading your frameworks...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <UpdateFrameworksButton />

        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Me</h1>
            <p className="text-gray-600">
              {frameworks.length === 0
                ? "You haven't created any frameworks yet."
                : `You have ${frameworks.length} framework${frameworks.length > 1 ? 's' : ''}`}
            </p>
          </div>

          {frameworks.length > 0 && (
            <div className="flex items-center space-x-3">
              <label
                htmlFor="filter"
                className="text-sm font-medium text-gray-700"
              >
                Filter:
              </label>
              <select
                id="filter"
                value={filter}
                onChange={e => setFilter(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-900 text-sm"
              >
                <option value="all">
                  All Frameworks ({frameworks.length})
                </option>
                <option value="drafts">
                  My Drafts (
                  {
                    frameworks.filter(
                      f => !f.isPublic && !f.publishedToOrganization
                    ).length
                  }
                  )
                </option>
                <option value="library">
                  Published to Marketplace (
                  {frameworks.filter(f => f.isPublic).length})
                </option>
                <option value="organization">
                  Published to Organization (
                  {frameworks.filter(f => f.publishedToOrganization).length})
                </option>
              </select>
            </div>
          )}
        </div>

        {frameworks.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <svg
              className="mx-auto h-24 w-24 text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No frameworks yet
            </h3>
            <p className="text-gray-600 mb-6">
              Create your first framework to get started
            </p>
            <button
              onClick={() => navigate(`/${tenantShim}/create`)}
              className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg hover:from-blue-700 hover:to-indigo-700 transition shadow-lg"
            >
              Create Framework
            </button>
          </div>
        ) : filteredFrameworks.length > 0 ? (
          <div className="space-y-6">
            {Object.entries(filteredGroupedFrameworks)
              .sort(([a], [b]) => a.localeCompare(b))
              .map(([family, familyFrameworks]) => (
                <div
                  key={family}
                  className="bg-white rounded-lg shadow-sm overflow-hidden"
                >
                  <button
                    onClick={() => toggleFamily(family)}
                    className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-blue-100 rounded-lg">
                        <svg
                          className="w-5 h-5 text-blue-600"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
                          />
                        </svg>
                      </div>
                      <div className="text-left">
                        <h2 className="text-xl font-semibold text-gray-900">
                          {family}
                        </h2>
                        <p className="text-sm text-gray-600">
                          {familyFrameworks.length} framework
                          {familyFrameworks.length > 1 ? 's' : ''}
                        </p>
                      </div>
                    </div>
                    <svg
                      className={`w-6 h-6 text-gray-400 transition-transform ${
                        expandedFamilies[family] ? 'transform rotate-180' : ''
                      }`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </button>

                  {expandedFamilies[family] && (
                    <div className="px-6 pb-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {familyFrameworks.map(framework => (
                        <FrameworkCard
                          key={framework.id}
                          framework={framework}
                          showCreator={false}
                        />
                      ))}
                    </div>
                  )}
                </div>
              ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm p-8 text-center">
            <p className="text-gray-600">
              No frameworks match the selected filter.
            </p>
          </div>
        )}

        {frameworks.length > 0 && (
          <button
            onClick={() => navigate(`/${tenantShim}/create`)}
            className="fixed bottom-8 right-8 p-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full shadow-2xl hover:shadow-3xl hover:scale-110 transition-all duration-200 group"
            title="Create New Framework"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  )
}

export default YourFrameworks
