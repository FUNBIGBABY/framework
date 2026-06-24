import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import TenantRoute from './TenantRoute'

const authState = vi.hoisted(() => ({
  value: {
    loading: false,
    user: null,
  },
}))

vi.mock('../contexts/AuthContext', () => ({
  useAuth: () => authState.value,
}))

describe('TenantRoute', () => {
  beforeEach(() => {
    authState.value = {
      loading: false,
      user: {
        id: 'backend-user-1',
        email: 'owner@example.com',
        tenantId: null,
        joinedOrganization: null,
        authProvider: 'backend-cookie',
      },
    }
  })

  it('allows authenticated backend-cookie users without a tenant through core framework routes', () => {
    render(
      <MemoryRouter initialEntries={['/personal/frameworks']}>
        <Routes>
          <Route
            path="/:tenantId/frameworks"
            element={
              <TenantRoute>
                <div>Core framework route shell</div>
              </TenantRoute>
            }
          />
          <Route path="/" element={<div>Root fallback</div>} />
          <Route path="/login" element={<div>Login route</div>} />
        </Routes>
      </MemoryRouter>
    )

    expect(screen.getByText('Core framework route shell')).toBeInTheDocument()
    expect(screen.queryByText('Root fallback')).not.toBeInTheDocument()
    expect(screen.queryByText('Login route')).not.toBeInTheDocument()
  })
})
