import { authService } from './auth.service'

interface RequestOptions extends RequestInit {
  _retry?: boolean
}

class ApiClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  private async handleResponse(response: Response) {
    if (!response.ok) {
      if (response.status === 401) {
        const refreshToken = authService.getRefreshToken()
        if (refreshToken) {
          try {
            await authService.refreshToken(refreshToken)
            return null
          } catch (error) {
            authService.logout()
            window.location.href = '/login'
          }
        }
      }

      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response
  }

  private async request<T>(
    url: string,
    options: RequestOptions = {}
  ): Promise<T> {
    const token = authService.getAccessToken()
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    let response = await fetch(`${this.baseURL}${url}`, {
      ...options,
      headers,
    })

    if (response.status === 401 && !options._retry) {
      const refreshToken = authService.getRefreshToken()
      if (refreshToken) {
        try {
          await authService.refreshToken(refreshToken)
          const newToken = authService.getAccessToken()
          if (newToken) {
            headers['Authorization'] = `Bearer ${newToken}`
            options._retry = true
            response = await fetch(`${this.baseURL}${url}`, {
              ...options,
              headers,
            })
          }
        } catch (error) {
          authService.logout()
          window.location.href = '/login'
          throw error
        }
      }
    }

    const processed = await this.handleResponse(response)
    if (!processed) {
      return this.request<T>(url, { ...options, _retry: true })
    }

    return processed.json() as Promise<T>
  }

  get<T>(url: string, options?: RequestInit) {
    return this.request<T>(url, { ...options, method: 'GET' })
  }

  post<T>(url: string, data?: unknown, options?: RequestInit) {
    return this.request<T>(url, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  put<T>(url: string, data?: unknown, options?: RequestInit) {
    return this.request<T>(url, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  patch<T>(url: string, data?: unknown, options?: RequestInit) {
    return this.request<T>(url, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  delete<T>(url: string, options?: RequestInit) {
    return this.request<T>(url, { ...options, method: 'DELETE' })
  }
}

export const ttmsApi = new ApiClient(
  import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
)
