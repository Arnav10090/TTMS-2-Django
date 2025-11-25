import { ttmsApi } from './api'
import { VehicleResponse, VehiclesListResponse } from './ttms.service'
import { VehicleRow, StageKey, StageState } from '@/types/vehicle'

export class VehiclesService {
  async getVehicles(params?: {
    limit?: number
    offset?: number
    search?: string
    ordering?: string
  }): Promise<{ results: VehicleRow[]; count: number }> {
    try {
      const queryParams = new URLSearchParams()
      if (params?.limit) queryParams.append('limit', String(params.limit))
      if (params?.offset) queryParams.append('offset', String(params.offset))
      if (params?.search) queryParams.append('search', params.search)
      if (params?.ordering) queryParams.append('ordering', params.ordering)

      const url = `/ttms/vehicles/${queryParams.toString() ? '?' + queryParams.toString() : ''}`
      const response = await ttmsApi.get<VehiclesListResponse>(url)

      const results = response.results.map((vehicle) => this.mapVehicleResponse(vehicle))

      return { results, count: response.count }
    } catch (error) {
      console.error('Failed to fetch vehicles:', error)
      throw error
    }
  }

  async getVehicleById(id: number): Promise<VehicleRow> {
    try {
      const response = await ttmsApi.get<VehicleResponse>(`/ttms/vehicles/${id}/`)
      return this.mapVehicleResponse(response)
    } catch (error) {
      console.error('Failed to fetch vehicle:', error)
      throw error
    }
  }

  async getActiveVehicles(): Promise<VehicleRow[]> {
    try {
      const response = await ttmsApi.get<VehiclesListResponse>('/ttms/vehicles/active/')
      return response.results.map((vehicle) => this.mapVehicleResponse(vehicle))
    } catch (error) {
      console.error('Failed to fetch active vehicles:', error)
      return []
    }
  }

  async getCompletedVehicles(): Promise<VehicleRow[]> {
    try {
      const response = await ttmsApi.get<VehiclesListResponse>('/ttms/vehicles/completed/')
      return response.results.map((vehicle) => this.mapVehicleResponse(vehicle))
    } catch (error) {
      console.error('Failed to fetch completed vehicles:', error)
      return []
    }
  }

  async createVehicle(data: {
    reg_no: string
    rfid_no: string
    tare_weight: number
    weight_after_loading: number
  }): Promise<VehicleRow> {
    try {
      const response = await ttmsApi.post<VehicleResponse>('/ttms/vehicles/', data)
      return this.mapVehicleResponse(response)
    } catch (error) {
      console.error('Failed to create vehicle:', error)
      throw error
    }
  }

  async updateVehicleStage(
    vehicleId: number,
    stage: StageKey,
    data: {
      state: 'pending' | 'active' | 'completed'
      wait_time?: number
    }
  ): Promise<void> {
    try {
      await ttmsApi.post(`/ttms/vehicles/${vehicleId}/update_stage/`, {
        stage,
        data,
      })
    } catch (error) {
      console.error('Failed to update vehicle stage:', error)
      throw error
    }
  }

  private mapVehicleResponse(vehicle: VehicleResponse): VehicleRow {
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
  }
}

export const vehiclesService = new VehiclesService()
