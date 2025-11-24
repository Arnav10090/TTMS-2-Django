# Frontend-Backend Integration Guide

This guide explains how to integrate the React frontend with the Django backend.

## Architecture Overview

```
Frontend (React/Vite)
    ↓ (HTTP/REST)
Django REST API
    ↓ (SQL)
PostgreSQL Database
```

## API Base URL Configuration

### Development Environment

Update your frontend environment or API client configuration:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';

// Or in environment variables (.env)
VITE_API_URL=http://localhost:8000/api
```

### Production Environment

```javascript
const API_BASE_URL = 'https://your-production-api.com/api';
```

## Integrating with Frontend Hooks

### Current Frontend Hook (`useRealTimeData`)

The current `useRealTimeData` hook uses mock data. Update it to call the backend:

```typescript
export function useRealTimeData() {
  const [kpiData, setKpiData] = useState<KPIData>({...});
  const [vehicleData, setVehicleData] = useState<VehicleRow[]>([]);
  const [parkingData, setParkingData] = useState<ParkingData>({...});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch KPI data
        const kpiResponse = await fetch(`${API_BASE_URL}/kpi/latest/`);
        const kpiJson = await kpiResponse.json();
        setKpiData(kpiJson);

        // Fetch vehicles
        const vehiclesResponse = await fetch(`${API_BASE_URL}/vehicles/?limit=25`);
        const vehiclesJson = await vehiclesResponse.json();
        setVehicleData(vehiclesJson.results || vehiclesJson);

        // Fetch parking
        const parkingResponse = await fetch(`${API_BASE_URL}/parking/by_area/`);
        const parkingJson = await parkingResponse.json();
        setParkingData(parkingJson);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Set up interval for real-time updates
    const interval = setInterval(fetchData, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  return { kpiData, vehicleData, parkingData, loading, allocateSpot };
}
```

## API Endpoint Mapping

### KPI Data

**Frontend expects:**
```typescript
{
  capacity: { utilization, plantCapacity, trucksInside, trend }
  turnaround: { avgDay, avgCum, lastYear, trend, performanceColor, sparkline }
  vehicles: { inDay, outDay, inCum, outCum, trend, target }
  dispatch: { today, cumMonth, targetDay, trend }
}
```

**Backend endpoint:**
```
GET /api/kpi/latest/
```

### Vehicle Data

**Frontend expects:**
```typescript
{
  sn: number
  regNo: string
  rfidNo?: string
  tareWt: number
  wtAfter: number
  progress: number
  ttr: number
  timestamp: string
  stages: { [key]: { state, waitTime, stdTime } }
}[]
```

**Backend endpoints:**
```
GET /api/vehicles/              # List all vehicles
GET /api/vehicles/{id}/         # Get single vehicle with stages
GET /api/vehicles/active/       # Get active vehicles
GET /api/vehicles/completed/    # Get completed vehicles
POST /api/vehicles/             # Create new vehicle
```

### Parking Data

**Frontend expects:**
```typescript
{
  'AREA-1': [ [ { status, label } ] ]
  'AREA-2': [ [ { status, label } ] ]
}
```

**Backend endpoints:**
```
GET /api/parking/               # List all parking cells
GET /api/parking/by_area/?area=AREA-1  # Get by area
GET /api/parking/available/     # Get available only
POST /api/parking/{id}/allocate/  # Allocate to vehicle
```

### Vehicle Entries

**Frontend expects:**
```typescript
{
  id: string
  sn: number
  gateEntryTime: string
  regNo: string
  area: string
  position: string
  loadingGate: string
  selected: boolean
}[]
```

**Backend endpoints:**
```
GET /api/entries/               # List entries
GET /api/entries/today/         # Get today's entries
POST /api/entries/              # Create entry
```

## Request/Response Examples

### GET KPI Data

```bash
curl -X GET http://localhost:8000/api/kpi/latest/
```

Response:
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
      {"v": 95},
      ...
    ]
  },
  ...
}
```

### GET Vehicles

```bash
curl -X GET http://localhost:8000/api/vehicles/
```

Response:
```json
{
  "count": 25,
  "next": null,
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
        ...
      ]
    }
  ]
}
```

### POST Create Vehicle

```bash
curl -X POST http://localhost:8000/api/vehicles/ \
  -H "Content-Type: application/json" \
  -d '{
    "reg_no": "MH12-1002",
    "rfid_no": "RFID-1002",
    "tare_weight": 2500,
    "weight_after_loading": 5200,
    "progress": 0,
    "turnaround_time": 0
  }'
```

## CORS Configuration

The backend is pre-configured for CORS. For development, it allows:

```
http://localhost:5173
http://127.0.0.1:5173
```

To add more origins, update `.env`:

```
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,https://yoursite.com
```

## Authentication (Optional)

For future authentication, add to your API calls:

```javascript
const response = await fetch(`${API_BASE_URL}/vehicles/`, {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});
```

## Error Handling

Implement error handling in your frontend:

```typescript
try {
  const response = await fetch(`${API_BASE_URL}/vehicles/`);
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  const data = await response.json();
  // Process data
} catch (error) {
  console.error('Error:', error);
  // Show error to user
}
```

## Pagination

The API supports pagination with the default page size of 100:

```
GET /api/vehicles/?page=1&page_size=50
```

## Filtering and Search

Vehicles support search:

```
GET /api/vehicles/?search=MH12-1001
GET /api/vehicles/?ordering=-turnaround_time
```

## Real-Time Data Updates

For real-time updates, implement WebSockets or polling:

### Option 1: Polling (Current Implementation)
```javascript
const interval = setInterval(fetchData, 30000); // Update every 30 seconds
```

### Option 2: WebSockets (Future Enhancement)
Consider upgrading to Django Channels for WebSocket support.

## Development Workflow

1. Start backend:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. Start frontend:
   ```bash
   npm run dev
   ```

3. Frontend runs at `http://localhost:5173`
4. Backend runs at `http://localhost:8000`
5. API available at `http://localhost:8000/api/`

## Testing API Endpoints

Use tools like:
- **Postman**: Desktop app for API testing
- **curl**: Command-line tool
- **Thunder Client**: VS Code extension
- **REST Client**: VS Code extension

Example REST Client file (`.http`):

```http
### Get KPI Data
GET http://localhost:8000/api/kpi/latest/

### Get Vehicles
GET http://localhost:8000/api/vehicles/?limit=10

### Create Vehicle
POST http://localhost:8000/api/vehicles/
Content-Type: application/json

{
  "reg_no": "MH12-1003",
  "rfid_no": "RFID-1003",
  "tare_weight": 2500,
  "weight_after_loading": 5200,
  "progress": 0,
  "turnaround_time": 0
}
```

## Common Integration Issues

### CORS Errors
- Ensure frontend URL is in `CORS_ALLOWED_ORIGINS`
- Check backend is running on port 8000

### 404 Not Found
- Verify endpoint path
- Check API base URL configuration
- Ensure migrations are run

### Database Errors
- Verify PostgreSQL is running
- Check database credentials
- Run migrations: `python manage.py migrate`

## Database Relationships

```
Vehicle
├── stages (VehicleStage)
├── entries (VehicleEntry)
├── alerts (SystemAlert)
└── parking_assignments (ParkingCell)

ParkingCell
└── vehicle (FK to Vehicle)

VehicleEntry
└── vehicle (FK to Vehicle)

SystemAlert
└── vehicle (FK to Vehicle)
```

## Performance Optimization

For production:

1. **Enable query optimization:**
   ```python
   # Use select_related and prefetch_related
   Vehicle.objects.select_related('parking').prefetch_related('stages')
   ```

2. **Add database indexes** (through migrations)

3. **Implement caching:**
   ```python
   from django.views.decorators.cache import cache_page
   
   @cache_page(60 * 5)  # Cache for 5 minutes
   def get_kpi(request):
       ...
   ```

4. **Use pagination** for large datasets

## Next Steps

1. Test API endpoints with Postman
2. Integrate endpoints into frontend hooks
3. Test frontend-backend communication
4. Deploy to production
