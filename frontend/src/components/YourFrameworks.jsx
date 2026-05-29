import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import FrameworkCard from './FrameworkCard'
import UpdateFrameworksButton from './UpdateFrameworksButton'
import {
  collection,
  query,
  where,
  orderBy,
  onSnapshot,
} from 'firebase/firestore'
import { db } from '../lib/firebase'

function YourFrameworks() {
  const navigate = useNavigate()
  const { user } = useAuth()

  const [frameworks, setFrameworks] = useState([])
  const [orgFrameworks, setOrgFrameworks] = useState([]) // frameworks of other people within the organization
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [expandedFamilies, setExpandedFamilies] = useState({})
  const [filter, setFilter] = useState('all') // Filter status

  // Real-time monitoring of the current user's Frameworks
  useEffect(() => {
    if (!user) {
      setLoading(false)
      return
    }

    // Creating a Firestore query - the frameworks I created
    const q = query(
      collection(db, 'frameworks'),
      where('creatorId', '==', user.uid),
      where('tenantId', '==', user.tenantId),
      orderBy('createdAt', 'desc')
    )

    // Real-time monitoring
    const unsubscribe = onSnapshot(
      q,
      querySnapshot => {
        const frameworksList = querySnapshot.docs.map(doc => {
          const data = doc.data()

          // ✅ Process artefacts and generate preview_artefacts
          const artefacts = data.artefacts || {}
          const additional = artefacts.additional || []

          // Take the first 3 artifacts for card display.
          const preview_artefacts = additional.slice(0, 3).map(art => {
            // ✅ Add type checking and protection
            if (typeof art === 'object' && art !== null) {
              return {
                name: String(art.name || ''), // ✅ Forced to string
                description: String(art.description || '').substring(0, 100),
              }
            } else if (typeof art === 'string') {
              // If it's a string, use it directly.
              return {
                name: art,
                description: '',
              }
            } else {
              // Unknown type, returns an empty object.
              console.warn('Unknown artefact type:', art)
              return {
                name: 'Unknown Artefact',
                description: '',
              }
            }
          })
          // If additional is empty, but default is present, also display default.
          if (preview_artefacts.length === 0 && artefacts.default) {
            const defaultArt = artefacts.default
            preview_artefacts.push({
              name: String(defaultArt.type || 'Framework Document'), // Forced conversion
              description: String(defaultArt.description || '').substring(
                0,
                100
              ), // Forced conversion
            })
          }

          return {
            id: doc.id,
            ...data,
            preview_artefacts, // ✅ Add processed fields
          }
        })

        setFrameworks(frameworksList)
        setLoading(false)
        setError(null)
      },
      err => {
        console.error('Error fetching frameworks:', err)
        setError('Failed to load frameworks. Please try again.')
        setLoading(false)
      }
    )

    // Cleanup function: Cancels the listener when the component is unloaded.
    return () => unsubscribe()
  }, [user])

  // Real-time monitoring of other people's Frameworks within the organization (publishedToOrganization = true)
  useEffect(() => {
    if (!user || !user.tenantId) {
      return
    }

    // Query: Frameworks published to the organization by other people within the same tenant.
    const qOrg = query(
      collection(db, 'frameworks'),
      where('tenantId', '==', user.tenantId),
      where('publishedToOrganization', '==', true),
      orderBy('createdAt', 'desc')
    )

    const unsubscribeOrg = onSnapshot(
      qOrg,
      querySnapshot => {
        const orgFrameworksList = querySnapshot.docs
          .map(doc => {
            const data = doc.data()

            // Show only creations by other people
            if (data.creatorId === user.uid) {
              return null
            }

            // Handling artefacts
            const artefacts = data.artefacts || {}
            const additional = artefacts.additional || []

            const preview_artefacts = additional.slice(0, 3).map(art => {
              if (typeof art === 'object' && art !== null) {
                return {
                  name: String(art.name || ''),
                  description: String(art.description || '').substring(0, 100),
                }
              } else if (typeof art === 'string') {
                return {
                  name: art,
                  description: '',
                }
              } else {
                return {
                  name: 'Unknown Artefact',
                  description: '',
                }
              }
            })

            if (preview_artefacts.length === 0 && artefacts.default) {
              const defaultArt = artefacts.default
              preview_artefacts.push({
                name: String(defaultArt.type || 'Framework Document'),
                description: String(defaultArt.description || '').substring(
                  0,
                  100
                ),
              })
            }

            return {
              id: doc.id,
              ...data,
              preview_artefacts,
            }
          })
          .filter(f => f !== null) // Filter out your own

        setOrgFrameworks(orgFrameworksList)
      },
      err => {
        console.error('Error fetching organization frameworks:', err)
      }
    )

    return () => unsubscribeOrg()
  }, [user])

  // Grouped by Family
  const groupedFrameworks = frameworks.reduce((acc, framework) => {
    const family = framework.family || 'Other'
    if (!acc[family]) {
      acc[family] = []
    }
    acc[family].push(framework)
    return acc
  }, {})

  // Toggle expand/collapse
  const toggleFamily = family => {
    setExpandedFamilies(prev => ({
      ...prev,
      [family]: !prev[family],
    }))
  }

  // Expand all groups by default (on first load).
  useEffect(() => {
    if (frameworks.length > 0 && Object.keys(expandedFamilies).length === 0) {
      const initialExpanded = {}
      Object.keys(groupedFrameworks).forEach(family => {
        initialExpanded[family] = true
      })
      setExpandedFamilies(initialExpanded)
    }
  }, [frameworks, groupedFrameworks, expandedFamilies])

  // Filter frameworks according to the filter.
  const getFilteredFrameworks = () => {
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
  }

  const filteredFrameworks = getFilteredFrameworks()

  // Grouped by Family (filtered)
  const filteredGroupedFrameworks = filteredFrameworks.reduce(
    (acc, framework) => {
      const family = framework.family || 'Other'
      if (!acc[family]) {
        acc[family] = []
      }
      acc[family].push(framework)
      return acc
    },
    {}
  )

  // Loading status
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

  // Error status
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

        {/* Header with Filter */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Me</h1>
            <p className="text-gray-600">
              {frameworks.length === 0
                ? "You haven't created any frameworks yet."
                : `You have ${frameworks.length} framework${frameworks.length > 1 ? 's' : ''}`}
            </p>
          </div>

          {/* ===== Filter dropdown menu ===== */}
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

        {/* Empty State */}
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
              onClick={() => navigate(`/${user.tenantId}/create`)}
              className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg hover:from-blue-700 hover:to-indigo-700 transition shadow-lg"
            >
              Create Framework
            </button>
          </div>
        ) : (
          <>
            {/* ===== The Frameworks I created (based on filters)===== */}
            {filteredFrameworks.length > 0 ? (
              <div className="space-y-6">
                {filter === 'organization' && (
                  <div className="mb-4">
                    <h2 className="text-xl font-semibold text-gray-900 mb-1">
                      My Shared Frameworks
                    </h2>
                    <p className="text-sm text-gray-600">
                      Frameworks you've published to your organization
                    </p>
                  </div>
                )}

                {Object.entries(filteredGroupedFrameworks)
                  .sort(([a], [b]) => a.localeCompare(b))
                  .map(([family, familyFrameworks]) => (
                    <div
                      key={family}
                      className="bg-white rounded-lg shadow-sm overflow-hidden"
                    >
                      {/* Family Header */}
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
                            expandedFamilies[family]
                              ? 'transform rotate-180'
                              : ''
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

                      {/* Frameworks in this Family */}
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

            {/* ===== Frameworks of other people within the organization (only displayed when filtering by Organization)===== */}
            {filter === 'organization' && orgFrameworks.length > 0 && (
              <div className="mt-12">
                <div className="mb-6 flex items-center space-x-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <svg
                      className="w-6 h-6 text-purple-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                      />
                    </svg>
                  </div>
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">
                      Organization Frameworks
                    </h2>
                    <p className="text-sm text-gray-600">
                      Frameworks shared by your team members (
                      {orgFrameworks.length})
                    </p>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow-sm p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {orgFrameworks.map(framework => (
                      <FrameworkCard
                        key={framework.id}
                        framework={framework}
                        showCreator={true}
                      />
                    ))}
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* Floating Action Button - Create New Framework */}
        {frameworks.length > 0 && (
          <button
            onClick={() => navigate(`/${user.tenantId}/create`)}
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
