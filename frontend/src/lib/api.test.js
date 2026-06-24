import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  apiFetch,
  createFramework,
  generateFrameworkFromText,
  regenerateFramework,
  updateFramework,
} from './api'

function mockResponse(status, data = {}) {
  return {
    status,
    ok: status >= 200 && status < 300,
    json: vi.fn().mockResolvedValue(data),
  }
}

function requestBody(fetchMock, callIndex = 0) {
  return JSON.parse(fetchMock.mock.calls[callIndex][1].body)
}

function requestHeaders(fetchMock, callIndex = 0) {
  return fetchMock.mock.calls[callIndex][1].headers || {}
}

function expectNoClientIdentityFields(value) {
  const serialized = JSON.stringify(value)

  expect(serialized).not.toContain('user_id')
  expect(serialized).not.toContain('creator_id')
  expect(serialized).not.toContain('tenant_id')
  expect(serialized).not.toContain('X-Tenant-ID')
}

afterEach(() => {
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

describe('apiFetch cookie-session refresh', () => {
  it('refreshes once after an expired-access 401 and retries the original request', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(mockResponse(401))
      .mockResolvedValueOnce(mockResponse(200))
      .mockResolvedValueOnce(mockResponse(200))
    vi.stubGlobal('fetch', fetchMock)

    const response = await apiFetch('/api/frameworks/my-frameworks')

    expect(response.status).toBe(200)
    expect(fetchMock).toHaveBeenCalledTimes(3)
    expect(fetchMock.mock.calls[0][0]).toContain('/api/frameworks/my-frameworks')
    expect(fetchMock.mock.calls[1][0]).toContain('/api/users/refresh')
    expect(fetchMock.mock.calls[1][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
    })
    expect(fetchMock.mock.calls[2][0]).toBe(fetchMock.mock.calls[0][0])
    expect(fetchMock.mock.calls[2][1]).toMatchObject({
      credentials: 'include',
    })
  })

  it('does not refresh authorization failures that remain 403', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(mockResponse(403))
    vi.stubGlobal('fetch', fetchMock)

    const response = await apiFetch('/api/admin/users', {
      suppressAuthRedirect: true,
    })

    expect(response.status).toBe(403)
    expect(fetchMock).toHaveBeenCalledTimes(1)
  })

  it('does not retry the refresh endpoint itself', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(mockResponse(401))
    vi.stubGlobal('fetch', fetchMock)

    const response = await apiFetch('/api/users/refresh', {
      method: 'POST',
      suppressAuthRedirect: true,
    })

    expect(response.status).toBe(401)
    expect(fetchMock).toHaveBeenCalledTimes(1)
  })

  it('stops after one failed refresh attempt', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(mockResponse(401))
      .mockResolvedValueOnce(mockResponse(401))
    vi.stubGlobal('fetch', fetchMock)

    const response = await apiFetch('/api/frameworks/my-frameworks', {
      suppressAuthRedirect: true,
    })

    expect(response.status).toBe(401)
    expect(fetchMock).toHaveBeenCalledTimes(2)
    expect(fetchMock.mock.calls[1][0]).toContain('/api/users/refresh')
  })
})

describe('framework mutation payloads', () => {
  it('sends patch-like update payloads without missing family, confidence, or raw data', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        mockResponse(200, { success: true, framework_id: 'fw_123' })
      )
    vi.stubGlobal('fetch', fetchMock)

    await updateFramework('fw_123', {
      metadata: { title: 'Updated Title' },
      steps: [{ id: 'step-1', name: 'Updated' }],
      user_id: 'client-user',
      creator_id: 'client-creator',
      tenant_id: 'client-tenant',
    })

    const body = requestBody(fetchMock)
    expect(body).toEqual({
      metadata: { title: 'Updated Title' },
      steps: [{ id: 'step-1', name: 'Updated' }],
    })
    expect(body).not.toHaveProperty('family')
    expect(body).not.toHaveProperty('confidence')
    expect(body).not.toHaveProperty('_raw')
    expectNoClientIdentityFields(body)
    expect(requestHeaders(fetchMock)).not.toHaveProperty('X-Tenant-ID')
  })

  it('omits empty raw framework data on update', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        mockResponse(200, { success: true, framework_id: 'fw_123' })
      )
    vi.stubGlobal('fetch', fetchMock)

    await updateFramework('fw_123', { _raw: {} })

    expect(requestBody(fetchMock)).toEqual({})
  })

  it('does not wipe raw framework data from editor autosave-style payloads', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        mockResponse(200, { success: true, framework_id: 'fw_123' })
      )
    vi.stubGlobal('fetch', fetchMock)

    await updateFramework('fw_123', {
      metadata: { title: 'Draft Title', lastUpdated: '2026-06-23T00:00:00Z' },
      steps: [{ id: 'step-1', name: 'Draft Step' }],
      artefacts: { additional: [] },
      risks: [],
      escalation: [],
      _raw: {},
    })

    const body = requestBody(fetchMock)
    expect(body).toEqual({
      metadata: {
        title: 'Draft Title',
        lastUpdated: '2026-06-23T00:00:00Z',
      },
      steps: [{ id: 'step-1', name: 'Draft Step' }],
      artefacts: { additional: [] },
      risks: [],
      escalation: [],
    })
    expect(body).not.toHaveProperty('family')
    expect(body).not.toHaveProperty('confidence')
    expect(body).not.toHaveProperty('_raw')
  })

  it('keeps create payloads valid while omitting empty raw data and client identity fields', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        mockResponse(200, { success: true, framework_id: 'fw_new' })
      )
    vi.stubGlobal('fetch', fetchMock)

    await createFramework({
      title: 'Created Framework',
      metadata: { title: 'Created Framework' },
      _raw: {},
      user_id: 'client-user',
      creator_id: 'client-creator',
      tenant_id: 'client-tenant',
    })

    const body = requestBody(fetchMock)
    expect(body).toMatchObject({
      title: 'Created Framework',
      version: '1.0.0',
      family: 'Other',
      confidence: 0,
      metadata: { title: 'Created Framework' },
      steps: [],
      artefacts: {},
      risks: [],
      escalation: [],
    })
    expect(body).not.toHaveProperty('_raw')
    expectNoClientIdentityFields(body)
    expect(requestHeaders(fetchMock)).not.toHaveProperty('X-Tenant-ID')
  })

  it('keeps generation helper payloads valid without client identity fields', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        mockResponse(200, { success: true, framework_id: 'fw_generated' })
      )
      .mockResolvedValueOnce(mockResponse(200, { success: true }))
    vi.stubGlobal('fetch', fetchMock)

    await generateFrameworkFromText('source text', true, 'model-a', true)
    await regenerateFramework(
      {
        metadata: { title: 'Regenerate Me' },
        steps: [{ id: 'step-1', name: 'Existing' }],
        _raw: {},
      },
      false
    )

    const generateBody = requestBody(fetchMock, 0)
    expect(generateBody).toEqual({
      text: 'source text',
      use_global_llm: true,
      model: 'model-a',
      reasoning: true,
    })
    expectNoClientIdentityFields(generateBody)

    const regenerateBody = requestBody(fetchMock, 1)
    expect(regenerateBody.framework).toMatchObject({
      title: 'Regenerate Me',
      version: '1.0.0',
      family: 'Other',
      confidence: 0,
      metadata: { title: 'Regenerate Me' },
      steps: [{ id: 'step-1', name: 'Existing' }],
    })
    expect(regenerateBody.framework).not.toHaveProperty('_raw')
    expectNoClientIdentityFields(regenerateBody)
  })
})
