# API Reference Documentation

Complete API reference for TTMS and PTMS systems.

## Base URLs

```
TTMS API:  http://localhost:8000/api/ttms
PTMS API:  http://localhost:8001/api/ptms
```

## Authentication

All API endpoints (except login and refresh) require a valid JWT access token in the Authorization header.

### Token Format
```
Authorization: Bearer {access_token}
```

---

## TTMS API Endpoints

### Authentication Endpoints

#### 1. Login
Authenticate user and receive JWT tokens.

```
POST /auth/login/
```

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Invalid credentials"
}
```

---

#### 2. Refresh Token
Refresh an expired access token using the refresh token.

```
POST /auth/refresh/
```

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

#### 3. Get Current User
Retrieve current authenticated user's information.

```
GET /auth/users/me/
```

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "operator",
  "is_active": true,
  "created_at": "2025-01-01T10:00:00Z"
}
```

---

#### 4. Change Password
Change current user's password.

```
POST /auth/users/me/change-password/
```

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "old_password": "oldpassword123",
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully."
}
```

---

#### 5. Logout
Logout user by blacklisting the refresh token.

```
POST /auth/users/logout/
```

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "message": "Logout successful."
}
```

---

### KPI Endpoints

#### 1. Get KPI Metrics
Retrieve current KPI metrics (capacity, turnaround time, vehicles, dispatch).

```
GET /kpi/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "capacity_utilization": 82,
      "plant_capacity": 120,
      "trucks_inside": 98,
      "capacity_trend_direction": "up",
      "capacity_trend_percentage": 8.5,
      "turnaround_avg_day": 45,
      "turnaround_avg_cum": 42,
      "turnaround_last_year": 52,
      "turnaround_trend_direction": "down",
      "turnaround_trend_percentage": -13.5,
      "turnaround_performance_color": "green",
      "vehicles_in_day": 38,
      "vehicles_out_day": 35,
      "vehicles_in_cum": 285,
      "vehicles_out_cum": 280,
      "vehicles_trend_direction": "up",
      "vehicles_trend_percentage": 5.2,
      "vehicles_target": 150,
      "dispatch_today": 35,
      "dispatch_cum_month": 685,
      "dispatch_target_day": 120,
      "dispatch_trend_direction": "up",
      "dispatch_trend_percentage": 12.3,
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T14:30:00Z"
    }
  ]
}
```

---

### Vehicle Endpoints

#### 1. List Vehicles
Retrieve list of all vehicles with pagination.

```
GET /vehicles/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
```
limit:  Integer, default 20 (number of results per page)
offset: Integer, default 0 (pagination offset)
search: String (search in registration number)
```

**Example Request:**
```
GET /vehicles/?limit=10&offset=0
```

**Response (200 OK):**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/ttms/vehicles/?limit=10&offset=10",
  "previous": null,
  "results": [
    {
      "id": 1,
      "reg_no": "TN01AB1234",
      "rfid_no": "RFID001",
      "tare_weight": 5000,
      "weight_after_loading": 12500,
      "progress": 80,
      "turnaround_time": 42,
      "timestamp": "2025-01-15T14:30:00Z",
      "created_at": "2025-01-15T09:45:00Z",
      "updated_at": "2025-01-15T14:27:00Z"
    }
  ]
}
```

---

#### 2. Get Vehicle Details
Retrieve specific vehicle information.

```
GET /vehicles/{id}/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "reg_no": "TN01AB1234",
  "rfid_no": "RFID001",
  "tare_weight": 5000,
  "weight_after_loading": 12500,
  "progress": 80,
  "turnaround_time": 42,
  "timestamp": "2025-01-15T14:30:00Z",
  "created_at": "2025-01-15T09:45:00Z",
  "updated_at": "2025-01-15T14:27:00Z"
}
```

---

### Parking Cell Endpoints

#### 1. List Parking Cells
Retrieve all parking cells with occupancy status.

```
GET /parking-cells/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
```
area:   String (filter by area: AREA-1, AREA-2)
status: String (filter by status: available, occupied, reserved)
```

**Response (200 OK):**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "area": "AREA-1",
      "label": "A1",
      "status": "occupied",
      "vehicle": 1,
      "created_at": "2025-01-15T09:50:00Z",
      "updated_at": "2025-01-15T14:20:00Z"
    },
    {
      "id": 2,
      "area": "AREA-1",
      "label": "A2",
      "status": "available",
      "vehicle": null,
      "created_at": "2025-01-15T09:50:00Z",
      "updated_at": "2025-01-15T14:20:00Z"
    }
  ]
}
```

---

#### 2. Get Parking Cell Details
Retrieve specific parking cell information.

```
GET /parking-cells/{id}/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "area": "AREA-1",
  "label": "A1",
  "status": "occupied",
  "vehicle": 1,
  "created_at": "2025-01-15T09:50:00Z",
  "updated_at": "2025-01-15T14:20:00Z"
}
```

