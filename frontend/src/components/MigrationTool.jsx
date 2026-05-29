import { useState } from 'react'
import { checkMigrationStatus, runFullMigration } from '../migrate-data'

function MigrationTool() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)
  const [log, setLog] = useState([])
  const [migrationComplete, setMigrationComplete] = useState(false)

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString()
    setLog(prev => [...prev, { message, type, timestamp }])
    console.log(`[${timestamp}] ${message}`)
  }

  const handleCheckStatus = async () => {
    setLoading(true)
    setLog([])
    addLog('🔍 Check data status...', 'info')

    try {
      const result = await checkMigrationStatus()
      setStatus(result)
      addLog('✅ Status check complete', 'success')

      // Check if the migration has been completed.
      if (
        result.users.needMigration === 0 &&
        result.frameworks.needMigration === 0
      ) {
        setMigrationComplete(true)
        addLog('🎉 Check if the migration has been completed.', 'success')
      } else {
        setMigrationComplete(false)
      }
    } catch (error) {
      addLog(`❌ Check failed: ${error.message}`, 'error')
      console.error('Status check error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRunMigration = async () => {
    const confirmed = window.confirm(
      '⚠️ Are you sure you want to start the migration? \n\nThis operation will modify the data in the database.\n' +
        'It is recommended to back up your Firebase data first.\n\n' +
        'Click "OK" to continue.'
    )

    if (!confirmed) {
      return
    }

    setLoading(true)
    setLog([])
    addLog('🚀 Start the full migration...', 'info')

    try {
      addLog('Step 1/2: Migrate user data...', 'info')
      await new Promise(resolve => setTimeout(resolve, 500)) // A short delay to see the logs

      const result = await runFullMigration()

      if (result.success) {
        addLog(
          `✅ User migration complete: ${result.users.updated} users have been updated, ${result.users.skipped} users have been skipped.`,
          'success'
        )
        addLog(
          `✅ Framework migration complete: ${result.frameworks.updated} items have been updated, ${result.frameworks.skipped} items have been skipped.`,
          'success'
        )
        addLog('🎉 Migration successful!', 'success')

        if (
          result.users.errors?.length > 0 ||
          result.frameworks.errors?.length > 0
        ) {
          addLog(
            '⚠️ Some project migrations failed; please check the console.',
            'warning'
          )
        }

        // Recheck status
        await handleCheckStatus()
      }
    } catch (error) {
      addLog(`❌ Migration failed: ${error.message}`, 'error')
      console.error('Migration error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-6">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
              <svg
                className="w-6 h-6 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Data migration tools
              </h1>
              <p className="text-gray-600 mt-1">
                Add necessary new fields to existing users and frameworks
              </p>
            </div>
          </div>
        </div>

        {/* Warning */}
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-yellow-400"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">
                Important Note
              </h3>
              <div className="mt-2 text-sm text-yellow-700">
                <ul className="list-disc list-inside space-y-1">
                  <li>This tool modifies data in the Firestore database.</li>
                  <li>
                    It is recommended to back up your data in the Firebase
                    Console first.
                  </li>
                  <li>
                    Please do not close this page during the migration process.
                  </li>
                  <li>
                    All old frames will be assigned to the "legacy" tenant.
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
            <svg
              className="w-6 h-6 mr-2 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            Operating steps
          </h2>

          <div className="space-y-4">
            <button
              onClick={handleCheckStatus}
              disabled={loading}
              className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            >
              {loading && !status ? (
                <>
                  <svg
                    className="animate-spin h-5 w-5 mr-2"
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
                  During inspection...
                </>
              ) : (
                <>
                  <svg
                    className="w-5 h-5 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                  Step 1: Check migration status
                </>
              )}
            </button>

            {status && !migrationComplete && (
              <button
                onClick={handleRunMigration}
                disabled={loading}
                className="w-full px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {loading && status ? (
                  <>
                    <svg
                      className="animate-spin h-5 w-5 mr-2"
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
                    Migrating in progress...
                  </>
                ) : (
                  <>
                    <svg
                      className="w-5 h-5 mr-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 10V3L4 14h7v7l9-11h-7z"
                      />
                    </svg>
                    Step 2: Begin the migration
                  </>
                )}
              </button>
            )}

            {migrationComplete && (
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center">
                  <svg
                    className="w-6 h-6 text-green-600 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <span className="text-green-800 font-medium">
                    🎉 All data migration is complete!
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Status Display */}
        {status && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
              <svg
                className="w-6 h-6 mr-2 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
              Migration Status Report
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Users */}
              <div className="border border-gray-200 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <svg
                    className="w-8 h-8 text-blue-500 mr-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                    />
                  </svg>
                  <h3 className="font-semibold text-gray-900 text-lg">
                    User data
                  </h3>
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">total:</span>
                    <span className="font-semibold text-gray-900">
                      {status.users.total}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">Migrated:</span>
                    <span className="font-semibold text-green-600">
                      {status.users.migrated}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-2">
                    <span className="text-gray-600">Migration required:</span>
                    <span
                      className={`font-semibold ${status.users.needMigration > 0 ? 'text-yellow-600' : 'text-green-600'}`}
                    >
                      {status.users.needMigration}
                    </span>
                  </div>
                </div>
              </div>

              {/* Frameworks */}
              <div className="border border-gray-200 rounded-lg p-6">
                <div className="flex items-center mb-4">
                  <svg
                    className="w-8 h-8 text-purple-500 mr-3"
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
                  <h3 className="font-semibold text-gray-900 text-lg">
                    Framework data
                  </h3>
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">total:</span>
                    <span className="font-semibold text-gray-900">
                      {status.frameworks.total}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">Migrated:</span>
                    <span className="font-semibold text-green-600">
                      {status.frameworks.migrated}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-2">
                    <span className="text-gray-600">Migration required:</span>
                    <span
                      className={`font-semibold ${status.frameworks.needMigration > 0 ? 'text-yellow-600' : 'text-green-600'}`}
                    >
                      {status.frameworks.needMigration}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Log Display */}
        {log.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <svg
                className="w-6 h-6 mr-2 text-blue-600"
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
              Operation Log
            </h2>

            <div className="bg-gray-900 rounded-lg p-4 max-h-96 overflow-y-auto font-mono text-sm">
              {log.map((entry, index) => (
                <div
                  key={index}
                  className={`mb-1 ${
                    entry.type === 'error'
                      ? 'text-red-400'
                      : entry.type === 'success'
                        ? 'text-green-400'
                        : entry.type === 'warning'
                          ? 'text-yellow-400'
                          : 'text-gray-300'
                  }`}
                >
                  <span className="text-gray-500">[{entry.timestamp}]</span>{' '}
                  {entry.message}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="bg-blue-50 rounded-lg p-6 mt-6">
          <h3 className="font-semibold text-blue-900 mb-3 flex items-center">
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            Instructions for use
          </h3>
          <ol className="list-decimal list-inside space-y-2 text-blue-800 text-sm">
            <li>
              Click "Check Migration Status" to view the data that needs to be
              migrated.
            </li>
            <li>
              After confirming that everything is correct, click "Start
              Migration" to execute the migration operation.
            </li>
            <li>
              After the migration is complete, all old frameworks will be
              assigned to the "legacy" tenant.
            </li>
            <li>
              You can create a formal tenant later in the tenant settings.
            </li>
            <li>You can close this page after the migration is complete.</li>
          </ol>
        </div>
      </div>
    </div>
  )
}

export default MigrationTool
