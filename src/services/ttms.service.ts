import { ttmsApi } from './api'
import { KPIData, CapacityData, TurnaroundData, VehiclesData, DispatchData } from '@/types/kpi'
import { VehicleRow, StageKey, StageState } from '@/types/vehicle'
import { ParkingData } from '@/types/dashboard'

export interface KPIMetricsResponse {
  capacity_utilization: number
  plant_capacity: number
  trucks_inside: number
  capacity_trend_direction: 'up' | 'down'
  capacity_trend_percentage: number
  turnaround_avg_day: number
  turnaround_avg_cum: number
  turnaround_last_year: number
  turnaround_trend_direction: 'up' | 'down'
  turnaround_trend_percentage: number
  turnaround_performance_color: string
  vehicles_in_day: number
  vehicles_out_day: number
  vehicles_in_cum: number
  vehicles_out_cum: number
  vehicles_trend_direction: 'up' | 'down'
  vehicles_trend_percentage: number
  vehicles_target: number
  dispatch_today: number
  dispatch_cum_month: number
  dispatch_target_day: number
  dispatch_trend_direction: 'up' | 'down'
  dispatch_trend_percentage: number
  created_at: string
  updated_at: string
}

export interface VehicleResponse {
  id: number
  reg_no: string
  rfid_no: string
  tare_weight: number
  weight_after_loading: number
  progress: number
  turnaround_time: number
  timestamp: string
  stages: Array<{
    id: number
    stage: StageKey
    state: 'pending' | 'active' | 'completed'
    wait_time: number
    standard_time: number
  }>
  created_at: string
  updated_at: string
}

export interface VehiclesListResponse {
  count: number
  next: string | null
  previous: string | null
  results: VehicleResponse[]
}

export interface ParkingCell {
  id: number
  area: string
  label: string
  status: 'available' | 'occupied' | 'reserved'
  vehicle?: number
  vehicle_reg_no?: string
  created_at: string
  updated_at: string
}

export interface ParkingListResponse {
  count: number
  next: string | null
  previous: string | null
  results: ParkingCell[]
}

export interface SystemAlert {
  id: number
  level: 'critical' | 'warning' | 'info' | 'success'
  message: string
  vehicle?: number
  vehicle_reg_no?: string
  is_resolved: boolean
  created_at: string
  resolved_at?: string
}

export interface AlertsListResponse {
  count: number
  next: string | null
  previous: string | null
  results: SystemAlert[]
}

export interface SparklinePoint {
  v: number
}

export class TTMSService {
  async getKPIMetrics(): Promise<KPIData> {
    try {
      const response = await ttmsApi.get<{ results: KPIMetricsResponse[] }>('/kpi/')
      const kpi = response.results[0]

      if (!kpi) {
        throw new Error('No KPI data available')
      }

      return {
        capacity: {
          utilization: kpi.capacity_utilization,
          plantCapacity: kpi.plant_capacity,
          trucksInside: kpi.trucks_inside,
          trend: {
            direction: kpi.capacity_trend_direction,
            percentage: kpi.capacity_trend_percentage,
          },
        } as CapacityData,
        turnaround: {
          avgDay: kpi.turnaround_avg_day,
          avgCum: kpi.turnaround_avg_cum,
          lastYear: kpi.turnaround_last_year,
          trend: {
            direction: kpi.turnaround_trend_direction,
            percentage: kpi.turnaround_trend_percentage,
          },
          performanceColor: (kpi.turnaround_performance_color as any) || 'blue',
          sparkline: await this.getSparklineData(),
        } as TurnaroundData,
        vehicles: {
          inDay: kpi.vehicles_in_day,
          outDay: kpi.vehicles_out_day,
          inCum: kpi.vehicles_in_cum,
          outCum: kpi.vehicles_out_cum,
          trend: {
            direction: kpi.vehicles_trend_direction,
            percentage: kpi.vehicles_trend_percentage,
          },
          target: kpi.vehicles_target,
        } as VehiclesData,
        dispatch: {
          today: kpi.dispatch_today,
          cumMonth: kpi.dispatch_cum_month,
          targetDay: kpi.dispatch_target_day,
          trend: {
            direction: kpi.dispatch_trend_direction,
            percentage: kpi.dispatch_trend_percentage,
          },
        } as DispatchData,
      }
    } catch (error) {
      console.error('Failed to fetch KPI data:', error)
      throw error
    }
  }

  async getVehicles(limit: number = 25, offset: number = 0): Promise<VehicleRow[]> {
    try {
      const response = await ttmsApi.get<VehiclesListResponse>(
        `/vehicles/?limit=${limit}&offset=${offset}`
      )

      return response.results.map((vehicle) => {
        const stageRecord: Record<StageKey, StageState> = {
          gateEntry: { state: 'pending', waitTime: 0, stdTime: 30 },
          tareWeighing: { state: 'pending', waitTime: 0, stdTime: 30 },
          loading: { state: 'pending', waitTime: 0, stdTime: 30 },
          postLoadingWeighing: { state: 'pending', waitTime: 0, stdTime: 30 },
          gateExit: { state: 'pending', waitTime: 0, stdTime: 30 },
        }

        vehicle.stages.forEach((stage) => {
          if (stageRecord[stage.stage]) {
            stageRecord[stage.stage] = {
              state: stage.state as any,
              waitTime: stage.wait_time,
              stdTime: stage.standard_time,
            }
          }
        })

        return {
          sn: vehicle.id,
          regNo: vehicle.reg_no,
          rfidNo: vehicle.rfid_no,
          tareWt: vehicle.tare_weight,
          wtAfter: vehicle.weight_after_loading,
          progress: vehicle.progress,
          ttr: vehicle.turnaround_time,
          timestamp: vehicle.timestamp,
          stages: stageRecord,
        } as VehicleRow
      })
    } catch (error) {
      console.error('Failed to fetch vehicles:', error)
      throw error
    }
  }

  async getParking(): Promise<ParkingData> {
    try {
      const response = await ttmsApi.get<ParkingListResponse>('/parking/')

      const parkingByArea: Record<string, { status: string; label: string }[][]> = {}

      response.results.forEach((cell) => {
        if (!parkingByArea[cell.area]) {
          parkingByArea[cell.area] = []
        }
      })

      Object.keys(parkingByArea).forEach((area) => {
        const cells = response.results.filter((c) => c.area === area)
        const grid: { status: string; label: string }[][] = []
        const rowSize = 5

        for (let i = 0; i < cells.length; i += rowSize) {
          grid.push(
            cells.slice(i, i + rowSize).map((cell) => ({
              status: cell.status,
              label: cell.label,
            }))
          )
        }

        parkingByArea[area] = grid
      })

      return parkingByArea as ParkingData
    } catch (error) {
      console.error('Failed to fetch parking data:', error)
      throw error
    }
  }

  async getAlerts(): Promise<SystemAlert[]> {
    try {
      const response = await ttmsApi.get<AlertsListResponse>('/alerts/')
      return response.results
    } catch (error) {
      console.error('Failed to fetch alerts:', error)
      return []
    }
  }

  async getSparklineData(): Promise<SparklinePoint[]> {
    try {
      const response = await ttmsApi.get<{ results: { value: number }[] }>(
        '/sparkline/recent/'
      )

      return (response.results || []).map((point) => ({
        v: point.value,
      }))
    } catch (error) {
      console.warn('Failed to fetch sparkline data, using empty array:', error)
      return []
    }
  }
}

export const ttmsService = new TTMSService()
