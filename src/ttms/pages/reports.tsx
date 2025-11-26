"use client"

import { useEffect, useMemo, useState } from 'react'
import DashboardLayout from '@/components/layout/DashboardLayout'
import SearchHeader from '@/components/reports/SearchHeader'
import ProcessTimeline from '@/components/reports/ProcessTimeline'
import SummaryCards from '@/components/reports/SummaryCards'
import TotalTimeStackedBar from '@/components/reports/TotalTimeStackedBar'
import { ReportStep, ReportStepKey } from '@/types/reports'
import { useRealTimeData } from '@/hooks/useRealTimeData'
import { VehicleRow } from '@/types/vehicle'
import { ttmsService } from '@/services/ttms.service'

const baseSteps: ReportStep[] = [
  { key: 'gateEntry', label: 'Gate Entry', minutes: 15, color: '#1976D2' },
  { key: 'tareWeight', label: 'Tare Weight', minutes: 9, color: '#9E9E9E' },
  { key: 'loading', label: 'Loading', minutes: 35, color: '#FF9800' },
  { key: 'postLoadingWeight', label: 'Weight after Loading', minutes: 13, color: '#FFC107' },
  { key: 'gateExit', label: 'Gate Exit', minutes: 18, color: '#4CAF50' },
]

function mapVehicleToSteps(row: VehicleRow): ReportStep[] {
  if (!row) return baseSteps
  const s = row.stages
  const getMin = (k: keyof typeof s, fallback = 0) => {
    const st = s[k]
    if (!st) return fallback
    return Math.max(0, Math.round(st.waitTime || st.stdTime || fallback))
  }

  return [
    { key: 'gateEntry', label: 'Gate Entry', minutes: getMin('gateEntry'), color: '#1976D2' },
    { key: 'tareWeight', label: 'Tare Weight', minutes: getMin('tareWeighing' as any), color: '#9E9E9E' },
    { key: 'loading', label: 'Loading', minutes: getMin('loading'), color: '#FF9800' },
    { key: 'postLoadingWeight', label: 'Weight after Loading', minutes: getMin('postLoadingWeighing' as any), color: '#FFC107' },
    { key: 'gateExit', label: 'Gate Exit', minutes: getMin('gateExit'), color: '#4CAF50' },
  ]
}

export default function TTMSReportsPage() {
  const { vehicleData } = useRealTimeData()

  const [vehicle, setVehicle] = useState<string>('')
  const [shift, setShift] = useState<'Day'|'Shift-A'|'Shift-B'|'Shift-C'>('Day')
  const [active, setActive] = useState<ReportStepKey>('loading')
  const [steps, setSteps] = useState<ReportStep[]>(baseSteps)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const t = setTimeout(() => setLoading(false), 600)
    return () => clearTimeout(t)
  }, [])

  useEffect(() => {
    const iv = setInterval(() => {
      setSteps((prev) => prev.map((s) => ({
        ...s,
        minutes: Math.max(1, Math.round(s.minutes + (Math.random() - 0.5) * (s.key === 'loading' ? 2 : 1)))
      })))
    }, 30000)
    return () => clearInterval(iv)
  }, [])

  useEffect(() => {
    let cancelled = false
    const load = async () => {
      if (!vehicle) {
        setSteps(baseSteps)
        return
      }
      // resolve vehicle id by reg no
      const v = await ttmsService.findVehicleByRegNo(vehicle)
      if (!v) {
        setSteps(baseSteps)
        return
      }
      const stages = await ttmsService.getVehicleStagesByVehicle(v.id)
      if (cancelled) return
      const toMin = (ms: number) => Math.max(0, Math.round(ms))
      const byKey: Record<string, number> = {}
      stages.forEach(s => {
        const k = s.stage
        const val = (s as any).time_taken ?? 0
        byKey[k] = typeof val === 'number' ? val : 0
      })
      const mapped: ReportStep[] = [
        { key: 'gateEntry', label: 'Gate Entry', minutes: byKey['gateEntry'] ?? 0, color: '#1976D2' },
        { key: 'tareWeight', label: 'Tare Weight', minutes: byKey['tareWeighing'] ?? 0, color: '#9E9E9E' },
        { key: 'loading', label: 'Loading', minutes: byKey['loading'] ?? 0, color: '#FF9800' },
        { key: 'postLoadingWeight', label: 'Weight after Loading', minutes: byKey['postLoadingWeighing'] ?? 0, color: '#FFC107' },
        { key: 'gateExit', label: 'Gate Exit', minutes: byKey['gateExit'] ?? 0, color: '#4CAF50' },
      ]
      setSteps(mapped)
    }
    load()
    return () => { cancelled = true }
  }, [vehicle, vehicleData])

  const totals = useMemo(() => steps.reduce((t, s) => t + s.minutes, 0), [steps])

  return (
    <DashboardLayout>
      <div className="space-y-4">
        <div className="w-full">
          <SummaryCards horizontal />
        </div>

        <div>
          <SearchHeader value={vehicle} onVehicleChange={setVehicle} shift={shift} onShiftChange={setShift} />
        </div>

        <div className="space-y-4">
          <ProcessTimeline steps={steps} active={active} onSelect={setActive} vehicle={vehicle} />
          <TotalTimeStackedBar steps={steps} active={active} onSelect={setActive} />
        </div>

      </div>
    </DashboardLayout>
  )
}
