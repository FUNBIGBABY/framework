import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import App from './App'

const authState = vi.hoisted(() => ({
  value: {
    loading: false,
    isAuthenticated: true,
    user: null,
    logout: vi.fn(),
  },
}))

vi.mock('./contexts/AuthContext', () => ({
  AuthProvider: ({ children }) => children,
  useAuth: () => authState.value,
}))

vi.mock('./components/Login', () => ({
  default: () => 'login route',
}))

vi.mock('./components/YourFrameworks', () => ({
  default: () => 'framework route shell',
}))

vi.mock('./components/CreateFramework', () => ({
  default: () => 'create route',
}))

vi.mock('./components/FrameworkEditor', () => ({
  default: () => 'editor route',
}))

vi.mock('./components/Library', () => ({
  default: () => 'library route',
}))

vi.mock('./components/MigrationTool', () => ({
  default: () => 'migration route',
}))

vi.mock('./components/TenantSettings', () => ({
  default: () => 'settings route',
}))

vi.mock('./components/TenantCreationModal', () => ({
  default: () => 'tenant creation modal',
}))

vi.mock('./components/InviteAccept', () => ({
  default: () => 'invite route',
}))

vi.mock('./components/YourOrganization', () => ({
  default: () => 'organization route',
}))

vi.mock('./components/AdminPanel', () => ({
  default: () => 'admin route',
}))

describe('App route shell', () => {
  beforeEach(() => {
    window.history.pushState({}, '', '/')
    authState.value = {
      loading: false,
      isAuthenticated: true,
      user: {
        id: 'backend-user-1',
        email: 'owner@example.com',
        username: 'owner',
        tenantId: null,
        joinedOrganization: null,
        authProvider: 'backend-cookie',
      },
      logout: vi.fn(),
    }
  })

  it('does not open tenant creation on the normal backend-cookie post-login path', async () => {
    render(<App />)

    expect(await screen.findByText('framework route shell')).toBeInTheDocument()
    expect(screen.queryByText('tenant creation modal')).not.toBeInTheDocument()

    await waitFor(() => {
      expect(window.location.pathname).toBe('/personal/frameworks')
    })
  })
})
