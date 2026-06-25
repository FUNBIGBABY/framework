import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import FrameworkEditor from './FrameworkEditor'

const apiMocks = vi.hoisted(() => {
  class MockAPIError extends Error {
    constructor(message, status, data) {
      super(message)
      this.name = 'APIError'
      this.status = status
      this.data = data
    }
  }

  return {
    APIError: MockAPIError,
    apiFetch: vi.fn(),
    createFrameworkArtefact: vi.fn(),
    deleteFrameworkArtefact: vi.fn(),
    getCurrentTenantId: vi.fn(() => 'personal'),
    getFramework: vi.fn(),
    listFrameworkArtefacts: vi.fn(),
    regenerateFramework: vi.fn(),
    updateFramework: vi.fn(),
    updateFrameworkArtefact: vi.fn(),
  }
})

vi.mock('../lib/api', () => ({
  default: {
    EXPORT_DOCX: '/api/frameworks/export-docx',
    AI_FILL: '/api/frameworks/ai-fill',
  },
  APIError: apiMocks.APIError,
  apiFetch: apiMocks.apiFetch,
  createFrameworkArtefact: apiMocks.createFrameworkArtefact,
  deleteFrameworkArtefact: apiMocks.deleteFrameworkArtefact,
  getCurrentTenantId: apiMocks.getCurrentTenantId,
  getFramework: apiMocks.getFramework,
  listFrameworkArtefacts: apiMocks.listFrameworkArtefacts,
  regenerateFramework: apiMocks.regenerateFramework,
  updateFramework: apiMocks.updateFramework,
  updateFrameworkArtefact: apiMocks.updateFrameworkArtefact,
}))

vi.mock('../contexts/AuthContext', () => ({
  useAuth: () => ({
    user: {
      id: 'user_owner',
      email: 'owner@example.com',
      tenantId: null,
    },
  }),
}))

vi.mock('./ArtefactEditor', () => ({
  default: ({ variant, index, onUpdate, onDelete, canDelete }) => (
    <div>
      <span>{variant.name}</span>
      <button
        type="button"
        onClick={() =>
          onUpdate(index, {
            ...variant,
            summary: 'Updated summary',
            sections: [{ heading: 'Updated', body: 'Body' }],
          })
        }
      >
        Update {variant.name}
      </button>
      {canDelete && (
        <button type="button" onClick={() => onDelete(index)}>
          Delete {variant.name}
        </button>
      )}
    </div>
  ),
}))

function makeFramework() {
  return {
    id: 'fw_123',
    metadata: {
      title: 'Test Framework',
      version: '1.0.0',
      tags: '',
    },
    steps: [],
    artefacts: {
      default: {
        type: 'Concept Pack',
        description: '',
      },
      additional: [],
    },
    risks: [],
    escalation: [],
    confidence: 80,
    _raw: {},
  }
}

function makeArtefact(overrides = {}) {
  return {
    id: 'art_1',
    name: 'Planning Canvas',
    artefact_type: 'canvas',
    summary: 'Initial summary',
    sections: [{ heading: 'Intro', body: 'Start here' }],
    metadata_json: {},
    ord: 0,
    ...overrides,
  }
}

function renderEditor() {
  return render(
    <MemoryRouter initialEntries={['/personal/frameworks/fw_123']}>
      <Routes>
        <Route path="/:tenant/frameworks/:id" element={<FrameworkEditor />} />
      </Routes>
    </MemoryRouter>
  )
}

beforeEach(() => {
  vi.spyOn(window, 'alert').mockImplementation(() => {})
  vi.spyOn(console, 'log').mockImplementation(() => {})
  vi.spyOn(console, 'error').mockImplementation(() => {})
})

afterEach(() => {
  vi.useRealTimers()
  vi.restoreAllMocks()
  localStorage.clear()
  Object.values(apiMocks).forEach(value => {
    if (typeof value?.mockReset === 'function') value.mockReset()
  })
  apiMocks.getCurrentTenantId.mockReturnValue('personal')
})

