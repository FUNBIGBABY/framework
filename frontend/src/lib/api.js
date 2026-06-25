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

function isPlainObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value)
}

function parseJsonIfNeeded(value, fallback) {
  if (value === undefined || value === null || value === '') return fallback
  if (typeof value !== 'string') return value

  try {
    return JSON.parse(value)
  } catch {
    return fallback
  }
}

function normalizeArtefacts(artefacts) {
  if (!isPlainObject(artefacts)) {
    return {
      default: {
        type: 'Framework Document',
        description: '',
      },
      additional: [],
    }
  }

  return {
    ...artefacts,
    default: {
      type: String(artefacts.default?.type || 'Framework Document'),
      description: String(artefacts.default?.description || ''),
    },
    additional: Array.isArray(artefacts.additional)
      ? artefacts.additional.map((artefact, index) => {
          if (isPlainObject(artefact)) {
            return {
              id: artefact.id || `art-${index + 1}`,
              name: String(artefact.name || ''),
              description: String(artefact.description || ''),
              selected: Boolean(artefact.selected),
            }
          }

          return {
            id: `art-${index + 1}`,
            name: String(artefact || 'Unknown Artefact'),
            description: '',
            selected: false,
          }
        })
      : [],
  }
}

function normalizePreviewArtefacts(artefacts) {
  if (!Array.isArray(artefacts)) return []

  return artefacts.slice(0, 3).map(artefact => {
    if (isPlainObject(artefact)) {
      return {
        name: String(artefact.name || ''),
        description: String(artefact.description || '').substring(0, 100),
      }
    }

    return {
      name: String(artefact || 'Unknown Artefact'),
      description: '',
    }
  })
}

function normalizeJsonContainer(value, fallback) {
  const parsed = parseJsonIfNeeded(value, fallback)
  if (Array.isArray(parsed) || isPlainObject(parsed)) return parsed
  return fallback
}

function stripArtefactResourceFields(artefactData = {}) {
  const resourceFields = new Set([
    'id',
    'name',
    ['framework', 'id'].join('_'),
    ['user', 'id'].join('_'),
    ['creator', 'id'].join('_'),
    ['tenant', 'id'].join('_'),
    ['X', 'Tenant-ID'].join('-'),
    'artefact_type',
    'metadata_json',
    'content_json',
    'ord',
    'created_at',
    'updated_at',
    '_resource',
  ])

  return Object.fromEntries(
    Object.entries(artefactData).filter(([key]) => !resourceFields.has(key))
  )
}

export function normalizeFrameworkArtefact(artefact = {}) {
  const content = normalizeJsonContainer(artefact.content_json, {})
  const metadata = normalizeJsonContainer(artefact.metadata_json, {})
  const contentObject = isPlainObject(content) ? content : {}

  return {
    ...contentObject,
    id: artefact.id,
    name: String(artefact.name || contentObject.name || 'Untitled Artefact'),
    artefact_type: String(
      artefact.artefact_type || contentObject.artefact_type || 'custom'
    ),
    ord: Number(artefact.ord || 0),
    metadata_json: metadata,
    _resource: artefact,
  }
}

function buildArtefactPayload(artefactData = {}, { forCreate = false } = {}) {
  const payload = {}

  if (forCreate || hasOwn(artefactData, 'name')) {
    const name = String(artefactData.name || '').trim()
    payload.name = name || 'Untitled Artefact'
  }

  if (forCreate || hasOwn(artefactData, 'artefact_type')) {
    payload.artefact_type = String(artefactData.artefact_type || 'custom')
  }

  if (hasOwn(artefactData, 'content_json')) {
    payload.content_json = normalizeJsonContainer(artefactData.content_json, {})
  } else {
    const contentJson = stripArtefactResourceFields(artefactData)
    if (forCreate || Object.keys(contentJson).length) {
      payload.content_json = contentJson
    }
  }

  if (hasOwn(artefactData, 'metadata_json')) {
    payload.metadata_json = normalizeJsonContainer(artefactData.metadata_json, {})
  } else if (forCreate) {
    payload.metadata_json = {}
  }

  if (forCreate || hasOwn(artefactData, 'ord')) {
    const ord = Number(artefactData.ord)
    payload.ord = Number.isFinite(ord) ? ord : 0
  }

  return payload
}

