import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  apiFetch,
  createFrameworkArtefact,
  createFramework,
  createAdminUser,
  deleteFrameworkArtefact,
  disableAdminUser,
  enableAdminUser,
  generateFrameworkFromText,
  getAdminUsers,
  getFrameworkArtefact,
  listFrameworkArtefacts,
  getPublicFrameworks,
  publishFramework,
  regenerateFramework,
  unpublishFramework,
  updateFramework,
  updateFrameworkArtefact,
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
  expect(serialized).not.toContain('framework_id')
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

describe('library and publish REST helpers', () => {
  it('loads authenticated public library items from the backend response shape', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, {
        items: [
          {
            id: 'fw_public',
            title: 'Published Framework',
            version: '2.0.0',
            family: 'Research',
            confidence: 88,
            category: 'Research',
            tags: ['evidence', 'planning'],
            published_at: '2026-06-23T10:00:00Z',
            updated_at: '2026-06-23T10:01:00Z',
            preview_artefacts: [
              { name: 'Canvas', description: 'Research canvas' },
            ],
          },
        ],
        next_cursor: 'cursor-2',
        limit: 20,
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    const result = await getPublicFrameworks({
      limit: 20,
      suppressAuthRedirect: true,
    })

    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/public?limit=20'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      credentials: 'include',
    })
    expect(result).toMatchObject({
      next_cursor: 'cursor-2',
      limit: 20,
    })
    expect(result.items[0]).toMatchObject({
      id: 'fw_public',
      title: 'Published Framework',
      tags: ['evidence', 'planning'],
      published_at: '2026-06-23T10:00:00Z',
      preview_artefacts: [{ name: 'Canvas', description: 'Research canvas' }],
      isPublic: true,
      canManage: false,
    })
  })

  it('publishes through the backend owner endpoint without client identity fields', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, {
        success: true,
        framework_id: 'fw_123',
        is_public: true,
        category: 'Research',
        tags: ['evidence'],
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    await publishFramework('fw_123', {
      category: 'Research',
      tags: ['evidence'],
      version: '2.0.0',
      user_id: 'ignored-user',
      creator_id: 'ignored-creator',
      tenant_id: 'ignored-tenant',
    })

    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/fw_123/publish'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })
    expect(requestBody(fetchMock)).toEqual({
      category: 'Research',
      tags: ['evidence'],
      version: '2.0.0',
    })
    expectNoClientIdentityFields(requestBody(fetchMock))
    expect(JSON.stringify(fetchMock.mock.calls)).not.toContain('push-framework')
  })

  it('unpublishes through the backend owner endpoint', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, {
        success: true,
        framework_id: 'fw_123',
        is_public: false,
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    await unpublishFramework('fw_123')

    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/fw_123/unpublish'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
    })
  })
})

