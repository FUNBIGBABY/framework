import { afterEach, describe, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import AdminPanel from './AdminPanel'

function mockResponse(status, data = {}) {
  return {
    status,
    ok: status >= 200 && status < 300,
    json: vi.fn().mockResolvedValue(data),
  }
}

function renderAdminPanel() {
  return render(
    <MemoryRouter>
      <AdminPanel />
    </MemoryRouter>
  )
}

afterEach(() => {
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

describe('AdminPanel backend REST wiring', () => {
  it('renders users from the backend admin list response', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(
      mockResponse(200, [
        {
          id: 'user_admin',
          email: 'admin@example.com',
          username: 'admin',
          created_at: '2026-06-23T10:00:00Z',
          last_login: null,
          is_disabled: false,
          disabled_at: null,
          is_super_admin: true,
        },
        {
          id: 'user_regular',
          email: 'regular@example.com',
          username: 'regular',
          created_at: '2026-06-23T11:00:00Z',
          last_login: '2026-06-23T12:00:00Z',
          is_disabled: true,
          disabled_at: '2026-06-23T13:00:00Z',
          is_super_admin: false,
        },
      ])
    )
    vi.stubGlobal('fetch', fetchMock)

    renderAdminPanel()

    expect(await screen.findByText('admin@example.com')).toBeInTheDocument()
    expect(screen.getByText('regular@example.com')).toBeInTheDocument()
    expect(screen.getByText('user_admin')).toBeInTheDocument()
    expect(screen.getByText('user_regular')).toBeInTheDocument()
    expect(screen.getByText('SUPER ADMIN')).toBeInTheDocument()
    expect(screen.getByText('DISABLED')).toBeInTheDocument()
    expect(fetchMock.mock.calls[0][0]).toContain('/api/admin/users')
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      credentials: 'include',
    })
  })

  it('creates a user without sending password_hash', async () => {
    const user = userEvent.setup()
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(mockResponse(200, []))
      .mockResolvedValueOnce(
        mockResponse(201, {
          id: 'user_new',
          email: 'new@example.com',
          username: 'new_user',
          is_disabled: false,
        })
      )
      .mockResolvedValueOnce(
        mockResponse(200, [
          {
            id: 'user_new',
            email: 'new@example.com',
            username: 'new_user',
            is_disabled: false,
            is_super_admin: false,
          },
        ])
      )
    vi.stubGlobal('fetch', fetchMock)

    renderAdminPanel()

    await screen.findByRole('heading', { name: 'Create User' })
    await user.type(screen.getByLabelText('Email'), 'new@example.com')
    await user.type(screen.getByLabelText('Username'), 'new_user')
    await user.type(
      screen.getByLabelText('Temporary Password'),
      'temporary-password'
    )
    await user.click(screen.getByRole('button', { name: 'Create User' }))

    await screen.findByText('Created user new@example.com.')
    expect(fetchMock).toHaveBeenCalledTimes(3)
    expect(fetchMock.mock.calls[1][0]).toContain('/api/admin/users')
    expect(fetchMock.mock.calls[1][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })

    const body = JSON.parse(fetchMock.mock.calls[1][1].body)
    expect(body).toEqual({
      email: 'new@example.com',
      username: 'new_user',
      password: 'temporary-password',
    })
    expect(JSON.stringify(body)).not.toContain('password_hash')
  })

  it('disables and enables users through backend endpoints', async () => {
    const user = userEvent.setup()
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        mockResponse(200, [
          {
            id: 'user_regular',
            email: 'regular@example.com',
            username: 'regular',
            is_disabled: false,
            is_super_admin: false,
          },
        ])
      )
      .mockResolvedValueOnce(
        mockResponse(200, {
          id: 'user_regular',
          email: 'regular@example.com',
          username: 'regular',
          is_disabled: true,
          is_super_admin: false,
        })
      )
      .mockResolvedValueOnce(
        mockResponse(200, {
          id: 'user_regular',
          email: 'regular@example.com',
          username: 'regular',
          is_disabled: false,
          is_super_admin: false,
        })
      )
    vi.stubGlobal('fetch', fetchMock)

    renderAdminPanel()

    await screen.findByText('regular@example.com')
    await user.click(screen.getByRole('button', { name: 'Disable' }))

    await waitFor(() =>
      expect(fetchMock.mock.calls[1][0]).toContain(
        '/api/admin/users/user_regular/disable'
      )
    )
    expect(fetchMock.mock.calls[1][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
    })

    await screen.findByText('regular@example.com is now disabled.')
    await user.click(screen.getByRole('button', { name: 'Enable' }))

    await waitFor(() =>
      expect(fetchMock.mock.calls[2][0]).toContain(
        '/api/admin/users/user_regular/enable'
      )
    )
    expect(fetchMock.mock.calls[2][1]).toMatchObject({
      method: 'POST',
      credentials: 'include',
    })
  })

  it('shows backend 403 as the admin authorization source', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(mockResponse(403, { detail: 'Admin access required' }))
    vi.stubGlobal('fetch', fetchMock)

    renderAdminPanel()

    expect(await screen.findByText(/backend returned 403/i)).toBeInTheDocument()
    expect(
      screen.getByText(/account cannot manage users/i)
    ).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Create User' })).toBeNull()
    expect(fetchMock).toHaveBeenCalledTimes(1)
  })

  it('does not render the old domain management controls', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(mockResponse(200, []))
    vi.stubGlobal('fetch', fetchMock)

    renderAdminPanel()

    expect(await screen.findByText('Domain Policy')).toBeInTheDocument()
    expect(screen.queryByText(/Email Domain Whitelist/i)).toBeNull()
    expect(
      screen.queryByRole('button', { name: /Add Domain/i })
    ).toBeNull()
    expect(
      screen.getByText(/not part of the accepted Phase 5 admin REST contract/i)
    ).toBeInTheDocument()
  })
})
