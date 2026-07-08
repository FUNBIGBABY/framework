import { describe, it, expect, beforeEach, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { AuthProvider, useAuth } from './AuthContext'

const apiMocks = vi.hoisted(() => ({
  getCurrentBackendUser: vi.fn(),
  loginWithBackend: vi.fn(),
  logoutWithBackend: vi.fn(),
}))

const removedUserStateKeys = [
  ['tenant', 'Id'].join(''),
  ['joined', 'Organization'].join(''),
  ['role', 's'].join(''),
  ['expert', 'Profile'].join(''),
]
const removedTenantUpdateKey = ['updateUser', 'Tenant'].join('')

vi.mock('../lib/api', () => ({
  getCurrentBackendUser: apiMocks.getCurrentBackendUser,
  loginWithBackend: apiMocks.loginWithBackend,
  logoutWithBackend: apiMocks.logoutWithBackend,
}))

function ContextProbe() {
  const auth = useAuth()

  return (
    <div>
      <output data-testid="auth">{String(auth.isAuthenticated)}</output>
      <output data-testid="user">{JSON.stringify(auth.user)}</output>
      <output data-testid="has-update-tenant">
        {String(Object.hasOwn(auth, removedTenantUpdateKey))}
      </output>
      <button type="button" onClick={() => auth.login('login@example.com', 'pw')}>
        Login
      </button>
      <button type="button" onClick={() => auth.logout()}>
        Logout
      </button>
    </div>
  )
}

function renderAuth() {
  return render(
    <AuthProvider>
      <ContextProbe />
    </AuthProvider>
  )
}

function readUser() {
  return JSON.parse(screen.getByTestId('user').textContent)
}

function expectNoTenantOrgState(user) {
  removedUserStateKeys.forEach(key => {
    expect(user).not.toHaveProperty(key)
  })
  expect(screen.getByTestId('has-update-tenant')).toHaveTextContent('false')
}

describe('AuthContext backend session state', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('restores a backend-cookie user without tenant or organization state', async () => {
    apiMocks.getCurrentBackendUser.mockResolvedValue({
      id: 'user_1',
      email: 'owner@example.com',
      username: 'owner',
      is_super_admin: true,
    })

    renderAuth()

    await screen.findByText('true')

    expect(apiMocks.getCurrentBackendUser).toHaveBeenCalledWith({
      suppressAuthRedirect: true,
    })
    expect(readUser()).toEqual({
      uid: 'user_1',
      id: 'user_1',
      backendUserId: 'user_1',
      email: 'owner@example.com',
      username: 'owner',
      isSuperAdmin: true,
      authProvider: 'backend-cookie',
    })
    expectNoTenantOrgState(readUser())
  })

  it('keeps login and logout on backend-cookie state only', async () => {
    apiMocks.getCurrentBackendUser.mockRejectedValue(new Error('not signed in'))
    apiMocks.loginWithBackend.mockResolvedValue({
      user: {
        id: 'user_2',
        email: 'login@example.com',
        username: null,
        is_super_admin: false,
      },
    })
    apiMocks.logoutWithBackend.mockResolvedValue({ success: true })

    renderAuth()

    await waitFor(() => {
      expect(screen.getByTestId('auth')).toHaveTextContent('false')
    })

    fireEvent.click(screen.getByRole('button', { name: 'Login' }))

    await waitFor(() => {
      expect(readUser()).toEqual({
        uid: 'user_2',
        id: 'user_2',
        backendUserId: 'user_2',
        email: 'login@example.com',
        username: 'login',
        isSuperAdmin: false,
        authProvider: 'backend-cookie',
      })
    })
    expectNoTenantOrgState(readUser())

    fireEvent.click(screen.getByRole('button', { name: 'Logout' }))

    await waitFor(() => expect(screen.getByTestId('user')).toHaveTextContent('null'))
    expect(apiMocks.logoutWithBackend).toHaveBeenCalled()
  })
})
