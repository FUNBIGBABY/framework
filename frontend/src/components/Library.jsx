import { useState, useEffect, useCallback } from 'react'
import LibraryCard from './LibraryCard'
import { APIError, getPublicFrameworks } from '../lib/api'

const PUBLIC_LIBRARY_PAGE_SIZE = 20

/**
 * Library - Public Framework Library Page
 *
 * Features:
 * - Show all frames with isPublic: true
 * - Group by category
 * - Search and filter functions
 * - Supports exporting frameworks
 */
function Library() {
  const [frameworks, setFrameworks] = useState([])
  const [loading, setLoading] = useState(true)
  const [loadingMore, setLoadingMore] = useState(false)
  const [error, setError] = useState(null)
  const [nextCursor, setNextCursor] = useState(null)
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [searchQuery, setSearchQuery] = useState('')

  const loadFrameworks = useCallback(async (cursor = '', append = false) => {
    try {
      if (append) {
        setLoadingMore(true)
      } else {
        setLoading(true)
      }
      setError(null)

      const response = await getPublicFrameworks({
        cursor,
        limit: PUBLIC_LIBRARY_PAGE_SIZE,
        suppressAuthRedirect: true,
      })

      setFrameworks(current =>
        append ? [...current, ...response.items] : response.items
      )
      setNextCursor(response.next_cursor)
    } catch (err) {
      console.error('Error fetching library frameworks:', err)
      if (err instanceof APIError && [401, 403].includes(err.status)) {
        setError('Sign in is required to view the Library.')
      } else {
        setError('Failed to load library. Please try again.')
      }
    } finally {
      setLoading(false)
      setLoadingMore(false)
    }
  }, [])

  useEffect(() => {
    loadFrameworks()
  }, [loadFrameworks])

  // Filtering framework
  const filteredFrameworks = frameworks.filter(framework => {
    // Category Filter
    if (selectedCategory !== 'All' && framework.category !== selectedCategory) {
      return false
    }

    // Search Filters
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      const titleMatch = framework.title?.toLowerCase().includes(query)
      const categoryMatch = framework.category?.toLowerCase().includes(query)
      const tagsMatch = framework.tags?.some(tag =>
        tag.toLowerCase().includes(query)
      )

      return titleMatch || categoryMatch || tagsMatch
    }

    return true
  })

  // Group by category
  const groupedFrameworks = filteredFrameworks.reduce((acc, framework) => {
    const category = framework.category || 'Other'
    if (!acc[category]) {
      acc[category] = []
    }
    acc[category].push(framework)
    return acc
  }, {})

  // Calculate the number of each category
  const categoryCounts = frameworks.reduce((acc, framework) => {
    const category = framework.category || 'Other'
    acc[category] = (acc[category] || 0) + 1
    return acc
  }, {})

  // Available categories
  const categories = [
    'All',
    ...Array.from(
      new Set([
        'Technology',
        'Healthcare',
        'Research',
        'Financial',
        'Other',
        ...frameworks.map(framework => framework.category || 'Other'),
      ])
    ),
  ]

  // Loading status
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading Framework Marketplace...</p>
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
            onClick={() => loadFrameworks()}
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
        {/* Header */}
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Marketplace
            </h1>
            <p className="text-gray-600">
              Discover and use expert-curated frameworks ({frameworks.length}{' '}
              available)
            </p>
          </div>
          <button
            onClick={() => loadFrameworks()}
            className="self-start px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition"
          >
            Reload
          </button>
        </div>

        {/* Search Bar */}
        <div className="mb-6">
          <div className="relative max-w-xl">
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search frameworks by name, category, or tags..."
              className="w-full px-4 py-3 pl-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <svg
              className="w-5 h-5 text-gray-400 absolute left-4 top-3.5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>

        {/* Category Tabs */}
        <div className="flex gap-2 mb-6 overflow-x-auto border-b border-gray-200 pb-2">
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 font-medium whitespace-nowrap transition-colors rounded-t-lg ${
                selectedCategory === category
                  ? 'text-blue-600 bg-blue-50 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              {category}
              {category === 'All' ? (
                <span className="ml-2 text-sm text-gray-500">
                  ({frameworks.length})
                </span>
              ) : categoryCounts[category] ? (
                <span className="ml-2 text-sm text-gray-500">
                  ({categoryCounts[category]})
                </span>
              ) : null}
            </button>
          ))}
        </div>

        {/* Empty State */}
        {filteredFrameworks.length === 0 ? (
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
              No frameworks found
            </h3>
            <p className="text-gray-600">
              {searchQuery
                ? 'Try adjusting your search terms'
                : 'No frameworks have been published to the library yet'}
            </p>
          </div>
        ) : (
          /* Frameworks Grid - Grouped by Category */
          <div className="space-y-8">
            {Object.entries(groupedFrameworks)
              .sort(([a], [b]) => a.localeCompare(b))
              .map(([category, categoryFrameworks]) => (
                <div key={category}>
                  {/* Category Header */}
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="flex items-center space-x-2">
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
                      <h2 className="text-xl font-semibold text-gray-900">
                        {category}
                      </h2>
                      <span className="text-sm text-gray-500">
                        ({categoryFrameworks.length})
                      </span>
                    </div>
                  </div>

                  {/* Frameworks Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {categoryFrameworks.map(framework => (
                      <LibraryCard key={framework.id} framework={framework} />
                    ))}
                  </div>
                </div>
              ))}

            {nextCursor && (
              <div className="text-center">
                <button
                  onClick={() => loadFrameworks(nextCursor, true)}
                  disabled={loadingMore}
                  className="px-5 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  {loadingMore ? 'Loading...' : 'Load more'}
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Library
