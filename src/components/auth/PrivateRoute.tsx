import { Navigate } from 'react-router-dom'
import { authService } from '@/services/auth.service'

interface PrivateRouteProps {
  element: React.ReactNode
}

export function PrivateRoute({ element }: PrivateRouteProps) {
  const isAuthenticated = authService.isAuthenticated()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return element
}
