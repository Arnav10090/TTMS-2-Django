# API Reference Documentation

Base URL: `http://localhost:8000/api`

## Table of Contents
1. [KPI Metrics](#kpi-metrics)
2. [Vehicles](#vehicles)
3. [Vehicle Stages](#vehicle-stages)
4. [Parking Cells](#parking-cells)
5. [Vehicle Entries](#vehicle-entries)
6. [System Alerts](#system-alerts)
7. [Sparkline Data](#sparkline-data)
8. [Error Responses](#error-responses)

---

## KPI Metrics

### Get All KPI Records
```
GET /api/kpi/
```

**Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "capacity_utilization": 72,
      "plant_capacity": 120,
      "trucks_inside": 86,
      "capacity_trend_direction": "up",
      "capacity_trend_percentage": 3.2,
      "turnaround_avg_day": 92,
      "turnaround_avg_cum": 95,
      "turnaround_last_year": 102,
      "turnaround_trend_direction": "down",
      "turnaround_trend_percentage": 1.4,
      "turnaround_performance_color": "yellow",
      "vehicles_in_day": 140,
      "vehicles_out_day": 132,
      "vehicles_in_cum": 1980,
      "vehicles_out_cum": 1968,
      "vehicles_trend_direction": "up",
      "vehicles_trend_percentage": 5.1,
      "vehicles_target": 150,
      "dispatch_today": 88,
      "dispatch_cum_month": 1220,
      "dispatch_target_day": 120,
      "dispatch_trend_direction": "up",
      "dispatch_trend_percentage": 2.3,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Latest KPI (Frontend Format)
```
GET /api/kpi/latest/
```

**Response (200 OK):**
```json
{
  "capacity": {
    "utilization": 72,
    "plantCapacity": 120,
    "trucksInside": 86,
    "trend": {
      "direction": "up",
      "percentage": 3.2
    }
  },
  "turnaround": {
    "avgDay": 92,
    "avgCum": 95,
    "lastYear": 102,
    "trend": {
      "direction": "down",
      "percentage": 1.4
    },
    "performanceColor": "yellow",
    "sparkline": [
      {"v": 85},
      {"v": 90},
      {"v": 88}
    ]
  },
  "vehicles": {
    "inDay": 140,
    "outDay": 132,
    "inCum": 1980,
    "outCum": 1968,
    "trend": {
      "direction": "up",
      "percentage": 5.1
    },
    "target": 150
  },
  "dispatch": {
    "today": 88,
    "cumMonth": 1220,
    "targetDay": 120,
    "trend": {
      "direction": "up",
      "percentage": 2.3
    }
  }
}
```

### Create/Update KPI
```
POST /api/kpi/create_or_update/
```

**Request Body:**
```json
{
  "capacity_utilization": 75,
  "plant_capacity": 120,
  "trucks_inside": 90,
  "capacity_trend_direction": "up",
  "capacity_trend_percentage": 4.5,
  "turnaround_avg_day": 88,
  "turnaround_avg_cum": 94,
  "turnaround_last_year": 102,
  "turnaround_trend_direction": "down",
  "turnaround_trend_percentage": 2.1,
  "turnaround_performance_color": "green",
  "vehicles_in_day": 145,
  "vehicles_out_day": 135,
  "vehicles_in_cum": 2000,
  "vehicles_out_cum": 1990,
  "vehicles_trend_direction": "up",
  "vehicles_trend_percentage": 5.5,
  "vehicles_target": 150,
  "dispatch_today": 92,
  "dispatch_cum_month": 1250,
  "dispatch_target_day": 120,
  "dispatch_trend_direction": "up",
  "dispatch_trend_percentage": 2.8
}
```

**Response (201 Created):**
Returns the created/updated KPI record

---

## Vehicles

### List All Vehicles
```
GET /api/vehicles/?limit=25&offset=0
```

**Query Parameters:**
- `search`: Filter by reg_no or rfid_no
- `ordering`: Sort by field name (e.g., `-turnaround_time`)
- `limit`: Items per page (default: 100)
- `offset`: Pagination offset

**Response (200 OK):**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/vehicles/?limit=25&offset=25",
  "previous": null,
  "results": [
    {
      "id": 1,
      "reg_no": "MH12-1001",
      "rfid_no": "RFID-1001",
      "tare_weight": 2500,
      "weight_after_loading": 5200,
      "progress": 45,
      "turnaround_time": 75,
      "timestamp": "2024-01-15T10:30:00Z",
      "stages": [
        {
          "id": 1,
          "stage": "gateEntry",
          "state": "completed",
          "wait_time": 15,
          "standard_time": 30
        },
        {
          "id": 2,
          "stage": "tareWeighing",
          "state": "active",
          "wait_time": 12,
          "standard_time": 30
        }
      ],
      "created_at": "2024-01-15T09:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Single Vehicle
```
GET /api/vehicles/{id}/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "reg_no": "MH12-1001",
  "rfid_no": "RFID-1001",
  "tare_weight": 2500,
  "weight_after_loading": 5200,
  "progress": 45,
  "turnaround_time": 75,
  "timestamp": "2024-01-15T10:30:00Z",
  "stages": [
    {
      "id": 1,
      "stage": "gateEntry",
      "state": "completed",
      "wait_time": 15,
      "standard_time": 30
    }
  ],
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Get Active Vehicles
```
GET /api/vehicles/active/
```

**Response (200 OK):**
Returns vehicles with active or pending stages

### Get Completed Vehicles
```
GET /api/vehicles/completed/
```

**Response (200 OK):**
Returns vehicles with completed stages

### Create Vehicle
```
POST /api/vehicles/
```

**Request Body:**
```json
{
  "reg_no": "MH12-1002",
  "rfid_no": "RFID-1002",
  "tare_weight": 2400,
  "weight_after_loading": 5100,
  "progress": 0,
  "turnaround_time": 0
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "reg_no": "MH12-1002",
  ...
}
```

### Update Vehicle Stage
```
POST /api/vehicles/{id}/update_stage/
```

**Request Body:**
```json
{
  "stage": "gateEntry",
  "data": {
    "state": "completed",
    "wait_time": 20
  }
}
```

**Response (200 OK):**
Returns updated stage data

---

## Vehicle Stages

### List All Stages
```
GET /api/stages/
```

**Query Parameters:**
- `search`: Filter by vehicle reg_no or stage name

### Get Stages by Vehicle
```
GET /api/stages/by_vehicle/?vehicle_id=1
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "stage": "gateEntry",
    "state": "completed",
    "wait_time": 15,
    "standard_time": 30
  },
  {
    "id": 2,
    "stage": "tareWeighing",
    "state": "active",
    "wait_time": 12,
    "standard_time": 30
  }
]
```

### Update Stage
```
PATCH /api/stages/{id}/
```

**Request Body:**
```json
{
  "state": "completed",
  "wait_time": 25
}
```

---

## Parking Cells

### List All Parking Cells
```
GET /api/parking/
```

**Query Parameters:**
- `search`: Filter by area, label, or status
- `ordering`: Sort by field

### Get Cells by Area
```
GET /api/parking/by_area/?area=AREA-1
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "area": "AREA-1",
    "label": "S1",
    "status": "available",
    "vehicle": null,
    "vehicle_reg_no": null,
    "created_at": "2024-01-15T09:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "area": "AREA-1",
    "label": "S2",
    "status": "occupied",
    "vehicle": 1,
    "vehicle_reg_no": "MH12-1001",
    "created_at": "2024-01-15T09:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Available Cells
```
GET /api/parking/available/
```

**Response (200 OK):**
Returns cells with status "available"

### Allocate Parking Cell
```
POST /api/parking/{id}/allocate/
```

**Request Body:**
```json
{
  "vehicle_id": 1
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "area": "AREA-1",
  "label": "S1",
  "status": "reserved",
  "vehicle": 1,
  "vehicle_reg_no": "MH12-1001",
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T10:45:00Z"
}
```

---

## Vehicle Entries

### List All Entries
```
GET /api/entries/
```

**Query Parameters:**
- `search`: Filter by vehicle reg_no, area, or loading gate
- `ordering`: Sort by field

### Get Today's Entries
```
GET /api/entries/today/
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "vehicle": 1,
    "vehicle_reg_no": "MH12-1001",
    "gate_entry_time": "2024-01-15T09:00:00Z",
    "area": "AREA-1",
    "position": "S1,S2",
    "loading_gate": "Gate-A",
    "created_at": "2024-01-15T09:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Create Entry
```
POST /api/entries/
```

**Request Body:**
```json
{
  "vehicle": 1,
  "gate_entry_time": "2024-01-15T11:00:00Z",
  "area": "AREA-1",
  "position": "S3",
  "loading_gate": "Gate-B"
}
```

---

## System Alerts

### List All Alerts
```
GET /api/alerts/
```

**Query Parameters:**
- `search`: Filter by level, message, or vehicle reg_no
- `ordering`: Sort by field

### Get Active Alerts
```
GET /api/alerts/active/
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "level": "critical",
    "message": "RFID read failure at Gate 3",
    "vehicle": 1,
    "vehicle_reg_no": "MH12-1001",
    "is_resolved": false,
    "created_at": "2024-01-15T10:15:00Z",
    "resolved_at": null
  }
]
```

### Resolve Alert
```
POST /api/alerts/{id}/resolve/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "level": "critical",
  "message": "RFID read failure at Gate 3",
  "vehicle": 1,
  "vehicle_reg_no": "MH12-1001",
  "is_resolved": true,
  "created_at": "2024-01-15T10:15:00Z",
  "resolved_at": "2024-01-15T10:20:00Z"
}
```

### Resolve All Alerts
```
POST /api/alerts/resolve_all/
```

**Response (200 OK):**
```json
{
  "resolved_count": 5
}
```

### Create Alert
```
POST /api/alerts/
```

**Request Body:**
```json
{
  "level": "warning",
  "message": "Delay at Loading Bay 2",
  "vehicle": 1
}
```

---

## Sparkline Data

### Get All Sparkline Data
```
GET /api/sparkline/
```

### Get Recent Sparkline Data
```
GET /api/sparkline/recent/
```

**Response (200 OK):**
```json
[
  {
    "id": 120,
    "timestamp": "2024-01-15T10:30:00Z",
    "value": 92
  },
  {
    "id": 119,
    "timestamp": "2024-01-15T10:00:00Z",
    "value": 95
  }
]
```

### Create Sparkline Entry
```
POST /api/sparkline/
```

**Request Body:**
```json
{
  "value": 88
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error occurred."
}
```

---

## Common Query Examples

### Search vehicles
```
GET /api/vehicles/?search=MH12
```

### Get active vehicles sorted by turnaround time
```
GET /api/vehicles/active/?ordering=-turnaround_time
```

### Get today's entries for specific area
```
GET /api/entries/today/?area=AREA-1
```

### Get unresolved critical alerts
```
GET /api/alerts/?level=critical&search=critical
```

### Paginate results
```
GET /api/vehicles/?limit=50&offset=100
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production deployments, consider adding:
- Django REST Framework's throttling classes
- redis-based rate limiting

---

## Versioning

The API is currently at version 1.0. Future versions may be introduced using:
- URL versioning: `/api/v2/vehicles/`
- Header versioning: `Accept: application/json; version=2.0`

---

## Webhook Integration (Future)

Future versions may include webhooks for:
- Vehicle status changes
- Parking space availability
- Alert notifications

Contact the development team for more information.
