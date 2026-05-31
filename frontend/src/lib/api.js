/**
 * API Client - Supports multi-domain architecture
 */
import { auth } from './firebase'

/**
 * Dynamically obtain API Base URL
 */
function getApiBaseUrl() {
  const hostname = window.location.hostname

  // Production environment - using relative paths
  if (hostname === 'expert.valorie.ai' || hostname.endsWith('.valorie.ai')) {
    return ''
  }

  // Development Environment
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
}

const API_BASE_URL = getApiBaseUrl()

/**
 * Get the current tenant ID
 */
function getCurrentTenantId() {
  const hostname = window.location.hostname

  // Extract from subdomain
  const tenantMatch = hostname.match(/^([a-z0-9-]+)\.valorie\.ai$/)
  if (tenantMatch) return tenantMatch[1]

  // Extract from URL path (local development)
  const pathMatch = window.location.pathname.match(/^\/([a-z0-9-]+)\//)
  if (pathMatch) return pathMatch[1]

  return null
}

/**
 * API Error Class
 */
class APIError extends Error {
  constructor(message, status, data) {
    super(message)
    this.name = 'APIError'
    this.status = status
    this.data = data
  }
}

/**
 * Obtain authentication token
 */
function getAuthToken() {
  return localStorage.getItem('access_token')
}

function getAuthHeaders(headers = {}) {
  const token = getAuthToken()
  const tenantId = getCurrentTenantId()
  const nextHeaders = { ...headers }

  if (token) nextHeaders.Authorization = `Bearer ${token}`
  if (tenantId) nextHeaders['X-Tenant-ID'] = tenantId

  return nextHeaders
}

function getApiUrl(url) {
  return /^https?:\/\//i.test(url) ? url : `${API_BASE_URL}${url}`
}

async function apiFetch(url, options = {}) {
  const { headers, ...rest } = options

  return fetch(getApiUrl(url), {
    ...rest,
    headers: getAuthHeaders(headers),
  })
}

/**
 * Get Firebase User ID
 */
function getFirebaseUserId() {
  const user = auth.currentUser
  return user ? user.uid : null
}

/**
 * General API Requests
 */
async function apiRequest(url, options = {}) {
  try {
    const response = await apiFetch(url, options)
    let data = {}

    try {
      data = await response.json()
    } catch {
      data = {}
    }

    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
        const hostname = window.location.hostname
        if (
          hostname.endsWith('.valorie.ai') &&
          hostname !== 'expert.valorie.ai'
        ) {
          window.location.href = 'https://expert.valorie.ai/login'
        } else {
          window.location.href = '/login'
        }
      }
      throw new APIError(
        data.detail || data.error || 'Request failed',
        response.status,
        data
      )
    }

    return data
  } catch (error) {
    if (error instanceof APIError) throw error
    throw new APIError(error.message || 'Network error occurred', 0, null)
  }
}