function getRawFramework(data) {
  return parseJsonIfNeeded(data?._raw ?? data?.rawFramework, undefined)
}

function hasOwn(value, key) {
  return Object.prototype.hasOwnProperty.call(value, key)
}

function hasMeaningfulRawFramework(rawFramework) {
  if (rawFramework === undefined || rawFramework === null || rawFramework === '') {
    return false
  }

  if (isPlainObject(rawFramework)) {
    return Object.keys(rawFramework).length > 0
  }

  if (Array.isArray(rawFramework)) {
    return rawFramework.length > 0
  }

  return true
}

function getExplicitRawFramework(frameworkData = {}) {
  if (hasOwn(frameworkData, '_raw')) {
    return parseJsonIfNeeded(frameworkData._raw, undefined)
  }

  if (hasOwn(frameworkData, 'rawFramework')) {
    return parseJsonIfNeeded(frameworkData.rawFramework, undefined)
  }

  return undefined
}

function addRawFrameworkIfPresent(payload, frameworkData) {
  const rawFramework = getExplicitRawFramework(frameworkData)
  if (hasMeaningfulRawFramework(rawFramework)) {
    payload._raw = rawFramework
  }
}

function buildFrameworkCreatePayload(frameworkData = {}) {
  const metadata = isPlainObject(frameworkData.metadata)
    ? frameworkData.metadata
    : {}

  const payload = {
    title: metadata.title || frameworkData.title || 'Untitled Framework',
    version: metadata.version || frameworkData.version || '1.0.0',
    family: frameworkData.family || 'Other',
    confidence: Number(frameworkData.confidence || 0),
    metadata,
    steps: Array.isArray(frameworkData.steps) ? frameworkData.steps : [],
    artefacts: isPlainObject(frameworkData.artefacts)
      ? frameworkData.artefacts
      : {},
    risks: Array.isArray(frameworkData.risks) ? frameworkData.risks : [],
    escalation: Array.isArray(frameworkData.escalation)
      ? frameworkData.escalation
      : [],
  }

  addRawFrameworkIfPresent(payload, frameworkData)

  if (frameworkData.pov) {
    payload.pov = frameworkData.pov
  }

  return payload
}

function setIfProvided(payload, frameworkData, field) {
  if (hasOwn(frameworkData, field) && frameworkData[field] !== undefined) {
    payload[field] = frameworkData[field]
  }
}

function buildFrameworkUpdatePayload(frameworkData = {}) {
  const payload = {}

  setIfProvided(payload, frameworkData, 'title')
  setIfProvided(payload, frameworkData, 'version')
  setIfProvided(payload, frameworkData, 'family')
  setIfProvided(payload, frameworkData, 'pov')

  if (hasOwn(frameworkData, 'confidence')) {
    const confidence = frameworkData.confidence
    if (confidence === null) {
      payload.confidence = null
    } else if (confidence !== undefined && confidence !== '') {
      const numericConfidence = Number(confidence)
      payload.confidence = Number.isFinite(numericConfidence)
        ? numericConfidence
        : confidence
    }
  }

  if (hasOwn(frameworkData, 'metadata') && frameworkData.metadata !== undefined) {
    payload.metadata = frameworkData.metadata
  }
  if (hasOwn(frameworkData, 'steps') && frameworkData.steps !== undefined) {
    payload.steps = frameworkData.steps
  }
  if (hasOwn(frameworkData, 'artefacts') && frameworkData.artefacts !== undefined) {
    payload.artefacts = frameworkData.artefacts
  }
  if (hasOwn(frameworkData, 'risks') && frameworkData.risks !== undefined) {
    payload.risks = frameworkData.risks
  }
  if (hasOwn(frameworkData, 'escalation') && frameworkData.escalation !== undefined) {
    payload.escalation = frameworkData.escalation
  }

  addRawFrameworkIfPresent(payload, frameworkData)

  return payload
}

