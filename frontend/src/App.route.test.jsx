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
        authProvider: 'backend-cookie',
      },
      logout: vi.fn(),
    }
  })

  it('routes authenticated root users to the personal framework list', async () => {
    render(<App />)

    expect(await screen.findByText('framework route shell')).toBeInTheDocument()

    await waitFor(() => {
      expect(window.location.pathname).toBe('/frameworks')
    })
  })

  it('mounts create, editor, library, and admin through personal private routes', async () => {
    window.history.pushState({}, '', '/frameworks/create')
    const { unmount } = render(<App />)
    expect(await screen.findByText('create route')).toBeInTheDocument()
    unmount()

    window.history.pushState({}, '', '/frameworks/fw_123')
    const editorRender = render(<App />)
    expect(await screen.findByText('editor route')).toBeInTheDocument()
    editorRender.unmount()

    window.history.pushState({}, '', '/library')
    const libraryRender = render(<App />)
    expect(await screen.findByText('library route')).toBeInTheDocument()
    libraryRender.unmount()

    window.history.pushState({}, '', '/admin')
    render(<App />)
    expect(await screen.findByText('admin route')).toBeInTheDocument()
  })
})