---

### Vehicle Entry Endpoints

#### 1. List Vehicle Entries
Retrieve historical vehicle entries.

```
GET /vehicle-entries/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
```
vehicle:  Integer (filter by vehicle ID)
area:     String (filter by area)
limit:    Integer, default 20
offset:   Integer, default 0
```

**Response (200 OK):**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "vehicle": 1,
      "gate_entry_time": "2025-01-15T09:45:00Z",
      "area": "AREA-1",
      "position": "A1",
      "loading_gate": "Gate-01",
      "created_at": "2025-01-15T09:45:00Z",
      "updated_at": "2025-01-15T14:20:00Z"
    }
  ]
}
```

---

### Alert Endpoints

#### 1. List Alerts
Retrieve system alerts with severity levels.

```
GET /alerts/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
```
level:       String (critical, warning, info, success)
is_resolved: Boolean (true, false)
vehicle:     Integer (filter by vehicle ID)
limit:       Integer, default 20
offset:      Integer, default 0
```

**Example Request:**
```
GET /alerts/?is_resolved=false&limit=10
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
      "level": "critical",
      "message": "Vehicle TN01AB1234 delayed at loading stage - exceeds standard time by 15 minutes",
      "vehicle": 1,
      "is_resolved": false,
      "created_at": "2025-01-15T14:10:00Z",
      "resolved_at": null
    },
    {
      "id": 2,
      "level": "warning",
      "message": "Parking area AREA-2 is at 80% capacity",
      "vehicle": null,
      "is_resolved": false,
      "created_at": "2025-01-15T14:15:00Z",
      "resolved_at": null
    }
  ]
}
```

---

#### 2. Get Alert Details
Retrieve specific alert information.

```
GET /alerts/{id}/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "level": "critical",
  "message": "Vehicle TN01AB1234 delayed at loading stage",
  "vehicle": 1,
  "is_resolved": false,
  "created_at": "2025-01-15T14:10:00Z",
  "resolved_at": null
}
```

---

### Sparkline Endpoints

#### 1. Get Turnaround Time Sparkline
Retrieve historical turnaround time data for charts.

```
GET /sparkline/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "count": 30,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "timestamp": "2024-12-17T00:00:00Z",
      "value": 55
    },
    {
      "id": 2,
      "timestamp": "2024-12-18T00:00:00Z",
      "value": 52
    },
    {
      "id": 30,
      "timestamp": "2025-01-15T00:00:00Z",
      "value": 25
    }
  ]
}
```

---

## PTMS API Endpoints

### Project Endpoints

#### 1. List Projects
Retrieve all projects with optional filtering.

```
GET /projects/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
```
status: String (active, completed, on_hold, cancelled)
limit:  Integer, default 20
offset: Integer, default 0
search: String (search in project name/description)
```

**Example Request:**
```
GET /projects/?status=active&limit=10
```

**Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Warehouse Management System Upgrade",
      "description": "Complete redesign of warehouse management system",
      "status": "in_progress",
      "created_by": 1,
      "created_at": "2024-12-01T10:00:00Z",
      "updated_at": "2025-01-15T14:30:00Z"
    },
    {
      "id": 2,
      "name": "Mobile App Development",
      "description": "Native iOS and Android applications",
      "status": "in_progress",
      "created_by": 1,
      "created_at": "2024-11-15T09:30:00Z",
      "updated_at": "2025-01-15T13:45:00Z"
    }
  ]
}
```

---

#### 2. Get Project Details
Retrieve specific project information.

```
GET /projects/{id}/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Warehouse Management System Upgrade",
  "description": "Complete redesign of warehouse management system with new inventory tracking",
  "status": "in_progress",
  "created_by": 1,
  "created_at": "2024-12-01T10:00:00Z",
  "updated_at": "2025-01-15T14:30:00Z"
}
```

---

#### 3. Create Project
Create a new project.

```
POST /projects/
```

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "New Project Name",
  "description": "Project description",
  "status": "active"
}
```

**Response (201 Created):**
```json
{
  "id": 9,
  "name": "New Project Name",
  "description": "Project description",
  "status": "active",
  "created_by": 1,
  "created_at": "2025-01-15T15:00:00Z",
  "updated_at": "2025-01-15T15:00:00Z"
}
```

---

#### 4. Update Project
Update an existing project.

```
PUT /projects/{id}/
PATCH /projects/{id}/
```

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Updated Project Name",
  "status": "completed"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Updated Project Name",
  "description": "Project description",
  "status": "completed",
  "created_by": 1,
  "created_at": "2024-12-01T10:00:00Z",
  "updated_at": "2025-01-15T15:05:00Z"
}
```

---

### Task Endpoints

#### 1. List Tasks
Retrieve all tasks with optional filtering.

```
GET /tasks/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
```
project:  Integer (filter by project ID)
status:   String (pending, in_progress, completed, blocked)
priority: String (low, medium, high, critical)
assigned_to: Integer (filter by assigned user)
limit:    Integer, default 20
offset:   Integer, default 0
```

