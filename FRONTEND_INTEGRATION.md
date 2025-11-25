# Frontend Integration Guide

Complete guide for integrating the frontend (React) with TTMS and PTMS backend APIs.

## Table of Contents
1. [Environment Setup](#section-1-environment-setup)
2. [Authentication Service](#section-2-authentication-service)
3. [API Interceptor](#section-3-api-interceptor)
4. [React Implementation](#section-4-react-implementation)
5. [CORS Configuration](#section-5-cors-configuration)
6. [Troubleshooting](#troubleshooting)

---

## Section 1: Environment Setup

### 1.1 Create .env.local file

Create a `.env.local` file in the root of your React project:

```env
# TTMS API Configuration
VITE_TTMS_API_URL=http://localhost:8000/api/ttms
VITE_TTMS_API_BASE=http://localhost:8000

# PTMS API Configuration
VITE_PTMS_API_URL=http://localhost:8001/api/ptms
VITE_PTMS_API_BASE=http://localhost:8001

# Environment
VITE_ENV=development
VITE_DEBUG=true
```

### 1.2 Update Vite Configuration

Make sure your `vite.config.ts` includes environment variable support:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/ttms': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/ttms/, '/api/ttms')
      },
      '/api/ptms': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/ptms/, '/api/ptms')
      }
    }
  }
})
```

### 1.3 Access Environment Variables in React

```typescript
// example.ts
const ttmsApiUrl = import.meta.env.VITE_TTMS_API_URL
const ptmsApiUrl = import.meta.env.VITE_PTMS_API_URL

console.log('TTMS API:', ttmsApiUrl)
console.log('PTMS API:', ptmsApiUrl)
```

---

## Section 2: Authentication Service

### 2.1 Create Auth Service

Create `src/services/auth.service.ts`:

```typescript
import axios, { AxiosInstance, AxiosError } from 'axios'