describe('framework artefact child-resource REST helpers', () => {
  it('lists artefacts from the framework child-resource endpoint', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, [
        {
          id: 'art_1',
          framework_id: 'fw_123',
          name: 'Planning Canvas',
          artefact_type: 'canvas',
          content_json: {
            summary: 'Canvas summary',
            sections: [{ heading: 'Intro', body: 'Start here' }],
          },
          metadata_json: { source: 'test' },
          ord: 2,
        },
      ])
    )
    vi.stubGlobal('fetch', fetchMock)

    const artefacts = await listFrameworkArtefacts('fw_123')

    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/fw_123/artefacts'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      credentials: 'include',
    })
    expect(artefacts[0]).toMatchObject({
      id: 'art_1',
      name: 'Planning Canvas',
      artefact_type: 'canvas',
      summary: 'Canvas summary',
      sections: [{ heading: 'Intro', body: 'Start here' }],
      metadata_json: { source: 'test' },
      ord: 2,
    })
  })

  it('creates artefacts without parent or identity fields in the body', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(201, {
        id: 'art_created',
        framework_id: 'fw_123',
        name: 'Created Artefact',
        artefact_type: 'brief',
        content_json: { summary: 'Created summary' },
        metadata_json: {},
        ord: 0,
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    await createFrameworkArtefact('fw_123', {
      name: 'Created Artefact',
      artefact_type: 'brief',
      summary: 'Created summary',
      framework_id: 'body-parent',
      user_id: 'client-user',
      creator_id: 'client-creator',
      tenant_id: 'client-tenant',
      'X-Tenant-ID': 'client-tenant',
    })

    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/fw_123/artefacts'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })
    expect(requestBody(fetchMock)).toEqual({
      name: 'Created Artefact',
      artefact_type: 'brief',
      content_json: { summary: 'Created summary' },
      metadata_json: {},
      ord: 0,
    })
    expectNoClientIdentityFields(requestBody(fetchMock))
  })

  it('gets a single framework artefact through the child-resource endpoint', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, {
        id: 'art_1',
        framework_id: 'fw_123',
        name: 'Planning Canvas',
        artefact_type: 'canvas',
        content_json: {},
        metadata_json: {},
        ord: 0,
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    await getFrameworkArtefact('fw_123', 'art_1')

    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/fw_123/artefacts/art_1'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      credentials: 'include',
    })
  })

  it('updates artefacts without parent or identity fields in the body', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, {
        id: 'art_1',
        framework_id: 'fw_123',
        name: 'Updated Artefact',
        artefact_type: 'brief',
        content_json: { summary: 'Updated summary' },
        metadata_json: { editor: 'rich-text' },
        ord: 4,
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    await updateFrameworkArtefact('fw_123', 'art_1', {
      id: 'art_1',
      name: 'Updated Artefact',
      artefact_type: 'brief',
      summary: 'Updated summary',
      metadata_json: { editor: 'rich-text' },
      ord: 4,
      framework_id: 'body-parent',
      user_id: 'client-user',
      creator_id: 'client-creator',
      tenant_id: 'client-tenant',
      'X-Tenant-ID': 'client-tenant',
    })

    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/fw_123/artefacts/art_1'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })
    expect(requestBody(fetchMock)).toEqual({
      name: 'Updated Artefact',
      artefact_type: 'brief',
      content_json: { summary: 'Updated summary' },
      metadata_json: { editor: 'rich-text' },
      ord: 4,
    })
    expectNoClientIdentityFields(requestBody(fetchMock))
  })

  it('deletes artefacts through the child-resource endpoint', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, {
        success: true,
        framework_id: 'fw_123',
        artefact_id: 'art_1',
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    await deleteFrameworkArtefact('fw_123', 'art_1')

    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/fw_123/artefacts/art_1'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      method: 'DELETE',
      credentials: 'include',
    })
    expect(fetchMock.mock.calls[0][1]).not.toHaveProperty('body')
  })
})

describe('admin users REST helpers', () => {
  it('loads backend admin users with cookie credentials', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, [
        {
          id: 'user_admin',
          email: 'admin@example.com',
          username: 'admin',
          is_disabled: false,
        },
      ])
    )
    vi.stubGlobal('fetch', fetchMock)

    const users = await getAdminUsers({ suppressAuthRedirect: true })

    expect(users[0]).toMatchObject({
      id: 'user_admin',
      email: 'admin@example.com',
    })
    expect(fetchMock.mock.calls[0][0]).toContain('/api/admin/users')
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      credentials: 'include',
    })
  })

  it('creates backend users without password hashes or client identity fields', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(201, {
        id: 'user_new',
        email: 'new@example.com',
        username: 'new_user',
        is_disabled: false,
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    await createAdminUser(
      {
        email: 'new@example.com',
        username: 'new_user',
        password: 'temporary-password',
        password_hash: 'must-not-send',
        user_id: 'client-user',
        creator_id: 'client-creator',
        tenant_id: 'client-tenant',
      },
      { suppressAuthRedirect: true }
    )

    expect(fetchMock.mock.calls[0][0]).toContain('/api/admin/users')
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })
    expect(requestBody(fetchMock)).toEqual({
      email: 'new@example.com',
      username: 'new_user',
      password: 'temporary-password',
    })
    expect(JSON.stringify(requestBody(fetchMock))).not.toContain(
      'password_hash'
    )
    expectNoClientIdentityFields(requestBody(fetchMock))
  })

  it('disables and enables users through backend admin endpoints', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        mockResponse(200, {
          id: 'user_regular',
          email: 'regular@example.com',
          is_disabled: true,
        })
      )
      .mockResolvedValueOnce(
        mockResponse(200, {
          id: 'user_regular',
          email: 'regular@example.com',
          is_disabled: false,
        })
      )
    vi.stubGlobal('fetch', fetchMock)

    await disableAdminUser('user_regular', { suppressAuthRedirect: true })
    await enableAdminUser('user_regular', { suppressAuthRedirect: true })

    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/admin/users/user_regular/disable'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
    })
    expect(fetchMock.mock.calls[1][0]).toContain(
      '/api/admin/users/user_regular/enable'
    )
    expect(fetchMock.mock.calls[1][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
    })
  })
})