export async function loginWithBackend(email, password) {
  let data = null

  const response = await fetch(`${API_BASE_URL}/api/users/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })

  try {
    data = await response.json()
  } catch {
    data = {}
  }

  if (!response.ok) {
    throw new APIError(
      data.detail || data.error || 'Login failed',
      response.status,
      data
    )
  }

  return data
}

/**
 * From text generation framework
 */
export async function generateFrameworkFromText(
  text,
  useGlobalLLM = true,
  model = undefined,
  reasoning = false
) {
  const userId = getFirebaseUserId()
  const tenantId = getCurrentTenantId()
  const payload = {
    text,
    use_global_llm: useGlobalLLM,
  }
  if (userId) payload.user_id = userId
  if (tenantId) payload.tenant_id = tenantId
  if (model) payload.model = model
  if (reasoning) payload.reasoning = true

  const response = await apiRequest('/api/frameworks/generate-from-text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.success) {
    throw new APIError(
      response.error || 'Framework generation failed',
      500,
      response
    )
  }
  return response
}

/**
 * From file generation framework
 */
export async function generateFrameworkFromFile(
  file,
  useGlobalLLM = true,
  model = undefined,
  reasoning = false
) {
  const formData = new FormData()
  formData.append('file', file)

  const userId = getFirebaseUserId()
  const tenantId = getCurrentTenantId()
  if (userId) formData.append('user_id', userId)
  if (tenantId) formData.append('tenant_id', tenantId)

  const params = new URLSearchParams({
    use_global_llm: String(useGlobalLLM),
  })
  if (model) params.set('model', model)
  if (reasoning) params.set('reasoning', 'true')

  const response = await apiFetch(
    `/api/frameworks/generate-from-file?${params.toString()}`,
    {
      method: 'POST',
      body: formData,
    }
  )

  const data = await response.json()
  if (!response.ok) {
    throw new APIError(
      data.detail || data.error || 'Framework generation failed',
      response.status,
      data
    )
  }
  if (!data.success) {
    throw new APIError(data.error || 'Framework generation failed', 500, data)
  }
  return data
}

/**
 * Generate a framework from multiple files
 */
export async function generateFrameworkFromFiles(
  files,
  useGlobalLLM = true,
  model = undefined,
  reasoning = false
) {
  const formData = new FormData()
  files.forEach(file => formData.append('files', file))

  const userId = getFirebaseUserId()
  const tenantId = getCurrentTenantId()
  if (userId) formData.append('user_id', userId)
  if (tenantId) formData.append('tenant_id', tenantId)

  const params = new URLSearchParams({
    use_global_llm: String(useGlobalLLM),
  })
  if (model) params.set('model', model)
  if (reasoning) params.set('reasoning', 'true')

  const response = await apiFetch(
    `/api/frameworks/generate-from-files?${params.toString()}`,
    {
      method: 'POST',
      body: formData,
    }
  )

  const data = await response.json()
  if (!response.ok) {
    throw new APIError(
      data.detail || data.error || 'Framework generation failed',
      response.status,
      data
    )
  }
  if (!data.success) {
    throw new APIError(data.error || 'Framework generation failed', 500, data)
  }
  return data
}

/**
 * Get all frameworks of the user
 */
export async function getMyFrameworks() {
  const userId = getFirebaseUserId()
  const tenantId = getCurrentTenantId()

  const params = new URLSearchParams()
  if (userId) params.set('user_id', userId)
  if (tenantId) params.set('tenant_id', tenantId)

  const query = params.toString()
  const url = `/api/frameworks/my-frameworks${query ? `?${query}` : ''}`

  return await apiRequest(url)
}

/**
 * Get frameworks by family
 */
export async function getMyFrameworksByFamily() {
  const userId = getFirebaseUserId()
  const tenantId = getCurrentTenantId()

  const params = new URLSearchParams()
  if (userId) params.set('user_id', userId)
  if (tenantId) params.set('tenant_id', tenantId)

  const query = params.toString()
  const url = `/api/frameworks/my-frameworks/by-family${query ? `?${query}` : ''}`

  return await apiRequest(url)
}

/**
 * Get a single framework
 */
export async function getFrameworkById(frameworkId) {
  return await apiRequest(`/api/frameworks/${frameworkId}`)
}

/**
 * Update framework
 */
export async function updateFramework(frameworkId, frameworkData) {
  return await apiRequest(`/api/frameworks/${frameworkId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(frameworkData),
  })
}

/**
 * Delete framework
 */
export async function deleteFramework(frameworkId) {
  return await apiRequest(`/api/frameworks/${frameworkId}`, {
    method: 'DELETE',
  })
}

/**
 * Save Frame
 */
export async function saveFramework(frameworkId, frameworkData) {
  return await updateFramework(frameworkId, frameworkData)
}

/**
 * Get framework details
 */
export async function getFramework(frameworkId) {
  return await getFrameworkById(frameworkId)
}

/**
 * Health check
 */
export async function checkHealth() {
  return apiRequest('/api/frameworks/health')
}

/**
 * Check backend status
 */
export async function checkBackendStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      timeout: 3000,
    })
    return response.ok
  } catch {
    return false
  }
}

/**
 * API endpoint configuration
 */
export const API_ENDPOINTS = {
  EXPORT_MARKDOWN: `${API_BASE_URL}/api/frameworks/export-markdown`,
  EXPORT_DOCX: `${API_BASE_URL}/api/frameworks/export-docx`,
  REGENERATE: `${API_BASE_URL}/api/frameworks/regenerate`,
  AI_MERGE: `${API_BASE_URL}/api/frameworks/ai-merge`,
  AI_FILL: `${API_BASE_URL}/api/frameworks/ai-fill`,
  PUSH_FRAMEWORK: `${API_BASE_URL}/api/frameworks/push-framework`,
}

export default API_ENDPOINTS
export {
  APIError,
  API_BASE_URL,
  apiFetch,
  getApiBaseUrl,
  getAuthHeaders,
  getAuthToken,
  getCurrentTenantId,
}
