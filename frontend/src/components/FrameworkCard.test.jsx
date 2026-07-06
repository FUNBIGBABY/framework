import { afterEach, describe, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import FrameworkCard from './FrameworkCard'

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

describe('FrameworkCard publish state actions', () => {
  it('unpublishes through the backend owner endpoint', async () => {
    const user = userEvent.setup()
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, {
        success: true,
        framework_id: 'fw_public',
        is_public: false,
        category: 'Research',
        tags: ['evidence'],
        published_at: null,
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    render(
      <MemoryRouter>
        <FrameworkCard
          framework={{
            id: 'fw_public',
            title: 'Published Framework',
            version: '2.0.0',
            family: 'Research',
            confidence: 91,
            created_at: '2026-06-23T10:00:00Z',
            preview_artefacts: [],
            isPublic: true,
          }}
        />
      </MemoryRouter>
    )

    expect(screen.getByText(/^Published$/)).toBeInTheDocument()

    await user.click(screen.getByTitle('More options'))
    await user.click(
      await screen.findByRole('button', {
        name: /Unpublish from Marketplace/i,
      })
    )

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1))
    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/fw_public/unpublish'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
    })
    await waitFor(() =>
      expect(screen.queryByText(/^Published$/)).not.toBeInTheDocument()
    )
  })
})