**Example Request:**
```
GET /tasks/?status=in_progress&priority=high
```

**Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "project": 1,
      "title": "Implement inventory tracking module",
      "description": "Core module for real-time inventory tracking with barcode scanning",
      "status": "in_progress",
      "priority": "high",
      "assigned_to": 2,
      "due_date": "2025-01-30T17:00:00Z",
      "created_at": "2024-12-08T09:00:00Z",
      "updated_at": "2025-01-14T15:20:00Z"
    },
    {
      "id": 3,
      "project": 1,
      "title": "Develop automated workflow engine",
      "description": "Create workflow orchestration system",
      "status": "in_progress",
      "priority": "high",
      "assigned_to": 3,
      "due_date": "2025-02-10T17:00:00Z",
      "created_at": "2024-12-15T14:00:00Z",
      "updated_at": "2025-01-13T11:30:00Z"
    }
  ]
}
```

---

#### 2. Get Task Details
Retrieve specific task information.

```
GET /tasks/{id}/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 2,
  "project": 1,
  "title": "Implement inventory tracking module",
  "description": "Core module for real-time inventory tracking with barcode scanning",
  "status": "in_progress",
  "priority": "high",
  "assigned_to": 2,
  "due_date": "2025-01-30T17:00:00Z",
  "created_at": "2024-12-08T09:00:00Z",
  "updated_at": "2025-01-14T15:20:00Z"
}
```

---

#### 3. Create Task
Create a new task within a project.

```
POST /tasks/
```

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "project": 1,
  "title": "New Task",
  "description": "Task description",
  "status": "pending",
  "priority": "high",
  "assigned_to": 2,
  "due_date": "2025-02-15T17:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "id": 26,
  "project": 1,
  "title": "New Task",
  "description": "Task description",
  "status": "pending",
  "priority": "high",
  "assigned_to": 2,
  "due_date": "2025-02-15T17:00:00Z",
  "created_at": "2025-01-15T15:00:00Z",
  "updated_at": "2025-01-15T15:00:00Z"
}
```

---

#### 4. Update Task
Update an existing task.

```
PUT /tasks/{id}/
PATCH /tasks/{id}/
```

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "status": "completed",
  "priority": "medium"
}
```

**Response (200 OK):**
```json
{
  "id": 26,
  "project": 1,
  "title": "New Task",
  "description": "Task description",
  "status": "completed",
  "priority": "medium",
  "assigned_to": 2,
  "due_date": "2025-02-15T17:00:00Z",
  "created_at": "2025-01-15T15:00:00Z",
  "updated_at": "2025-01-15T15:30:00Z"
}
```

---

#### 5. Delete Task
Delete a task.

```
DELETE /tasks/{id}/
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (204 No Content):**
```
(empty)
```

---

## Common Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Success with no response body |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but no permission |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict (e.g., duplicate) |
| 500 | Internal Server Error | Server error |

---

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error message",
  "code": "error_code"
}
```

For validation errors:

```json
{
  "field_name": ["Error message"],
  "another_field": ["Error 1", "Error 2"]
}
```

---

## Rate Limiting

API endpoints are rate limited to prevent abuse:

- **Limit**: 1000 requests per hour per IP
- **Limit-Remaining** header shows remaining requests
- **Limit-Reset** header shows when limit resets

When limit is exceeded, response is:

```
HTTP 429 Too Many Requests
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1642252800
```

---

## Pagination

List endpoints support pagination with these query parameters:

```
limit:  Number of results per page (default: 20, max: 100)
offset: Number of results to skip (default: 0)
```

Paginated responses include:

```json
{
  "count": 100,
  "next": "http://api.example.com/resource/?limit=20&offset=20",
  "previous": null,
  "results": [...]
}
```

---

## Filtering

Many endpoints support filtering. Use query parameters:

```
GET /resource/?status=active&priority=high
```

Multiple values can be comma-separated:

```
GET /resource/?status=active,pending
```

---

## API Testing

Test endpoints using curl:

```bash
# Login
curl -X POST http://localhost:8000/api/ttms/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Get KPI (replace TOKEN with actual access token)
curl -X GET http://localhost:8000/api/ttms/kpi/ \
  -H "Authorization: Bearer TOKEN"

# List projects
curl -X GET http://localhost:8001/api/ptms/projects/ \
  -H "Authorization: Bearer TOKEN"
```

---

For more information, see:
- [Frontend Integration Guide](./FRONTEND_INTEGRATION.md)
- [Quick Start Guide](./QUICKSTART.md)
