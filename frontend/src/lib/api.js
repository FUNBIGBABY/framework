/**
 * API Client - backend REST with cookie sessions.
 */

function getApiBaseUrl() {
  const hostname = window.location.hostname

  // Production environment - using relative paths.
  if (hostname === 'expert.valorie.ai' || hostname.endsWith('.valorie.ai')) {
    return ''
  }

  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
}

const API_BASE_URL = getApiBaseUrl()

/**
 * Phase 7 owns semantic tenant/domain cleanup. Phase 6 Round 1 keeps this
 * helper for legacy route generation only; it is not sent as request identity.
 */
function getCurrentTenantId() {
  const hostname = window.location.hostname

  const tenantMatch = hostname.match(/^([a-z0-9-]+)\.valorie\.ai$/)
  if (tenantMatch) return tenantMatch[1]

  const pathMatch = window.location.pathname.match(/^\/([a-z0-9-]+)\//)
  if (pathMatch) return pathMatch[1]

  return null
}

class APIError extends Error {
  constructor(message, status, data) {
    super(message)
    this.name = 'APIError'
    this.status = status
    this.data = data
  }
}

function getAuthHeaders(headers = {}) {
  return { ...headers }
}

function getApiUrl(url) {
  return /^https?:\/\//i.test(url) ? url : `${API_BASE_URL}${url}`
}

const AUTH_REFRESH_SKIP_PATHS = new Set([
  '/api/users/login',
  '/api/users/logout',
  '/api/users/refresh',
  '/api/users/register',
])

function getRequestPath(url) {
  try {
    return new URL(getApiUrl(url), window.location.origin).pathname
  } catch {
    return String(url)
  }
}

function shouldRefreshAfterResponse(url, response, skipAuthRefresh) {
  if (skipAuthRefresh || response.status !== 401) return false
  return !AUTH_REFRESH_SKIP_PATHS.has(getRequestPath(url))
}

async function refreshSessionForRetry() {
  const response = await fetch(getApiUrl('/api/users/refresh'), {
    method: 'POST',
    credentials: 'include',
  })

  return response.ok
}

function notifyUnauthorized() {
  if (typeof window === 'undefined') return

  window.dispatchEvent(new CustomEvent('auth:unauthorized'))

  if (window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}

async function readJson(response) {
  try {
    return await response.json()
  } catch {
    return {}
  }
}

async function apiFetch(url, options = {}) {
  const {
    headers,
    suppressAuthRedirect = false,
    skipAuthRefresh = false,
    ...rest
  } = options

  const requestOptions = {
    ...rest,
    credentials: 'include',
    headers: getAuthHeaders(headers),
  }

  let response = await fetch(getApiUrl(url), requestOptions)

  if (shouldRefreshAfterResponse(url, response, skipAuthRefresh)) {
    const refreshed = await refreshSessionForRetry()
    if (refreshed) {
      response = await fetch(getApiUrl(url), requestOptions)
    }
  }

  if (
    !suppressAuthRedirect &&
    (response.status === 401 || response.status === 403)
  ) {
    notifyUnauthorized()
  }

  return response
}

async function apiRequest(url, options = {}) {
  try {
    const response = await apiFetch(url, options)
    const data = await readJson(response)

    if (!response.ok) {
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
  const response = await fetch(getApiUrl('/api/users/login'), {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })

  const data = await readJson(response)

  if (!response.ok) {
    throw new APIError(
      data.detail || data.error || 'Login failed',
      response.status,
      data
    )
  }

  return data
}

export async function refreshBackendSession(options = {}) {
  return await apiRequest('/api/users/refresh', {
    method: 'POST',
    suppressAuthRedirect: Boolean(options.suppressAuthRedirect),
    skipAuthRefresh: true,
  })
}

export async function getCurrentBackendUser(options = {}) {
  return await apiRequest('/api/users/me', {
    suppressAuthRedirect: Boolean(options.suppressAuthRedirect),
  })
}

export async function logoutWithBackend() {
  return await apiRequest('/api/users/logout', {
    method: 'POST',
  })
}

export async function generateFrameworkFromText(
  text,
  useGlobalLLM = true,
  model = undefined,
  reasoning = false
) {
  const payload = {
    text,
    use_global_llm: useGlobalLLM,
  }
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

export async function generateFrameworkFromFile(
  file,
  useGlobalLLM = true,
  model = undefined,
  reasoning = false
) {
  const formData = new FormData()
  formData.append('file', file)

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

  const data = await readJson(response)
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

export async function generateFrameworkFromFiles(
  files,
  useGlobalLLM = true,
  model = undefined,
  reasoning = false
) {
  const formData = new FormData()
  files.forEach(file => formData.append('files', file))

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

  const data = await readJson(response)
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

export async function getMyFrameworks() {
  return await apiRequest('/api/frameworks/my-frameworks')
}

export async function getMyFrameworksByFamily() {
  return await apiRequest('/api/frameworks/my-frameworks/by-family')
}

export async function getFrameworkById(frameworkId) {
  return await apiRequest(`/api/frameworks/${frameworkId}`)
}

export async function updateFramework(frameworkId, frameworkData) {
  return await apiRequest(`/api/frameworks/${frameworkId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(frameworkData),
  })
}

export async function deleteFramework(frameworkId) {
  return await apiRequest(`/api/frameworks/${frameworkId}`, {
    method: 'DELETE',
  })
}

export async function saveFramework(frameworkId, frameworkData) {
  return await updateFramework(frameworkId, frameworkData)
}

export async function getFramework(frameworkId) {
  return await getFrameworkById(frameworkId)
}

export async function checkHealth() {
  return apiRequest('/api/frameworks/health')
}

export async function checkBackendStatus() {
  try {
    const response = await fetch(getApiUrl('/health'), {
      method: 'GET',
      credentials: 'include',
    })
    return response.ok
  } catch {
    return false
  }
}

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
  getCurrentTenantId,
}