describe('FrameworkEditor artefact child-resource wiring', () => {
  it('loads child artefacts and keeps local draft backup free of auth material', async () => {
    apiMocks.getFramework.mockResolvedValue(makeFramework())
    apiMocks.listFrameworkArtefacts.mockResolvedValue([makeArtefact()])
    apiMocks.updateFramework.mockResolvedValue({ success: true })

    renderEditor()

    await waitFor(() => expect(apiMocks.listFrameworkArtefacts).toHaveBeenCalled())
    fireEvent.click(screen.getByRole('button', { name: 'Artefacts' }))

    expect(await screen.findByText('Planning Canvas')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Save Draft' }))

    await waitFor(() => expect(apiMocks.updateFramework).toHaveBeenCalled())
    const [, payload] = apiMocks.updateFramework.mock.calls[0]
    expect(payload).not.toHaveProperty('artefacts')

    const draft = localStorage.getItem('framework-draft-fw_123')
    expect(draft).toContain('artefactResources')
    expect(draft).not.toContain('access_token')
    expect(draft).not.toContain('Authorization')
    expect(draft).not.toContain('Bearer')
  })

  it('surfaces backend 403 and 404 artefact list failures', async () => {
    apiMocks.getFramework.mockResolvedValue(makeFramework())
    apiMocks.listFrameworkArtefacts.mockRejectedValue(
      new apiMocks.APIError('Forbidden artefacts', 403, {})
    )

    const { unmount } = renderEditor()

    fireEvent.click(await screen.findByRole('button', { name: 'Artefacts' }))
    expect(
      await screen.findByText(
        'The backend denied access to this framework artefact list.'
      )
    ).toBeInTheDocument()

    unmount()
    apiMocks.getFramework.mockReset()
    apiMocks.listFrameworkArtefacts.mockReset()
    apiMocks.getFramework.mockResolvedValue(makeFramework())
    apiMocks.listFrameworkArtefacts.mockRejectedValue(
      new apiMocks.APIError('Missing artefacts', 404, {})
    )

    renderEditor()

    fireEvent.click(await screen.findByRole('button', { name: 'Artefacts' }))
    expect(
      await screen.findByText('The backend could not find this artefact list.')
    ).toBeInTheDocument()
  })

  it('updates and deletes artefacts through child-resource helpers', async () => {
    apiMocks.getFramework.mockResolvedValue(makeFramework())
    apiMocks.listFrameworkArtefacts.mockResolvedValue([
      makeArtefact(),
      makeArtefact({ id: 'art_2', name: 'Second Artefact', ord: 1 }),
    ])
    apiMocks.updateFrameworkArtefact.mockResolvedValue(
      makeArtefact({ summary: 'Updated summary' })
    )
    apiMocks.deleteFrameworkArtefact.mockResolvedValue({ success: true })

    renderEditor()

    fireEvent.click(await screen.findByRole('button', { name: 'Artefacts' }))
    await screen.findByText('Planning Canvas')

    fireEvent.click(screen.getByRole('button', { name: 'Update Planning Canvas' }))

    await waitFor(() =>
      expect(apiMocks.updateFrameworkArtefact).toHaveBeenCalledWith(
        'fw_123',
        'art_1',
        expect.objectContaining({
          id: 'art_1',
          summary: 'Updated summary',
        })
      ),
      { timeout: 2000 }
    )

    fireEvent.click(screen.getByRole('button', { name: 'Delete Planning Canvas' }))
    await waitFor(() =>
      expect(apiMocks.deleteFrameworkArtefact).toHaveBeenCalledWith(
        'fw_123',
        'art_1'
      )
    )
  })

  it('creates artefacts through the child-resource helper', async () => {
    apiMocks.getFramework.mockResolvedValue(makeFramework())
    apiMocks.listFrameworkArtefacts.mockResolvedValue([])
    apiMocks.createFrameworkArtefact.mockResolvedValue(
      makeArtefact({ id: 'art_created', name: 'New Artefact' })
    )

    renderEditor()

    fireEvent.click(await screen.findByRole('button', { name: 'Artefacts' }))
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'New Artefact' })).not.toBeDisabled()
    )
    fireEvent.click(screen.getByRole('button', { name: 'New Artefact' }))

    await waitFor(() =>
      expect(apiMocks.createFrameworkArtefact).toHaveBeenCalledWith(
        'fw_123',
        expect.objectContaining({
          name: 'New Artefact',
          artefact_type: 'Concept Pack',
          ord: 0,
        })
      )
    )
  })
})
