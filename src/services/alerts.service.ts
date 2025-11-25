import { ttmsApi } from './api'
import { SystemAlert } from './ttms.service'

export interface AlertsListResponse {
  count: number
  next: string | null
  previous: string | null
  results: SystemAlert[]
}

export class AlertsService {
  async getAlerts(params?: {
    level?: 'critical' | 'warning' | 'info' | 'success'
    isResolved?: boolean
    limit?: number
    offset?: number
  }): Promise<SystemAlert[]> {
    try {
      const queryParams = new URLSearchParams()
      if (params?.level) queryParams.append('level', params.level)
      if (params?.isResolved !== undefined) queryParams.append('is_resolved', String(params.isResolved))
      if (params?.limit) queryParams.append('limit', String(params.limit))
      if (params?.offset) queryParams.append('offset', String(params.offset))

      const url = `/ttms/alerts/${queryParams.toString() ? '?' + queryParams.toString() : ''}`
      const response = await ttmsApi.get<AlertsListResponse>(url)
      return response.results
    } catch (error) {
      console.error('Failed to fetch alerts:', error)
      return []
    }
  }

  async getActiveAlerts(): Promise<SystemAlert[]> {
    return this.getAlerts({ isResolved: false })
  }

  async resolveAlert(id: number): Promise<SystemAlert> {
    try {
      return await ttmsApi.post<SystemAlert>(`/ttms/alerts/${id}/resolve/`, {})
    } catch (error) {
      console.error('Failed to resolve alert:', error)
      throw error
    }
  }

  async resolveAllAlerts(): Promise<{ resolved_count: number }> {
    try {
      return await ttmsApi.post<{ resolved_count: number }>('/ttms/alerts/resolve_all/', {})
    } catch (error) {
      console.error('Failed to resolve all alerts:', error)
      throw error
    }
  }

  async createAlert(data: {
    level: 'critical' | 'warning' | 'info' | 'success'
    message: string
    vehicle?: number
  }): Promise<SystemAlert> {
    try {
      return await ttmsApi.post<SystemAlert>('/ttms/alerts/', data)
    } catch (error) {
      console.error('Failed to create alert:', error)
      throw error
    }
  }
}

export const alertsService = new AlertsService()
