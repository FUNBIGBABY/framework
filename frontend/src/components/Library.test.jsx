import { afterEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import Library from './Library'

function mockResponse(status, data = {}) {
  return {
    status,
    ok: status >= 200 && status < 300,
    json: vi.fn().mockResolvedValue(data),
  }
}

afterEach(() => {
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

describe('Library', () => {
  it('loads authenticated backend public-list items', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, {
        items: [
          {
            id: 'fw_public',
            title: 'Evidence Planning Framework',
            version: '2.0.0',
            family: 'Research',
            confidence: 92,
            category: 'Research',
            tags: ['evidence', 'planning'],
            published_at: '2026-06-23T10:00:00Z',
            updated_at: '2026-06-23T10:01:00Z',
            preview_artefacts: [
              { name: 'Planning Canvas', description: 'A compact canvas' },
            ],
          },
        ],
        next_cursor: null,
        limit: 20,
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    render(<Library />)

    expect(
      await screen.findByText('Evidence Planning Framework')
    ).toBeInTheDocument()
    expect(screen.getByText('Planning Canvas')).toBeInTheDocument()
    expect(screen.getByText('evidence')).toBeInTheDocument()
    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/public?limit=20'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      credentials: 'include',
    })
  })

  it('shows an auth-required state when the backend rejects the library request', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(mockResponse(401, { detail: 'Not authenticated' }))
      .mockResolvedValueOnce(mockResponse(401, { detail: 'Not authenticated' }))
    vi.stubGlobal('fetch', fetchMock)

    render(<Library />)

    expect(
      await screen.findByText('Sign in is required to view the Library.')
    ).toBeInTheDocument()
  })
})
