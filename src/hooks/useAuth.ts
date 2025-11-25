import { useCallback, useState, useEffect } from 'react'
import { authService, User } from '@/services/auth.service'

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const currentUser = authService.getUser()
    setUser(currentUser)
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    setLoading(true)
    setError(null)
    try {
      const response = await authService.login(email, password)
      setUser(response.user || null)
      return response
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Login failed'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = useCallback(async () => {
    setLoading(true)
    try {
      await authService.logout()
      setUser(null)
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  const isAuthenticated = !!user || authService.isAuthenticated()

  return {
    user,
    isAuthenticated,
    loading,
    error,
    login,
    logout,
  }
}
