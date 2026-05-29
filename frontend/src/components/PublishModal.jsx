import { useState } from 'react'
import { doc, updateDoc, serverTimestamp } from 'firebase/firestore'
import { db } from '../lib/firebase'

/**
 * PublishModal - A configuration pop-up for publishing frameworks to a library.
 *
 * Props:
 * - framework: The framework object to be published
 * - onClose: Callback function for closing the pop-up window
 * - onSuccess: Callback function after successful publication
 */
function PublishModal({ framework, onClose, onSuccess }) {
  const [category, setCategory] = useState(framework.family || 'Other')
  const [tags, setTags] = useState('')
  const [version, setVersion] = useState(framework.version || 'v1.0')
  const [isPublishing, setIsPublishing] = useState(false)
  const [error, setError] = useState(null)
  const [confirmed, setConfirmed] = useState(false)

  // Available classification options
  const categories = [
    'Technology',
    'Healthcare',
    'Research',
    'Financial',
    'Other',
  ]

  const handlePublish = async () => {
    if (!confirmed) {
      setError('Please confirm that your framework is ready to be shared')
      return
    }

    setIsPublishing(true)
    setError(null)

    try {
      const frameworkRef = doc(db, 'frameworks', framework.id)

      // Handling tags: Convert comma-separated strings into arrays
      const tagsArray = tags
        .split(',')
        .map(tag => tag.trim())
        .filter(tag => tag.length > 0)

      // Update the framework and add the fields required by the Library.
      await updateDoc(frameworkRef, {
        isPublic: true,
        category: category,
        tags: tagsArray,
        version: version,
        publishedAt: serverTimestamp(),
        updatedAt: serverTimestamp(),
      })

      console.log('✅ Framework published to library:', framework.id)

      // ========== NEW Push to Vector Store ==========
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

      try {
        const pushResponse = await fetch(
          `${API_BASE_URL}/api/frameworks/push-framework`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              framework: {
                ...framework,
                isPublic: true,
                category: category,
                tags: tagsArray,
                version: version,
                tenantId: framework.tenantId,
              },
            }),
          }
        )

        if (pushResponse.ok) {
          console.log('✅ Framework pushed to Vector Store successfully')
        } else {
          console.error(
            '⚠️ Vector Store push failed (non-blocking):',
            pushResponse.statusText
          )
        }
      } catch (vectorError) {
        console.error('⚠️ Vector Store push error (non-blocking):', vectorError)
      }

      // Successful callback call
      if (onSuccess) {
        onSuccess()
      }

      // Close pop-up window
      onClose()
    } catch (err) {
      console.error('❌ Error publishing framework:', err)
      setError('Failed to publish framework. Please try again.')
      setIsPublishing(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full shadow-2xl">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900">
              Publish to Marketplace
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition"
              disabled={isPublishing}
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
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="px-6 py-4 space-y-4">
          {/* Framework Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Framework
            </label>
            <div className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-800">
              {framework.title || 'Untitled Framework'}
            </div>
          </div>

          {/* Category */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <select
              value={category}
              onChange={e => setCategory(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isPublishing}
            >
              {categories.map(cat => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Tags (comma-separated)
            </label>
            <input
              type="text"
              value={tags}
              onChange={e => setTags(e.target.value)}
              placeholder="e.g., agile, software, retrospective"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isPublishing}
            />
            <p className="text-xs text-gray-500 mt-1">
              Separate multiple tags with commas
            </p>
          </div>

          {/* Version */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Version
            </label>
            <input
              type="text"
              value={version}
              onChange={e => setVersion(e.target.value)}
              placeholder="e.g., v1.0"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isPublishing}
            />
          </div>

          {/* Confirmation Checkbox */}
          <div className="flex items-start space-x-2 pt-2">
            <input
              type="checkbox"
              id="confirm"
              checked={confirmed}
              onChange={e => setConfirmed(e.target.checked)}
              className="mt-1 w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
              disabled={isPublishing}
            />
            <label htmlFor="confirm" className="text-sm text-gray-700">
              I confirm this framework is ready to be shared publicly in the
              Library
            </label>
          </div>

          {/* Error Message */}
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-700 hover:bg-gray-200 rounded-lg transition"
            disabled={isPublishing}
          >
            Cancel
          </button>
          <button
            onClick={handlePublish}
            disabled={isPublishing || !confirmed}
            className={`px-4 py-2 rounded-lg transition flex items-center space-x-2 ${
              isPublishing || !confirmed
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {isPublishing ? (
              <>
                <svg
                  className="animate-spin h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                <span>Publishing...</span>
              </>
            ) : (
              <span>Publish to Marketplace</span>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

export default PublishModal
