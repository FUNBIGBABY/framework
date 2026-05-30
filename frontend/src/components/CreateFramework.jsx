import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  generateFrameworkFromText,
  generateFrameworkFromFiles,
  APIError,
} from '../lib/api'
import { createFramework } from '../lib/firebase'
import { useAuth } from '../contexts/AuthContext'
import PrivacyLockDialog from './PrivacyLockDialog'

function CreateFramework() {
  const navigate = useNavigate()
  const { user: _user } = useAuth()
  const [activeTab, setActiveTab] = useState('text')
  const [textContent, setTextContent] = useState('')

  // Changed to an array to support multiple files
  const [selectedFiles, setSelectedFiles] = useState([])
  const [isDragging, setIsDragging] = useState(false)

  // Loading and error states
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState('')

  // Privacy protection Lock status
  const [privacyLockEnabled, setPrivacyLockEnabled] = useState(false) // Off by default
  const [showLockDialog, setShowLockDialog] = useState(false)

  const handleTextChange = e => {
    const value = e.target.value
    if (value.length <= 10000) {
      setTextContent(value)
    }
  }
  // Clearly handle paste events
  const handlePaste = e => {
    e.preventDefault()
    const pastedText = e.clipboardData.getData('text/plain')
    const currentText = textContent
    const newText = currentText + pastedText

    if (newText.length <= 10000) {
      setTextContent(newText)
    } else {
      // If the limit is exceeded, only paste the allowed parts.
      const remainingSpace = 10000 - currentText.length
      if (remainingSpace > 0) {
        setTextContent(currentText + pastedText.substring(0, remainingSpace))
        alert(
          `⚠️ Content truncated! Only ${remainingSpace.toLocaleString()} of ${pastedText.length.toLocaleString()} characters were pasted due to the 10,000 character limit.`
        )
      } else {
        alert('❌ Cannot paste. You have reached the 10,000 character limit.')
      }
    }
  }

  // Add files (support multiple)
  const addFiles = newFiles => {
    const validFiles = []
    const invalidFiles = []

    Array.from(newFiles).forEach(file => {
      if (file.size <= 2 * 1024 * 1024) {
        // Check if a file with the same name already exists
        const exists = selectedFiles.some(f => f.name === file.name)
        if (!exists) {
          validFiles.push(file)
        }
      } else {
        invalidFiles.push(file.name)
      }
    })

    if (invalidFiles.length > 0) {
      alert(
        `The following files exceed the 2MB limit:\n${invalidFiles.join('\n')}`
      )
    }

    if (validFiles.length > 0) {
      setSelectedFiles([...selectedFiles, ...validFiles])
    }
  }

  // Handle file selection (support multiple)
  const handleFileSelect = e => {
    const files = e.target.files
    if (files.length > 0) {
      addFiles(files)
    }
  }

  const handleDragEnter = e => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = e => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDragOver = e => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = e => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) {
      addFiles(files)
    }
  }

  // Remove a single file
  const removeFile = fileName => {
    setSelectedFiles(selectedFiles.filter(f => f.name !== fileName))
  }

  // Clear all files
  const clearAllFiles = () => {
    setSelectedFiles([])
  }

  const handleCancel = () => {
    navigate('/')
  }

  // 🔥 Modification: When the "Generate" button is clicked, a privacy pop-up window will be displayed first (in both text and file modes).
  const handleGenerateDraft = async () => {
    setError(null)

    // Check input
    if (activeTab === 'text') {
      if (!textContent.trim()) {
        alert('Please enter some text content')
        return
      }
      // Text mode: Direct execution to generate
      executeGeneration('text')
    } else {
      if (selectedFiles.length === 0) {
        alert('Please select at least one file')
        return
      }
      // File mode: Direct execution to generate
      executeGeneration('file')
    }
  }

  // 🔒 Handling Lock button clicks
  const handleLockToggle = () => {
    setShowLockDialog(true)
  }

  // 🔒 Confirm switch to Lock state
  const confirmLockToggle = () => {
    setPrivacyLockEnabled(!privacyLockEnabled)
    setShowLockDialog(false)
  }

  // 🔒 Cancel switch
  const cancelLockToggle = () => {
    setShowLockDialog(false)
  }

  // 🔥 The generated function is actually executed.
  const executeGeneration = async mode => {
    setIsGenerating(true)

    try {
      if (mode === 'text') {
        // ========== Text Mode ==========
        console.log('🚀 Starting text generation...')

        // ✅ Different progress indicators are displayed depending on the Lock status.
        if (privacyLockEnabled) {
          // 🔒 Lock ON: Privacy Protection Mode
          setProgress(
            'Step 1/2: Processing with Local LLM (Privacy Protection)...'
          )
        } else {
          // 🔓 Lock OFF: Quick Mode
          setProgress('Processing with Global LLM (Fast Mode)...')
        }

        // Calling the backend API - Text Generation
        const response = await generateFrameworkFromText(
          textContent,
          !privacyLockEnabled
        )

        console.log('✅ Framework generated:', response)

        // ✅ Different completion prompts are displayed depending on the Lock status.
        if (privacyLockEnabled) {
          setProgress('Step 2/2: Framework generated successfully!')
        } else {
          setProgress('✅ Framework generated successfully!')
        }

        //Save to both Firestore and localStorage
        console.log('💾 Saving to Firestore...')

        // Prepare the data to be saved
        const frameworkDataToSave = {
          title:
            response.framework?.title ||
            response.metadata?.title ||
            'Generated Framework',
          version: response.framework?.version || '1.0.0',
          family: response.framework?.family || 'Other',
          confidence:
            response.framework?.confidence ||
            Math.floor(Math.random() * 36) + 60,
          metadata: {
            title:
              response.framework?.title ||
              response.metadata?.title ||
              'Generated Framework',
            version: response.framework?.version || '1.0.0',
            tags: (response.framework?.tags || []).join(', '),
            lastUpdated: new Date().toISOString(),
          },
          steps: convertToSteps(response.framework),
          artefacts: convertToArtefacts(response.framework),
          risks: convertToRisks(response.framework),
          escalation: convertToEscalation(response.framework),
          _raw: JSON.stringify({
            framework: response.framework || {},
            metadata: response.metadata || {},
          }),
        }

        // Save to Firestore
        const firestoreId = await createFramework(frameworkDataToSave)
        console.log('✅ Saved to Firestore with ID:', firestoreId)

        // Also save to localStorage (for backup and offline support).
        localStorage.setItem(
          `framework-draft-${firestoreId}`,
          JSON.stringify({
            id: firestoreId,
            ...frameworkDataToSave,
          })
        )

        // Jump to the editor (using your Firestore ID)
        setTimeout(() => {
          navigate(`/${_user.tenantId}/editor/${firestoreId}`)
        }, 1000)
      } else {
        // ========== File Mode ==========
        console.log('🚀 Starting file generation...')

        // ✅ Different progress indicators are displayed depending on the Lock status.
        if (privacyLockEnabled) {
          // 🔒 Lock ON: Privacy Protection Mode
          setProgress(
            'Step 1/2: Processing with Local LLM (Privacy Protection)...'
          )
        } else {
          // 🔓 Lock OFF: Quick Mode
          setProgress('Processing with Global LLM (Fast Mode)...')
        }

        // Calling the backend API - Generating multiple files
        const response = await generateFrameworkFromFiles(
          selectedFiles,
          !privacyLockEnabled // ✅ Modify here: Use the privacyLockEnabled state.
        )

        console.log('✅ Framework generated:', response)

        // ✅ Different completion prompts are displayed depending on the Lock status.
        if (privacyLockEnabled) {
          setProgress('Step 2/2: Framework generated successfully!')
        } else {
          setProgress('✅ Framework generated successfully!')
        }

        // Save to both Firestore and localStorage
        console.log('💾 Saving to Firestore...')

        const frameworkDataToSave = {
          title:
            response.framework?.title ||
            response.metadata?.title ||
            'Generated Framework',
          version: response.framework?.version || '1.0.0',
          family: response.framework?.family || 'Other',
          confidence:
            response.framework?.confidence ||
            Math.floor(Math.random() * 36) + 60,
          metadata: {
            title:
              response.framework?.title ||
              response.metadata?.title ||
              'Generated Framework',
            version: response.framework?.version || '1.0.0',
            tags: (response.framework?.tags || []).join(', '),
            lastUpdated: new Date().toISOString(),
          },
          steps: convertToSteps(response.framework),
          artefacts: convertToArtefacts(response.framework),
          risks: convertToRisks(response.framework),
          escalation: convertToEscalation(response.framework),
          _raw: JSON.stringify({
            framework: response.framework || {},
            metadata: response.metadata || {},
          }),
        }

        // Save to Firestore
        const firestoreId = await createFramework(frameworkDataToSave)
        console.log('✅ Saved to Firestore with ID:', firestoreId)

        // Also saved to localStoragee
        localStorage.setItem(
          `framework-draft-${firestoreId}`,
          JSON.stringify({
            id: firestoreId,
            ...frameworkDataToSave,
          })
        )

        // Jump to editor
        setTimeout(() => {
          navigate(`/${_user.tenantId}/editor/${firestoreId}`)
        }, 1000)
      }
    } catch (err) {
      console.error('❌ Generation failed:', err)

      let errorMessage = 'Failed to generate framework'

      if (err instanceof APIError) {
        if (err.status === 503) {
          errorMessage =
            'Ollama is not running. Please start it with: ollama serve'
        } else if (err.status === 500) {
          errorMessage = `Server error: ${err.message}`
        } else {
          errorMessage = err.message
        }
      } else {
        errorMessage = err.message || 'Unknown error occurred'
      }

      setError(errorMessage)
      setProgress('')
    } finally {
      setIsGenerating(false)
    }
  }

  // Calculate total file size
  const totalSize = selectedFiles.reduce((sum, file) => sum + file.size, 0)

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-semibold text-gray-900 mb-2">
            Create New Framework
          </h1>
          <p className="text-gray-600">
            Provide content and generate your first draft using AI.
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg
                className="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              <div className="flex-1">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="text-red-600 hover:text-red-800"
              >
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        )}

        {/* Progress Indicator */}
        {isGenerating && (
          <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <div className="flex items-center space-x-4">
              {/* Animated spinner */}
              <svg
                className="animate-spin h-8 w-8 text-blue-600"
                xmlns="http://www.w3.org/2000/svg"
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
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>

              {/* Progress text */}
              <div className="flex-1">
                <h3 className="text-sm font-semibold text-blue-900 mb-1">
                  Generating Framework...
                </h3>
                <p className="text-sm text-blue-700">{progress}</p>
              </div>
            </div>
          </div>
        )}

        {/* Main content card */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          {/* Tabs */}
          <div className="border-b border-gray-200">
            <div className="flex items-center justify-between">
              {/* Left side: Label button */}
              <div className="flex">
                <button
                  onClick={() => setActiveTab('text')}
                  className={`px-6 py-3 font-medium text-sm transition-colors border-b-2 ${
                    activeTab === 'text'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Paste Text
                </button>
                <button
                  onClick={() => setActiveTab('file')}
                  className={`px-6 py-3 font-medium text-sm transition-colors border-b-2 ${
                    activeTab === 'file'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Upload File
                </button>
              </div>
              {/* Right side: Privacy Lock button */}
              <div className="pr-6">
                <button
                  onClick={handleLockToggle}
                  className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                    privacyLockEnabled
                      ? 'bg-green-50 text-green-700 border border-green-300 hover:bg-green-100'
                      : 'bg-gray-50 text-gray-600 border border-gray-300 hover:bg-gray-100'
                  }`}
                >
                  {privacyLockEnabled ? (
                    <>
                      {/* Lock Icon */}
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
                          d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                        />
                      </svg>
                      <span className="hidden sm:inline">
                        Privacy Protection: ON
                      </span>
                      <span className="sm:hidden">Protected</span>
                      <span className="text-xs bg-green-200 text-green-800 px-2 py-0.5 rounded-full">
                        Secure
                      </span>
                    </>
                  ) : (
                    <>
                      {/* Unlock Icon */}
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
                          d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z"
                        />
                      </svg>
                      <span className="hidden sm:inline">
                        Privacy Protection: OFF
                      </span>
                      <span className="sm:hidden">Standard</span>
                      <span className="text-xs bg-amber-200 text-amber-800 px-2 py-0.5 rounded-full">
                        Fast
                      </span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Tab content */}
          <div className="p-6">
            {activeTab === 'text' ? (
              // Text input tab
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Paste your content here
                </label>
                <textarea
                  value={textContent}
                  onChange={handleTextChange}
                  onPaste={handlePaste}
                  placeholder="Enter the text content you want to convert into a framework..."
                  className="w-full h-80 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                />
                <div className="mt-2 flex justify-between items-center text-sm text-gray-500">
                  <span>Maximum 10,000 characters</span>
                  <span
                    className={
                      textContent.length > 9000 ? 'text-orange-600' : ''
                    }
                  >
                    {textContent.length.toLocaleString()} / 10,000
                  </span>
                </div>
              </div>
            ) : (
              // File upload tab
              <div>
                {/* File drop zone */}
                <div
                  onDragEnter={handleDragEnter}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
                    isDragging
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <svg
                    className="w-16 h-16 mx-auto text-gray-400 mb-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                    />
                  </svg>

                  <p className="text-lg font-medium text-gray-700 mb-2">
                    Drag and drop your files here
                  </p>
                  <p className="text-sm text-gray-500 mb-4">or</p>

                  <label className="inline-block px-6 py-2 bg-blue-50 text-blue-600 rounded-lg font-medium hover:bg-blue-100 transition-colors cursor-pointer">
                    Choose Files
                    <input
                      type="file"
                      multiple
                      accept=".txt,.pdf,.doc,.docx"
                      onChange={handleFileSelect}
                      className="hidden"
                    />
                  </label>

                  <p className="text-xs text-gray-500 mt-4">
                    Supported formats: TXT, PDF, DOC, DOCX (Max 2MB per file)
                  </p>
                </div>

                {/* Selected files list */}
                {selectedFiles.length > 0 && (
                  <div className="mt-6">
                    <div className="flex justify-between items-center mb-3">
                      <h3 className="font-medium text-gray-900">
                        Selected Files ({selectedFiles.length})
                      </h3>
                      <button
                        onClick={clearAllFiles}
                        className="text-sm text-red-600 hover:text-red-800 font-medium"
                      >
                        Clear All
                      </button>
                    </div>

                    <div className="space-y-2 max-h-64 overflow-y-auto">
                      {selectedFiles.map((file, index) => (
                        <div
                          key={index}
                          className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200"
                        >
                          <div className="flex items-center space-x-3 flex-1 min-w-0">
                            <svg
                              className="w-8 h-8 text-blue-500 flex-shrink-0"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
                              <path
                                fillRule="evenodd"
                                d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"
                                clipRule="evenodd"
                              />
                            </svg>
                            <div className="min-w-0 flex-1">
                              <p className="font-medium text-gray-900 truncate">
                                {file.name}
                              </p>
                              <p className="text-sm text-gray-500">
                                {(file.size / 1024).toFixed(2)} KB
                              </p>
                            </div>
                          </div>

                          <button
                            onClick={() => removeFile(file.name)}
                            className="ml-3 p-1 text-gray-400 hover:text-red-600 transition-colors flex-shrink-0"
                          >
                            <svg
                              className="w-5 h-5"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
                              <path
                                fillRule="evenodd"
                                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                clipRule="evenodd"
                              />
                            </svg>
                          </button>
                        </div>
                      ))}
                    </div>

                    <div className="mt-3 text-sm text-gray-600">
                      Total: {(totalSize / 1024).toFixed(2)} KB
                    </div>

                    <p className="mt-2 text-xs text-gray-500">
                      Supports up to 10k characters or 2MB file size per file.
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="border-t border-gray-200 px-6 py-4 bg-gray-50 flex justify-end space-x-3 rounded-b-lg">
            <button
              onClick={handleCancel}
              className="px-5 py-2 text-gray-700 hover:text-gray-900 font-medium transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleGenerateDraft}
              disabled={isGenerating}
              className={`px-5 py-2 bg-blue-600 text-white rounded font-medium hover:bg-blue-700 transition-colors ${
                isGenerating ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {isGenerating ? 'Generating...' : 'Generate Draft'}
            </button>
          </div>
        </div>
      </div>

      {/* 🔒 Privacy Lock Confirmation dialog box */}
      <PrivacyLockDialog
        isOpen={showLockDialog}
        currentLockState={privacyLockEnabled}
        onConfirm={confirmLockToggle}
        onCancel={cancelLockToggle}
      />
    </div>
  )
}

/**
 * Convert the framework returned by the API into the editor's steps format.
 */
function convertToSteps(framework) {
  if (!framework) {
    return [
      {
        id: 'step-1',
        name: 'Planning Phase',
        description: 'Initial planning and setup',
        subSteps: [
          'Define objectives',
          'Identify stakeholders',
          'Allocate resources',
        ],
      },
    ]
  }

  // Step 1: Extract all necessary data sources (the order is important!)
  const rawMetadata = framework._raw?.metadata || {}
  const rawFramework = framework._raw?.framework || framework // ← Define this first

  const sections = rawMetadata.sections || []
  const workflowLayers = rawFramework.workflow_layers || [] // ← Then use it
  const coreMethod = rawFramework.core_method || []
  const facets = rawMetadata.facets || {}

  console.log('🔍 convertToSteps Debug:')
  console.log('  - sections:', sections.length)
  console.log('  - workflow_layers:', workflowLayers.length)
  console.log('  - core_method:', coreMethod.length)

  // Priority 1: Extract from _raw.metadata.sections (containing detailed information)
  if (sections.length > 0) {
    console.log('✅ Using sections from metadata')
    return sections.slice(0, 10).map((section, index) => {
      const title = section.title || `Framework ${index + 1}`
      const content = section.content || ''

      // Extract sub-steps from the content (segmented by sentence or key point).
      let subSteps = []
      if (content) {
        const lines = content
          .split(/[\n:,]/)
          .map(line => line.trim())
          .filter(line => line.length > 10 && line.length < 150)
          .slice(0, 6)

        subSteps = lines.length > 0 ? lines : [content.substring(0, 200)]
      }

      return {
        id: `framework-${index + 1}`,
        name: title,
        description: content.substring(0, 300),
        subSteps:
          subSteps.length > 0
            ? subSteps
            : ['Review and implement key activities'],
      }
    })
  }

  // Priority 2: Extract from workflow_layers (OpenAI's standard output)
  if (workflowLayers.length > 0) {
    console.log('✅ Using workflow_layers')
    return workflowLayers.map((layer, index) => {
      const layerName = layer.name || `Framework ${index + 1}`
      const layerFocus = layer.focus || ''
      const layerGuidance = layer.guidance || []

      return {
        id: `framework-${index + 1}`,
        type: 'framework', // This is marked as a framework type.
        source: 'generated', // Mark source (generated | recommended | custom)
        name: layerName,
        description: layerFocus,
        subSteps:
          layerGuidance.length > 0
            ? layerGuidance
            : [
                'Review key objectives',
                'Execute planned activities',
                'Validate outcomes',
              ],
      }
    })
  }

  // Priority 3: Extract from core_method
  if (coreMethod.length > 0) {
    console.log('✅ Using core_method')
    const steps = coreMethod.map((method, index) => {
      const layer = workflowLayers[index] || {}

      // Extract description
      let description = layer.focus || layer.description || ''

      // Extract sub-steps
      let subSteps = layer.guidance || []

      // If guidance is empty, try to extract it from facets.
      if (subSteps.length === 0) {
        const facetKey = method.toLowerCase().replace(/\s+/g, '_')
        const facet = facets[facetKey]

        if (facet && facet.items) {
          subSteps = facet.items.map(item => item.value || item).slice(0, 5)
        }
      }

      // If it's still empty, add a default item.
      if (subSteps.length === 0) {
        subSteps = [
          `Define objectives for ${method}`,
          `Execute key activities`,
          `Monitor and adjust approach`,
        ]
      }

      return {
        id: `framework-${index + 1}`,
        name: method,
        description: description || `Key activities for ${method}`,
        subSteps: subSteps,
      }
    })

    return steps
  }

  // Final default value
  console.warn('⚠️ No steps found, using default')
  return [
    {
      id: 'framework-1',
      name: 'Initial Phase',
      description: 'Start implementing the framework',
      subSteps: ['Plan', 'Execute', 'Review'],
    },
  ]
}

/**
 * Convert the framework returned by the API into the editor's Artefacts format.
 */
const convertToArtefacts = framework => {
  console.log('🔄 Converting framework artefacts:', framework)

  // ✅Prioritize using AI-generated primary_artefact
  if (framework.primary_artefact && framework.primary_artefact.name) {
    const primaryArtefact = framework.primary_artefact
    const outputsDeliverables = framework.outputs_deliverables || {}
    const optionalItems = outputsDeliverables.optional || []
    console.log('📊 Optional items raw data:', optionalItems)
    console.log('📊 First item type:', typeof optionalItems[0])
    console.log('📊 First item:', optionalItems[0])

    console.log('✅ Using AI-generated artefacts:', {
      primary: primaryArtefact.name,
      optional: optionalItems,
    })

    // ✅ Handling additional artifacts - Supports two formats
    const additional = optionalItems.map((item, idx) => {
      // Check if it is an object or a string
      if (typeof item === 'object' && item !== null) {
        // New format: object {name: "...", description: "..."}
        return {
          id: `art-${idx + 1}`,
          name: item.name || `Artefact ${idx + 1}`,
          description: item.description || '',
          selected: false,
        }
      } else if (typeof item === 'string') {
        // Old format: string "Artefact Name"
        return {
          id: `art-${idx + 1}`,
          name: item,
          description: '',
          selected: false,
        }
      } else {
        // Unknown format
        console.warn('Unknown artefact format:', item)
        return {
          id: `art-${idx + 1}`,
          name: 'Unknown Artefact',
          description: '',
          selected: false,
        }
      }
    })

    return {
      default: {
        type: primaryArtefact.name,
        description: primaryArtefact.purpose || '',
      },
      additional: additional,
    }
  }
  console.warn('⚠️ No primary_artefact found, using empty template')
  return {
    default: {
      type: 'Framework Document',
      description: 'Please regenerate the framework to get proper artefacts',
    },
    additional: [],
  }
}

/**
 * Convert the framework returned by the API into the editor's risk format.
 */
function convertToRisks(framework) {
  if (!framework) {
    return [
      {
        id: 'risk-1',
        title: 'Scope creep',
        description: 'Uncontrolled changes in project scope',
      },
    ]
  }

  // Prioritize extraction from _raw.metadata.risks (detailed description available).
  const rawRisks = framework._raw?.metadata?.risks || []

  if (rawRisks.length > 0) {
    return rawRisks.map((risk, index) => ({
      id: `risk-${index + 1}`,
      title: risk.title || risk.risk || risk.name || `Risk ${index + 1}`,
      description: risk.description || risk.impact || risk.evidence || '',
    }))
  }

  // Fallback: from risks_watchouts
  const risksWatchouts = framework.risks_watchouts || []

  const risks = risksWatchouts.map((risk, index) => {
    if (typeof risk === 'string') {
      return {
        id: `risk-${index + 1}`,
        title: risk,
        description: 'Monitor and mitigate to ensure framework success',
      }
    }

    if (typeof risk === 'object') {
      return {
        id: `risk-${index + 1}`,
        title: risk.title || risk.risk || `Risk ${index + 1}`,
        description: risk.description || risk.impact || '',
      }
    }

    return {
      id: `risk-${index + 1}`,
      title: `Risk ${index + 1}`,
      description: '',
    }
  })

  return risks.length > 0
    ? risks
    : [
        {
          id: 'risk-1',
          title: 'Implementation challenges',
          description: 'Unexpected obstacles during execution',
        },
      ]
}

/**
 * Convert the framework returned by the API into the editor's escalation format.
 */
function convertToEscalation(framework) {
  if (!framework) {
    return [
      {
        id: 'esc-1',
        trigger: 'Critical blocker',
        action: 'Escalate to project manager',
      },
    ]
  }

  const escalation = framework.escalation || []

  // Improvements: Handles more data formats
  /* eslint-disable no-unused-vars */
  const escalationPaths = escalation.map((esc, index) => {
    if (typeof esc === 'string') {
      return {
        id: `esc-${index + 1}`,
        trigger: esc,
        action: 'Escalate to appropriate specialist for resolution',
      }
    }

    if (typeof esc === 'object') {
      return {
        id: `esc-${index + 1}`,
        trigger:
          esc.trigger || esc.condition || esc.when || `Trigger ${index + 1}`,
        action: esc.action || esc.response || esc.what || 'Contact specialist',
      }
    }

    return {
      id: `esc-${index + 1}`,
      trigger: `Escalation ${index + 1}`,
      action: 'Take appropriate action',
    }
  })

  // If escalation is too low, generate some from risks.
  if (escalationPaths.length < 2) {
    const rawRisks = framework._raw?.metadata?.risks || []
    rawRisks.slice(0, 3).forEach((risk, index) => {
      const riskTitle = risk.title || risk.risk || ''
      if (riskTitle) {
        escalationPaths.push({
          id: `esc-${escalationPaths.length + 1}`,
          trigger: `If ${riskTitle.toLowerCase()} occurs`,
          action: 'Escalate to project lead or steering committee',
        })
      }
    })
  }

  return escalationPaths.length > 0
    ? escalationPaths
    : [
        {
          id: 'esc-1',
          trigger: 'Major issue identified',
          action: 'Escalate to management',
        },
      ]
}

export default CreateFramework
