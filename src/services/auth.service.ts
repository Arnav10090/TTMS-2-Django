export interface LoginResponse {
  access: string
  refresh: string
  user?: {
    id: number
    email: string
    username: string
  }
}

export interface TokenRefreshResponse {
  access: string
}

export interface User {
  id: number
  email: string
  username: string
}

class AuthService {
  private apiBase: string
  private storageKeyAccess = 'auth_access_token'
  private storageKeyRefresh = 'auth_refresh_token'
  private storageKeyUser = 'auth_user'

  constructor(apiBase: string) {
    this.apiBase = apiBase
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const response = await fetch(`${this.apiBase}/auth/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Login failed')
      }

      const data = (await response.json()) as LoginResponse

      if (data.access && data.refresh) {
        this.setTokens(data.access, data.refresh)
        if (data.user) {
          this.setUser(data.user)
        }
      }

      return data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async refreshToken(refreshToken: string): Promise<string> {
    try {
      const response = await fetch(`${this.apiBase}/auth/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      })

      if (!response.ok) {
        this.clearTokens()
        throw new Error('Token refresh failed')
      }

      const data = (await response.json()) as TokenRefreshResponse

      if (data.access) {
        this.setAccessToken(data.access)
      }

      return data.access
    } catch (error) {
      this.clearTokens()
      throw this.handleError(error)
    }
  }

  async logout(): Promise<void> {
    try {
      const refreshToken = this.getRefreshToken()

      if (refreshToken) {
        await fetch(`${this.apiBase}/auth/logout/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh: refreshToken }),
        })
      }
    } catch (error) {
      console.warn('Logout request failed:', error)
    } finally {
      this.clearTokens()
      this.clearUser()
    }
  }

  getAccessToken(): string | null {
    return localStorage.getItem(this.storageKeyAccess)
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.storageKeyRefresh)
  }

  getUser(): User | null {
    const user = localStorage.getItem(this.storageKeyUser)
    return user ? JSON.parse(user) : null
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken()
  }

  private setTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(this.storageKeyAccess, accessToken)
    localStorage.setItem(this.storageKeyRefresh, refreshToken)
  }

  private setAccessToken(accessToken: string): void {
    localStorage.setItem(this.storageKeyAccess, accessToken)
  }

  private setUser(user: User): void {
    localStorage.setItem(this.storageKeyUser, JSON.stringify(user))
  }

  private clearTokens(): void {
    localStorage.removeItem(this.storageKeyAccess)
    localStorage.removeItem(this.storageKeyRefresh)
  }

  private clearUser(): void {
    localStorage.removeItem(this.storageKeyUser)
  }

  private handleError(error: unknown): Error {
    if (error instanceof Error) {
      return error
    }
    return new Error('An unexpected error occurred')
  }
}

export const authService = new AuthService(
  import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
)
