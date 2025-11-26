"use client"

import { useEffect, useState } from 'react'
import { ttmsService } from '@/services/ttms.service'

type GateStatus = 'available' | 'occupied' | 'reserved' | 'maintenance'

type Gate = { id: string; status: GateStatus; name: string; area: string }

function statusColor(s: GateStatus) {
  if (s === 'available') return 'bg-green-500'
  if (s === 'occupied') return 'bg-red-500'
  if (s === 'maintenance') return 'bg-slate-500'
  return 'bg-yellow-500' // reserved
}

export default function LoadingGateStatus() {
  const [gates, setGates] = useState<Gate[]>([])
  const [error, setError] = useState<string>('')

  const fetchGates = async () => {
    try {
      setError('')
      const res = await ttmsService.getLoadingGates()
      let items: Gate[] = (res.results || []).map((g) => ({
        id: String(g.id),
        status: (g.status as GateStatus) || 'available',
        name: g.name,
        area: g.area,
      }))
      // Ensure exactly 12 cells are shown; pad with defaults as available
      if (items.length < 12) {
        const existingNames = new Set(items.map(it => it.name))
        const needed = 12 - items.length
        const pads: Gate[] = []
        for (let i = 1; pads.length < needed && i <= 12; i++) {
          const name = `G-${i}`
          if (!existingNames.has(name)) {
            pads.push({ id: `p-${i}`, name, area: 'AREA-1', status: 'available' })
          }
        }
        items = [...items, ...pads].slice(0, 12)
      } else if (items.length > 12) {
        items = items.slice(0, 12)
      }
      // Overlay local allocations (yellow = reserved)
      try {
        const raw = localStorage.getItem('loadingGateStatuses')
        if (raw) {
          const overrides = JSON.parse(raw) as { id: string; status: GateStatus }[]
          const byId = new Map(overrides.map((o) => [o.id, o.status]))
          items = items.map((it) => (byId.has(it.name)
            ? { ...it, status: (byId.get(it.name) as GateStatus) }
            : it))
        }
      } catch {}
      setGates(items)
    } catch (e) {
      setError('Failed to load loading gate status')
    }
  }

  useEffect(() => {
    fetchGates()
    const timer = setInterval(fetchGates, 30000)
    const handler = () => {
      // reapply overrides quickly without waiting for API
      setGates((prev) => {
        let items = prev
        try {
          const raw = localStorage.getItem('loadingGateStatuses')
          if (raw) {
            const overrides = JSON.parse(raw) as { id: string; status: GateStatus }[]
            const byId = new Map(overrides.map((o) => [o.id, o.status]))
            items = prev.map((it) => (byId.has(it.name)
              ? { ...it, status: (byId.get(it.name) as GateStatus) }
              : it))
          }
        } catch {}
        return items
      })
    }
    window.addEventListener('loadingGateStatuses-updated', handler as any)
    return () => {
      clearInterval(timer)
      window.removeEventListener('loadingGateStatuses-updated', handler as any)
    }
  }, [])

  return (
    <div className="card p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-slate-800 font-semibold">Loading Gate Status</h3>
        {error && <div className="text-xs text-red-600">{error}</div>}
      </div>
      <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
        {gates.map((g) => {
          const statusLabel = g.status === 'reserved' ? 'allocated' : g.status
          return (
            <div
              key={g.id}
              className={`relative rounded-ui ${statusColor(g.status)} text-white h-12 flex items-center justify-center transition`}
              title={`${g.name} - ${statusLabel}`}
              aria-label={`${g.name} - ${statusLabel}`}
            >
              <span className="text-xs font-semibold">{g.name}</span>
              <span className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-white/80" />
            </div>
          )
        })}
      </div>
      <div className="mt-3 flex items-center gap-3 text-xs text-slate-600">
        <div className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-green-500 inline-block" /> Available</div>
        <div className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-red-500 inline-block" /> Occupied</div>
        <div className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-yellow-500 inline-block" /> Allocated</div>
        <div className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-slate-500 inline-block" /> Maintenance</div>
      </div>
    </div>
  )
}
