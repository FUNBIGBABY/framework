import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import Login from './Login'

const authMock = vi.hoisted(() => ({
  login: vi.fn(),
}))

vi.mock('../contexts/AuthContext', () => ({
  useAuth: () => ({
    login: authMock.login,
  }),
}))

describe('Login', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    authMock.login.mockResolvedValue({
      success: true,
      user: {
        id: 'backend-user-1',
        email: 'owner@example.com',
        tenantId: null,
        authProvider: 'backend-cookie',
      },
    })
  })

  it('routes backend-cookie users without a tenant to the personal framework shell', async () => {
    const user = userEvent.setup()

    render(
      <MemoryRouter initialEntries={['/login']}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/personal/frameworks"
            element={<div>Personal frameworks destination</div>}
          />
        </Routes>
      </MemoryRouter>
    )

    await user.type(screen.getByLabelText('Email Address'), 'owner@example.com')
    await user.type(screen.getByLabelText('Password'), 'correct-password')
    await user.click(screen.getByRole('button', { name: /^sign in$/i }))

    expect(authMock.login).toHaveBeenCalledWith(
      'owner@example.com',
      'correct-password'
    )
    expect(
      await screen.findByText('Personal frameworks destination')
    ).toBeInTheDocument()
  })
})
