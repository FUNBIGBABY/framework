import { Link } from 'react-router-dom'

function Signup() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-4">
            <span className="text-white font-bold text-2xl">V</span>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Registration Disabled
          </h2>
          <p className="text-gray-600">
            Accounts are created by an administrator.
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <p className="text-sm text-gray-600 mb-6">
            Use your existing account, or ask the administrator to create one
            through the backend seed/admin workflow.
          </p>
          <Link
            to="/login"
            className="inline-flex justify-center w-full py-3 px-4 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            Sign In
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Signup
