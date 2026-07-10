/**
 * Typed HTTP client for the IDP Lite API.
 *
 * Every request goes through here so that:
 *   - the Bearer token is attached consistently
 *   - API errors are normalized into a single shape the UI can render
 *
 * The token is set explicitly via setToken() — it's never read from
 * localStorage. It lives only in this module's private field plus
 * AuthContext's React state, both of which are wiped on a full page reload.
 * That's intentional (see hooks/useAuth.tsx).
 */

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export interface User {
  id: string
  username: string
  email: string | null
  role: 'member' | 'team_admin' | 'super_admin'
  team_id: string | null
}

export interface ApiKeyResponse {
  api_key: string
  note: string
}

export class APIError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
    this.name = 'APIError'
  }
}

class APIClient {
  private token: string | null = null

  setToken(token: string | null) {
    this.token = token
  }

  private async request<T>(path: string, opts: RequestInit = {}): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(opts.headers as Record<string, string> | undefined),
    }
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    const resp = await fetch(`${API_BASE}${path}`, { ...opts, headers })

    if (!resp.ok) {
      const body = await resp.json().catch(() => ({ detail: `HTTP ${resp.status}` }))
      throw new APIError(resp.status, body.detail ?? `HTTP ${resp.status}`)
    }

    if (resp.status === 204) {
      return undefined as T
    }
    return resp.json()
  }

  getMe = () => this.request<User>('/auth/me')
  generateApiKey = () => this.request<ApiKeyResponse>('/auth/api-key', { method: 'POST' })
}

export const api = new APIClient()