export interface LoginResponse {
  access: string
  refresh: string
  user: {
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
  private axiosInstance: AxiosInstance
  private storageKeyAccess = 'auth_access_token'
  private storageKeyRefresh = 'auth_refresh_token'
  private storageKeyUser = 'auth_user'

  constructor(apiBase: string) {
    this.apiBase = apiBase
    this.axiosInstance = axios.create({
      baseURL: apiBase,
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }

  /**
   * Login with email and password
   * @param email User email
   * @param password User password
   * @param appType 'ttms' or 'ptms' to determine endpoint
   * @returns Promise with login response containing tokens
   */
  async login(email: string, password: string, appType: 'ttms' | 'ptms'): Promise<LoginResponse> {
    try {
      const endpoint = `/${appType === 'ttms' ? 'ttms' : 'ptms'}/auth/login/`
      
      const response = await this.axiosInstance.post<LoginResponse>(endpoint, {
        email,
        password
      })

      if (response.data.access && response.data.refresh) {
        this.setTokens(response.data.access, response.data.refresh)
        if (response.data.user) {
          this.setUser(response.data.user)
        }
      }

      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Refresh access token using refresh token
   * @param refreshToken Refresh token
   * @param appType 'ttms' or 'ptms'
   * @returns Promise with new access token
   */
  async refreshToken(refreshToken: string, appType: 'ttms' | 'ptms'): Promise<string> {
    try {
      const endpoint = `/${appType === 'ttms' ? 'ttms' : 'ptms'}/auth/refresh/`
      
      const response = await this.axiosInstance.post<TokenRefreshResponse>(endpoint, {
        refresh: refreshToken
      })

      if (response.data.access) {
        this.setAccessToken(response.data.access)
      }

      return response.data.access
    } catch (error) {
      this.clearTokens()
      throw this.handleError(error)
    }
  }

  /**
   * Logout user
   * @param appType 'ttms' or 'ptms'
   */
  async logout(appType: 'ttms' | 'ptms'): Promise<void> {
    try {
      const endpoint = `/${appType === 'ttms' ? 'ttms' : 'ptms'}/auth/logout/`
      const refreshToken = this.getRefreshToken()

      if (refreshToken) {
        await this.axiosInstance.post(endpoint, {
          refresh: refreshToken
        })
      }
    } catch (error) {
      console.warn('Logout request failed:', error)
    } finally {
      this.clearTokens()
      this.clearUser()
    }
  }

  /**
   * Get current access token
   */
  getAccessToken(): string | null {
    return localStorage.getItem(this.storageKeyAccess)
  }

  /**
   * Get current refresh token
   */
  getRefreshToken(): string | null {
    return localStorage.getItem(this.storageKeyRefresh)
  }

  /**
   * Get current user
   */
  getUser(): User | null {
    const user = localStorage.getItem(this.storageKeyUser)
    return user ? JSON.parse(user) : null
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getAccessToken()
  }

  /**
   * Change user password
   * @param oldPassword Current password
   * @param newPassword New password
   * @param appType 'ttms' or 'ptms'
   */
  async changePassword(
    oldPassword: string,
    newPassword: string,
    appType: 'ttms' | 'ptms'
  ): Promise<void> {
    try {
      const endpoint = `/${appType === 'ttms' ? 'ttms' : 'ptms'}/auth/users/me/change-password/`
      const token = this.getAccessToken()

      await this.axiosInstance.post(
        endpoint,
        {
          old_password: oldPassword,
          new_password: newPassword
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
    } catch (error) {
      throw this.handleError(error)
    }
  }

  /**
   * Get current user info
   * @param appType 'ttms' or 'ptms'
   */
  async getCurrentUser(appType: 'ttms' | 'ptms'): Promise<User> {
    try {
      const endpoint = `/${appType === 'ttms' ? 'ttms' : 'ptms'}/auth/users/me/`
      const token = this.getAccessToken()

      const response = await this.axiosInstance.get<User>(endpoint, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      this.setUser(response.data)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
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
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError
      if (axiosError.response?.status === 401) {
        return new Error('Unauthorized: Invalid credentials')
      } else if (axiosError.response?.status === 400) {
        return new Error(JSON.stringify(axiosError.response.data))
      }
      return new Error(axiosError.message || 'Authentication failed')
    }
    return new Error('An unexpected error occurred')
  }
}

export const ttmsAuthService = new AuthService(
  import.meta.env.VITE_TTMS_API_BASE || 'http://localhost:8000/api'
)

export const ptmsAuthService = new AuthService(
  import.meta.env.VITE_PTMS_API_BASE || 'http://localhost:8001/api'
)
```

---

## Section 3: API Interceptor

### 3.1 Create API Service with Axios Interceptors

Create `src/services/api.ts`:

```typescript
import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios'
import { ttmsAuthService, ptmsAuthService } from './auth.service'

interface RequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean
}

class ApiClient {
  private axiosInstance: AxiosInstance
  private baseURL: string
  private authService: typeof ttmsAuthService
  private appType: 'ttms' | 'ptms'

  constructor(baseURL: string, appType: 'ttms' | 'ptms') {
    this.baseURL = baseURL
    this.appType = appType
    this.authService = appType === 'ttms' ? ttmsAuthService : ptmsAuthService

    this.axiosInstance = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    this.setupInterceptors()
  }

  private setupInterceptors(): void {
    this.axiosInstance.interceptors.request.use(
      (config: RequestConfig) => {
        const token = this.authService.getAccessToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    this.axiosInstance.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const config = error.config as RequestConfig

        if (error.response?.status === 401 && !config._retry) {
          config._retry = true

          try {
            const refreshToken = this.authService.getRefreshToken()
            if (refreshToken) {
              await this.authService.refreshToken(refreshToken, this.appType)
              const newToken = this.authService.getAccessToken()
              if (newToken && config.headers) {
                config.headers.Authorization = `Bearer ${newToken}`
              }
              return this.axiosInstance(config)
            }
          } catch (refreshError) {
            this.authService.logout(this.appType)
            window.location.href = '/login'
            return Promise.reject(refreshError)
          }
        }

        return Promise.reject(error)
      }
    )
  }

  public getAxiosInstance(): AxiosInstance {
    return this.axiosInstance
  }

  public get<T>(url: string, config = {}) {
    return this.axiosInstance.get<T>(url, config)
  }

  public post<T>(url: string, data?: any, config = {}) {
    return this.axiosInstance.post<T>(url, data, config)
  }

  public put<T>(url: string, data?: any, config = {}) {
    return this.axiosInstance.put<T>(url, data, config)
  }

  public patch<T>(url: string, data?: any, config = {}) {
    return this.axiosInstance.patch<T>(url, data, config)
  }

  public delete<T>(url: string, config = {}) {
    return this.axiosInstance.delete<T>(url, config)
  }
}

export const ttmsApi = new ApiClient(
  import.meta.env.VITE_TTMS_API_URL || 'http://localhost:8000/api/ttms',
  'ttms'
)

export const ptmsApi = new ApiClient(
  import.meta.env.VITE_PTMS_API_URL || 'http://localhost:8001/api/ptms',
  'ptms'
)
```

---

## Section 4: React Implementation

### 4.1 Login Component

Create `src/pages/LoginPage.tsx`:

```typescript
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ttmsAuthService } from '../services/auth.service'

interface LoginPageProps {
  appType: 'ttms' | 'ptms'
}

export function LoginPage({ appType }: LoginPageProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await ttmsAuthService.login(email, password, appType)
      navigate(appType === 'ttms' ? '/ttms/dashboard' : '/ptms/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-6">
          {appType === 'ttms' ? 'TTMS Login' : 'PTMS Login'}
        </h2>

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium mb-2">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="mb-6">
            <label htmlFor="password" className="block text-sm font-medium mb-2">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

### 4.2 Protected Route Component

Create `src/components/ProtectedRoute.tsx`:

```typescript
import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { ttmsAuthService, ptmsAuthService } from '../services/auth.service'

interface ProtectedRouteProps {
  children: ReactNode
  appType: 'ttms' | 'ptms'
}

export function ProtectedRoute({ children, appType }: ProtectedRouteProps) {
  const authService = appType === 'ttms' ? ttmsAuthService : ptmsAuthService
  const isAuthenticated = authService.isAuthenticated()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}
```

### 4.3 API Call Examples - TTMS Data

Create `src/services/ttms.service.ts`:

```typescript
import { ttmsApi } from './api'

export interface KPIMetrics {
  id: number
  capacity_utilization: number
  turnaround_avg_day: number
  turnaround_avg_cum: number
  vehicles_in_day: number
  vehicles_out_day: number
  dispatch_today: number
}

export interface Vehicle {
  id: number
  reg_no: string
  progress: number
  turnaround_time: number
  tare_weight: number
  weight_after_loading: number
}

export interface SystemAlert {
  id: number
  level: 'critical' | 'warning' | 'info' | 'success'
  message: string
  is_resolved: boolean
  created_at: string
}

export class TTMSService {
  async getKPIMetrics() {
    const response = await ttmsApi.get<KPIMetrics>('/kpi/')
    return response.data
  }

  async getVehicles(params?: { limit?: number; offset?: number }) {
    const response = await ttmsApi.get<{
      results: Vehicle[]
      count: number
      next?: string
      previous?: string
    }>('/vehicles/', { params })
    return response.data
  }

  async getVehicleById(id: number) {
    const response = await ttmsApi.get<Vehicle>(`/vehicles/${id}/`)
    return response.data
  }

  async getParkingCells() {
    const response = await ttmsApi.get('/parking-cells/')
    return response.data
  }

  async getAlerts(params?: { is_resolved?: boolean }) {
    const response = await ttmsApi.get<SystemAlert[]>('/alerts/', { params })
    return response.data
  }

  async getSparklineData() {
    const response = await ttmsApi.get('/sparkline/')
    return response.data
  }

  async getVehicleEntries() {
    const response = await ttmsApi.get('/vehicle-entries/')
    return response.data
  }
}

export const ttmsService = new TTMSService()
```

### 4.4 API Call Examples - PTMS Data

Create `src/services/ptms.service.ts`:

```typescript
import { ptmsApi } from './api'

export interface Project {
  id: number
  name: string
  description: string
  status: 'active' | 'completed' | 'on_hold' | 'cancelled'
  created_at: string
  updated_at: string
}

export interface Task {
  id: number
  project: number
  title: string
  description: string
  status: 'pending' | 'in_progress' | 'completed' | 'blocked'
  priority: 'low' | 'medium' | 'high' | 'critical'
  due_date?: string
  created_at: string
  updated_at: string
}

export class PTMSService {
  async getProjects(params?: { status?: string }) {
    const response = await ptmsApi.get<{
      results: Project[]
      count: number
    }>('/projects/', { params })
    return response.data
  }

  async getProjectById(id: number) {
    const response = await ptmsApi.get<Project>(`/projects/${id}/`)
    return response.data
  }

  async getTasks(params?: { status?: string; priority?: string; project?: number }) {
    const response = await ptmsApi.get<{
      results: Task[]
      count: number
    }>('/tasks/', { params })
    return response.data
  }

  async getTaskById(id: number) {
    const response = await ptmsApi.get<Task>(`/tasks/${id}/`)
    return response.data
  }

  async updateTask(id: number, data: Partial<Task>) {
    const response = await ptmsApi.put<Task>(`/tasks/${id}/`, data)
    return response.data
  }

  async createProject(data: { name: string; description: string }) {
    const response = await ptmsApi.post<Project>('/projects/', data)
    return response.data
  }
}

export const ptmsService = new PTMSService()
```

### 4.5 Dashboard Component with Real Data

Create `src/pages/TTMSDashboard.tsx`:

```typescript
import { useEffect, useState } from 'react'
import { ttmsService } from '../services/ttms.service'
import { Spinner } from '../components/ui/Spinner'
import { Alert } from '../components/ui/Alert'

export function TTMSDashboard() {
  const [kpis, setKpis] = useState(null)
  const [vehicles, setVehicles] = useState([])
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true)
        const [kpiData, vehiclesData, alertsData] = await Promise.all([
          ttmsService.getKPIMetrics(),
          ttmsService.getVehicles({ limit: 10 }),
          ttmsService.getAlerts({ is_resolved: false })
        ])

        setKpis(kpiData)
        setVehicles(vehiclesData.results || [])
        setAlerts(alertsData || [])
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data')
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  if (loading) return <Spinner />
  if (error) return <Alert type="error">{error}</Alert>

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">TTMS Dashboard</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded shadow">
          <div className="text-gray-600 text-sm">Capacity Utilization</div>
          <div className="text-3xl font-bold text-blue-600">
            {kpis?.capacity_utilization}%
          </div>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <div className="text-gray-600 text-sm">Avg Turnaround (Day)</div>
          <div className="text-3xl font-bold text-green-600">
            {kpis?.turnaround_avg_day}min
          </div>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <div className="text-gray-600 text-sm">Vehicles In (Today)</div>
          <div className="text-3xl font-bold text-purple-600">
            {kpis?.vehicles_in_day}
          </div>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <div className="text-gray-600 text-sm">Dispatch Today</div>
          <div className="text-3xl font-bold text-orange-600">
            {kpis?.dispatch_today}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-bold mb-4">Active Vehicles</h2>
          <div className="space-y-2">
            {vehicles.map((vehicle) => (
              <div key={vehicle.id} className="flex justify-between p-2 border-b">
                <span>{vehicle.reg_no}</span>
                <span className="text-sm text-gray-600">{vehicle.progress}%</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-bold mb-4">Active Alerts</h2>
          <div className="space-y-2">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className={`p-2 rounded text-sm ${
                  alert.level === 'critical'
                    ? 'bg-red-100 text-red-700'
                    : alert.level === 'warning'
                    ? 'bg-yellow-100 text-yellow-700'
                    : 'bg-blue-100 text-blue-700'
                }`}
              >
                {alert.message}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
```

### 4.6 Token Refresh & Logout Flow

Create a custom hook in `src/hooks/useAuth.ts`:

```typescript
import { useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { ttmsAuthService, ptmsAuthService } from '../services/auth.service'

export function useAuth(appType: 'ttms' | 'ptms') {
  const authService = appType === 'ttms' ? ttmsAuthService : ptmsAuthService
  const navigate = useNavigate()

  const logout = useCallback(async () => {
    try {
      await authService.logout(appType)
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      navigate('/login')
    }
  }, [authService, appType, navigate])

  const refreshToken = useCallback(async () => {
    try {
      const refreshToken = authService.getRefreshToken()
      if (refreshToken) {
        await authService.refreshToken(refreshToken, appType)
        return true
      }
      return false
    } catch (error) {
      console.error('Token refresh failed:', error)
      await logout()
      return false
    }
  }, [authService, appType, logout])

  return {
    isAuthenticated: authService.isAuthenticated(),
    user: authService.getUser(),
    logout,
    refreshToken
  }
}
```

---

## Section 5: CORS Configuration

### 5.1 Backend CORS Settings

CORS is already configured in `backend/core/settings_ttms.py` and `backend/core/settings_ptms.py`:

```python
# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
```

### 5.2 Frontend Proxy Configuration

The Vite proxy (shown in Section 1.2) handles CORS locally during development:

```typescript
server: {
  proxy: {
    '/api/ttms': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
    '/api/ptms': {
      target: 'http://localhost:8001',
      changeOrigin: true,
    }
  }
}
```

### 5.3 Production Deployment

For production, update environment variables:

```env
VITE_TTMS_API_URL=https://api.example.com/api/ttms
VITE_PTMS_API_URL=https://api.example.com/api/ptms
```

And update backend CORS settings:

```python
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://www.example.com",
]
```

---

## Troubleshooting

### Issue: CORS Error

**Error:** `Access to XMLHttpRequest has been blocked by CORS policy`

**Solutions:**
1. Check backend `CORS_ALLOWED_ORIGINS` includes your frontend domain
2. Verify `changeOrigin: true` in Vite proxy
3. Check request includes proper headers

### Issue: 401 Unauthorized

**Error:** `Unauthorized: Invalid credentials`

**Solutions:**
1. Verify token is being sent in Authorization header
2. Check token hasn't expired
3. Verify backend auth endpoint is working: `curl -X GET http://localhost:8000/api/ttms/auth/users/me/ -H "Authorization: Bearer YOUR_TOKEN"`

### Issue: Token Not Persisting

**Error:** Token lost after page refresh

**Solutions:**
1. Check browser localStorage is enabled
2. Verify auth service is using correct storage keys
3. Check browser console for storage errors

### Issue: API Endpoints Not Found

**Error:** `404 Not Found`

**Solutions:**
1. Verify API URL in environment variables
2. Check backend app is running: `curl http://localhost:8000/api/ttms/`
3. Verify endpoint path matches backend routes

### Debug Mode

Enable debug logging in `.env.local`:

```env
VITE_DEBUG=true
```

Then in your API client:

```typescript
if (import.meta.env.VITE_DEBUG) {
  console.log('Request:', config)
  console.log('Response:', response)
}
```

---

## Next Steps

1. Set up environment variables in `.env.local`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`
4. Login with test credentials
5. View populated dashboards with sample data
6. Check console for any errors

For API reference, see [API_REFERENCE.md](./API_REFERENCE.md)
For quick start guide, see [QUICKSTART.md](./QUICKSTART.md)
