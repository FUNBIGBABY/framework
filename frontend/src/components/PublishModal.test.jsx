import { afterEach, describe, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PublishModal from './PublishModal'

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

describe('PublishModal', () => {
  it('publishes through backend REST without vector sync side effects', async () => {
    const user = userEvent.setup()
    const onClose = vi.fn()
    const onSuccess = vi.fn()
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, {
        success: true,
        framework_id: 'fw_123',
        is_public: true,
        category: 'Research',
        tags: ['evidence', 'planning'],
        published_at: '2026-06-23T10:00:00Z',
      })
    )
    vi.stubGlobal('fetch', fetchMock)

    render(
      <PublishModal
        framework={{
          id: 'fw_123',
          title: 'Research Framework',
          family: 'Research',
          version: '2.0.0',
        }}
        onClose={onClose}
        onSuccess={onSuccess}
      />
    )

    await user.type(
      screen.getByLabelText('Tags (comma-separated)'),
      'evidence, planning'
    )
    await user.click(
      screen.getByRole('checkbox', {
        name: /I confirm this framework is ready to be shared in the Library/i,
      })
    )
    await user.click(
      screen.getByRole('button', { name: /^Publish to Marketplace$/i })
    )

    await waitFor(() => expect(onSuccess).toHaveBeenCalledTimes(1))
    expect(onClose).toHaveBeenCalledTimes(1)
    expect(fetchMock).toHaveBeenCalledTimes(1)
    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/frameworks/fw_123/publish'
    )
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({
      category: 'Research',
      tags: ['evidence', 'planning'],
      version: '2.0.0',
    })
    expect(JSON.stringify(fetchMock.mock.calls)).not.toContain('push-framework')
  })
})