export function normalizeFrameworkSummary(framework = {}) {
  const createdAt = framework.created_at || framework.createdAt
  const updatedAt = framework.updated_at || framework.updatedAt || createdAt
  const publishedAt = framework.published_at || framework.publishedAt || null

  return {
    id: framework.id,
    title: framework.title || 'Untitled Framework',
    version: framework.version || '1.0.0',
    family: framework.family || 'Other',
    confidence: Number(framework.confidence || 0),
    category: framework.category || framework.family || 'Other',
    tags: Array.isArray(framework.tags) ? framework.tags : [],
    created_at: createdAt,
    updated_at: updatedAt,
    published_at: publishedAt,
    publishedAt,
    preview_artefacts: normalizePreviewArtefacts(framework.preview_artefacts),
    isPublic: Boolean(framework.is_public ?? framework.isPublic),
    publishedToOrganization: Boolean(framework.publishedToOrganization),
    canManage: true,
  }
}

export function normalizePublicFramework(framework = {}) {
  const publishedAt = framework.published_at || framework.publishedAt || null
  const updatedAt = framework.updated_at || framework.updatedAt || null
  const previewArtefacts =
    framework.preview_artefacts ||
    framework.previewArtefacts ||
    framework.artefacts?.additional

  return {
    id: framework.id,
    title: framework.title || 'Untitled Framework',
    version: framework.version || '1.0.0',
    family: framework.family || 'Other',
    confidence: Number(framework.confidence || 0),
    category: framework.category || framework.family || 'Other',
    tags: Array.isArray(framework.tags)
      ? framework.tags.map(tag => String(tag)).filter(Boolean)
      : [],
    published_at: publishedAt,
    publishedAt,
    updated_at: updatedAt,
    updatedAt,
    preview_artefacts: normalizePreviewArtefacts(previewArtefacts),
    isPublic: true,
    canManage: false,
  }
}

export function normalizeFrameworkForEditor(framework = {}) {
  const metadata = isPlainObject(framework.metadata) ? framework.metadata : {}
  const updatedAt = framework.updated_at || framework.updatedAt

  return {
    id: framework.id,
    title: framework.title || metadata.title || 'New Framework',
    version: framework.version || metadata.version || '1.0.0',
    family: framework.family || 'Other',
    confidence: Number(framework.confidence || 0),
    metadata: {
      ...metadata,
      title: metadata.title || framework.title || 'New Framework',
      version: metadata.version || framework.version || '1.0.0',
      tags: metadata.tags || '',
      lastUpdated:
        metadata.lastUpdated || metadata.last_updated || updatedAt || '',
    },
    steps: Array.isArray(framework.steps) ? framework.steps : [],
    artefacts: normalizeArtefacts(framework.artefacts),
    risks: Array.isArray(framework.risks) ? framework.risks : [],
    escalation: Array.isArray(framework.escalation)
      ? framework.escalation
      : [],
    _raw: getRawFramework(framework),
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
  const frameworks = await apiRequest('/api/frameworks/my-frameworks')
  return Array.isArray(frameworks)
    ? frameworks.map(normalizeFrameworkSummary)
    : []
}

export async function getMyFrameworksByFamily() {
  return await apiRequest('/api/frameworks/my-frameworks/by-family')
}

export async function getPublicFrameworks(options = {}) {
  const {
    cursor = '',
    limit = 20,
    suppressAuthRedirect = false,
  } = options
  const params = new URLSearchParams()

  if (cursor) params.set('cursor', cursor)
  if (limit) params.set('limit', String(limit))

  const queryString = params.toString()
  const response = await apiRequest(
    `/api/frameworks/public${queryString ? `?${queryString}` : ''}`,
    { suppressAuthRedirect }
  )

  return {
    items: Array.isArray(response.items)
      ? response.items.map(normalizePublicFramework)
      : [],
    next_cursor: response.next_cursor || null,
    limit: response.limit || limit,
  }
}

export async function getFrameworkById(frameworkId) {
  const framework = await apiRequest(`/api/frameworks/${frameworkId}`)
  return normalizeFrameworkForEditor(framework)
}

export async function getFrameworkBinding(frameworkId) {
  return await apiRequest(`/api/frameworks/${frameworkId}/binding`)
}

export async function createFramework(frameworkData) {
  return await apiRequest('/api/frameworks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(buildFrameworkCreatePayload(frameworkData)),
  })
}

