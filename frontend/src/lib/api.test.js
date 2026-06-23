import { afterEach, describe, expect, it, vi } from 'vitest'
import { apiFetch } from './api'

function mockResponse(status) {
  return {
    status,
    ok: status >= 200 && status < 300,
    json: vi.fn().mockResolvedValue({}),
  }
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
