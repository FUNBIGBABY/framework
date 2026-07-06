import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { useNavigate } from 'react-router-dom'
import PublishModal from './PublishModal'
import API_ENDPOINTS, {
  apiFetch,
  deleteFramework,
  unpublishFramework,
} from '../lib/api'

function FrameworkCard({ framework, showCreator = false }) {
  const navigate = useNavigate()

  const [showDropdown, setShowDropdown] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [isDeleted, setIsDeleted] = useState(false)
  const [isPublic, setIsPublic] = useState(
    Boolean(framework.is_public ?? framework.isPublic)
  )
  const [showPublishModal, setShowPublishModal] = useState(false)
  const [dropdownPosition, setDropdownPosition] = useState({ top: 0, left: 0 })
  const buttonRef = useRef(null)
  const dropdownRef = useRef(null)
  const canManage = framework.canManage !== false && !showCreator
  const isShared = Boolean(framework.publishedToOrganization)

  useEffect(() => {
    setIsPublic(Boolean(framework.is_public ?? framework.isPublic))
  }, [framework.is_public, framework.isPublic])

  const handleEdit = () => {
    navigate(`/frameworks/${framework.id}`)
  }

  const handleDownload = async () => {
    try {
      const response = await apiFetch(API_ENDPOINTS.EXPORT_DOCX, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(framework),
      })

      if (!response.ok) {
        throw new Error('Download failed')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${framework.title.replace(/[^a-zA-Z0-9]/g, '_')}.docx`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Download failed:', error)
      alert('Failed to download framework')
    }
  }

  const formatDate = dateString => {
    const date = dateString ? new Date(dateString) : null
    if (!date || Number.isNaN(date.getTime())) return 'unknown date'

    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  const handlePublish = () => {
    setShowPublishModal(true)
    setShowDropdown(false)
  }

  const handlePublishSuccess = result => {
    setIsPublic(Boolean(result?.is_public ?? true))
  }

  const handleUnpublish = async () => {
    const confirmed = window.confirm(
      'Are you sure you want to unpublish this framework from the Library?'
    )

    if (!confirmed) return

    try {
      const result = await unpublishFramework(framework.id)
      setIsPublic(Boolean(result?.is_public))
      setShowDropdown(false)
    } catch (error) {
      console.error('Error unpublishing framework:', error)
      alert('Failed to unpublish framework')
    }
  }

  const handlePublishToOrg = () => {
    alert('Organization sharing is not available in this migration round.')
    setShowDropdown(false)
  }

  const handleUnpublishFromOrg = () => {
    alert('Organization sharing is not available in this migration round.')
    setShowDropdown(false)
  }

  const handleDelete = async () => {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${framework.title}"? This action cannot be undone.`
    )

    if (!confirmed) return

    setIsDeleting(true)

    try {
      await deleteFramework(framework.id)
      setIsDeleted(true)
    } catch (error) {
      console.error('Error deleting framework:', error)
      alert('Failed to delete framework')
      setIsDeleting(false)
    }
  }

  const handleDuplicate = () => {
    alert('Duplicate feature - Coming soon!')
    setShowDropdown(false)
  }

  const updateDropdownPosition = () => {
    if (buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect()
      setDropdownPosition({
        top: rect.bottom + window.scrollY + 4,
        left: rect.right - 208 + window.scrollX,
      })
    }
  }

  const toggleDropdown = () => {
    if (!showDropdown) {
      updateDropdownPosition()
    }
    setShowDropdown(!showDropdown)
  }

  useEffect(() => {
    if (!showDropdown) return

    const handleUpdate = () => {
      updateDropdownPosition()
    }

    window.addEventListener('scroll', handleUpdate, true)
    window.addEventListener('resize', handleUpdate)

    return () => {
      window.removeEventListener('scroll', handleUpdate, true)
      window.removeEventListener('resize', handleUpdate)
    }
  }, [showDropdown])

  useEffect(() => {
    if (!showDropdown) return

    const handleClickOutside = event => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target) &&
        buttonRef.current &&
        !buttonRef.current.contains(event.target)
      ) {
        setShowDropdown(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [showDropdown])

  if (isDeleted) return null

  return (
    <>
      <div className="bg-white rounded-lg border border-gray-200 hover:shadow-lg transition-shadow duration-200 p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {framework.title}
            </h3>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <span className="px-2 py-0.5 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                {framework.family}
              </span>
              <span>-</span>
              <span>v{framework.version}</span>

              {isPublic && (
                <>
                  <span>-</span>
                  <span className="px-2 py-0.5 bg-green-100 text-green-800 rounded text-xs font-medium">
                    Published
                  </span>
                </>
              )}

              {isShared && (
                <>
                  <span>-</span>
                  <span className="px-2 py-0.5 bg-purple-100 text-purple-800 rounded text-xs font-medium">
                    Shared
                  </span>
                </>
              )}
            </div>

            {showCreator && (
              <p className="text-xs text-gray-500 mt-1">
                by{' '}
                {framework.creatorEmail ||
                  framework.creatorName ||
                  'Team Member'}
              </p>
            )}
          </div>

          <div className="ml-4 flex-shrink-0">
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-green-600">
                {Math.round(framework.confidence)}%
              </span>
            </div>
            <p className="text-xs text-gray-500 text-right mt-1">Confidence</p>
          </div>
        </div>

        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-3">
            Key Artefacts
          </h4>
          <div className="space-y-2">
            {framework.preview_artefacts &&
            framework.preview_artefacts.length > 0 ? (
              framework.preview_artefacts.map((artefact, index) => (
                <div
                  key={index}
                  className="bg-gray-50 rounded p-3 border border-gray-100"
                >
                  <div className="flex items-start">
                    <svg
                      className="w-4 h-4 text-blue-600 mt-0.5 mr-2 flex-shrink-0"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {artefact.name}
                      </p>
                      {artefact.description && (
                        <p className="text-xs text-gray-600 mt-1 line-clamp-2">
                          {artefact.description}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-gray-500 italic">
                No artefacts defined
              </p>
            )}
          </div>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="text-xs text-gray-500">
            <span>Created {formatDate(framework.created_at)}</span>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={handleDownload}
              className="px-3 py-1.5 text-sm border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors flex items-center space-x-1"
              title="Download as Word document"
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
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"
                />
              </svg>
              <span>Download</span>
            </button>

            {canManage && (
              <button
                onClick={handleEdit}
                className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors flex items-center space-x-1"
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
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                  />
                </svg>
                <span>Edit</span>
              </button>
            )}

            {canManage && (
              <button
                ref={buttonRef}
                onClick={toggleDropdown}
                className="px-2 py-1.5 text-sm border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors"
                title="More options"
              >
                <svg
                  className="w-4 h-4"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                </svg>
              </button>
            )}
          </div>
        </div>
      </div>

      {showDropdown &&
        createPortal(
          <div
            ref={dropdownRef}
            className="w-60 bg-white rounded-lg shadow-2xl border border-gray-200 py-1"
            style={{
              position: 'absolute',
              top: `${dropdownPosition.top}px`,
              left: `${dropdownPosition.left}px`,
              zIndex: 9999,
            }}
          >
            {isPublic ? (
              <button
                onClick={handleUnpublish}
                className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
              >
                <span>Unpublish from Marketplace</span>
              </button>
            ) : (
              <button
                onClick={handlePublish}
                className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
              >
                <span>Publish to Marketplace</span>
              </button>
            )}

            {isShared ? (
              <button
                onClick={handleUnpublishFromOrg}
                className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
              >
                <span>Unpublish from Organization</span>
              </button>
            ) : (
              <button
                onClick={handlePublishToOrg}
                className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
              >
                <span>Publish to Organization</span>
              </button>
            )}

            <button
              onClick={handleDuplicate}
              className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
            >
              <span>Duplicate</span>
            </button>

            <div className="border-t border-gray-100 my-1"></div>

            <button
              onClick={handleDelete}
              disabled={isDeleting}
              className="w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span>{isDeleting ? 'Deleting...' : 'Delete'}</span>
            </button>
          </div>,
          document.body
        )}

      {showPublishModal && (
        <PublishModal
          framework={framework}
          onClose={() => setShowPublishModal(false)}
          onSuccess={handlePublishSuccess}
        />
      )}
    </>
  )
}

export default FrameworkCard