export async function updateFramework(frameworkId, frameworkData) {
  return await apiRequest(`/api/frameworks/${frameworkId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(buildFrameworkUpdatePayload(frameworkData)),
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

export async function regenerateFramework(frameworkData, useLocal = false) {
  return await apiRequest('/api/frameworks/regenerate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      framework: buildFrameworkCreatePayload(frameworkData),
      use_local: Boolean(useLocal),
    }),
  })
}

export async function mergeFrameworksWithAI(frameworks) {
  return await apiRequest('/api/frameworks/ai-merge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ frameworks }),
  })
}

export async function publishFramework(frameworkId, options = {}) {
  const payload = {}

  if (options.category !== undefined) payload.category = options.category
  if (options.version !== undefined) payload.version = options.version

  if (options.tags !== undefined) {
    payload.tags = Array.isArray(options.tags)
      ? options.tags
      : String(options.tags)
          .split(',')
          .map(tag => tag.trim())
          .filter(Boolean)
  }

  return await apiRequest(`/api/frameworks/${frameworkId}/publish`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export async function unpublishFramework(frameworkId) {
  return await apiRequest(`/api/frameworks/${frameworkId}/unpublish`, {
    method: 'POST',
  })
}

export async function listFrameworkArtefacts(frameworkId) {
  const artefacts = await apiRequest(`/api/frameworks/${frameworkId}/artefacts`)
  return Array.isArray(artefacts)
    ? artefacts.map(normalizeFrameworkArtefact)
    : []
}

export async function createFrameworkArtefact(frameworkId, artefactData = {}) {
  const artefact = await apiRequest(`/api/frameworks/${frameworkId}/artefacts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(buildArtefactPayload(artefactData, { forCreate: true })),
  })

  return normalizeFrameworkArtefact(artefact)
}

export async function getFrameworkArtefact(frameworkId, artefactId) {
  const artefact = await apiRequest(
    `/api/frameworks/${frameworkId}/artefacts/${artefactId}`
  )
  return normalizeFrameworkArtefact(artefact)
}

export async function updateFrameworkArtefact(
  frameworkId,
  artefactId,
  artefactData = {}
) {
  const artefact = await apiRequest(
    `/api/frameworks/${frameworkId}/artefacts/${artefactId}`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(buildArtefactPayload(artefactData)),
    }
  )

  return normalizeFrameworkArtefact(artefact)
}

export async function deleteFrameworkArtefact(frameworkId, artefactId) {
  return await apiRequest(
    `/api/frameworks/${frameworkId}/artefacts/${artefactId}`,
    {
      method: 'DELETE',
    }
  )
}

export async function getAdminUsers(options = {}) {
  return await apiRequest('/api/admin/users', {
    suppressAuthRedirect: Boolean(options.suppressAuthRedirect),
  })
}

export async function createAdminUser(userData = {}, options = {}) {
  const payload = {
    email: userData.email,
    password: userData.password,
  }

  if (userData.username !== undefined && userData.username !== '') {
    payload.username = userData.username
  }

  return await apiRequest('/api/admin/users', {
    method: 'POST',
    suppressAuthRedirect: Boolean(options.suppressAuthRedirect),
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export async function disableAdminUser(userId, options = {}) {
  return await apiRequest(`/api/admin/users/${userId}/disable`, {
    method: 'POST',
    suppressAuthRedirect: Boolean(options.suppressAuthRedirect),
  })
}

export async function enableAdminUser(userId, options = {}) {
  return await apiRequest(`/api/admin/users/${userId}/enable`, {
    method: 'POST',
    suppressAuthRedirect: Boolean(options.suppressAuthRedirect),
  })
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
