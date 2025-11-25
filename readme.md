# Truck Turnaround Time Monitoring System (TTR)

A comprehensive React-based dashboard application for monitoring truck turnaround times, facility management, and logistics operations. Built with modern web technologies for real-time data visualization and interactive operational management.

## Overview

The TTR Dashboard provides a centralized platform for tracking and optimizing truck turnaround times at logistics facilities. It includes features for real-time KPI monitoring, vehicle tracking, parking management, document verification, and operational scheduling.

## Tech Stack

- **Frontend Framework**: React 18 with TypeScript
- **Build Tool**: Vite (fast build and dev server)
- **Routing**: React Router v6 for client-side navigation
- **Styling**: Tailwind CSS with PostCSS and Autoprefixer
- **Charting**: Recharts for data visualization
- **Icons**: lucide-react for UI icons
- **Utilities**: date-fns for date formatting, classnames for conditional styling

## Features

### Dashboard
- **Real-time KPI Monitoring**: Track capacity utilization, turnaround times, vehicle summaries, and dispatch metrics
- **Trends & Comparisons**: View trend indicators and compare metrics across different time ranges (Today, Monthly, Yearly)
- **Parking Management**: Visual grid-based parking area management with status indicators
- **Vehicle Tracking**: Comprehensive vehicle table with progress tracking and TTR (Turnaround Time) metrics

### Additional Modules
- **Document Verification**: Upload and manage documents with RFID module integration
- **Scheduling**: Manage facility scheduling with gate status and parking area coordination
- **Reports**: Generate and view operational reports with timeline and analysis
- **Alarms**: System alerts and notifications for operational anomalies
- **Historical Data**: Access and analyze historical performance data

## Getting Started

### Prerequisites
- Node.js 16+ and npm/yarn

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```
   The app will run at `http://localhost:3000` with hot module reloading.

3. **Build for production**
   ```bash
   npm run build
   ```
   Creates an optimized production build in the `dist/` folder.

4. **Preview the production build**
   ```bash
   npm start
   ```
   Runs the built app on `http://localhost:3000` using Vite preview server.

## Project Structure

```
ttr-dashboard/
├── index.html                 # HTML entry point
├── vite.config.ts            # Vite configuration
├── tsconfig.json             # TypeScript configuration
├── tailwind.config.ts        # Tailwind CSS configuration
├── postcss.config.js         # PostCSS configuration
├── src/
│   ├── main.tsx              # React entry point
│   ├── App.tsx               # Route definitions with React Router
│   ├── app/                  # Page components (migrated from Next.js structure)
│   │   ├── layout.tsx        # App layout wrapper
│   │   ├── globals.css       # Global styles
│   │   ├── page.tsx          # Main dashboard page
│   │   ├── alarms/page.tsx   # Alarms page
│   │   ├── document-verification/page.tsx
│   │   ├── history/page.tsx
│   │   ├── reports/page.tsx  # Reports page
│   │   ├── scheduling/page.tsx # Scheduling page
│   │   └── spare/page.tsx
│   ├── components/
│   │   ├── layout/           # Layout components
│   │   │   ├── DashboardLayout.tsx  # Main layout wrapper
│   │   │   ├── Header.tsx           # Header with title and date
│   │   │   ├── Navigation.tsx       # Main navigation bar
│   │   │   └── FetchGuard.tsx
│   │   ├── dashboard/        # Dashboard-specific components
│   │   │   ├── AlertBanner.tsx      # Ticker alert banner
│   │   │   ├── CapacityUtilizationKPI.tsx  # Capacity metrics
│   │   │   ├── TurnaroundTimeKPI.tsx       # TTR metrics
│   │   │   ├── VehicleSummaryKPI.tsx      # Vehicle counts
│   │   │   ├── DispatchSummaryKPI.tsx     # Dispatch metrics
│   │   │   ├── ParkingGrid.tsx     # Parking area visualization
│   │   │   └── VehicleTable.tsx    # Vehicle tracking table
│   │   ├── charts/           # Chart components
│   │   │   ├── KPISmallChart.tsx    # Small sparkline charts
│   │   │   ├── TrendsChart.tsx      # Trends comparison chart
│   │   │   └── Sparkline.tsx
│   │   ├── document/         # Document verification components
│   │   │   ├── DocumentUploadZone.tsx
│   │   │   ├── DocumentViewer.tsx
│   │   │   ├── DriverHelperDetails.tsx
│   │   │   ├── GateSelector.tsx
│   │   │   ├── ProgressTracker.tsx
│   │   │   ├── RFIDModule.tsx
│   │   │   ├── SearchableOrderList.tsx
│   │   │   └── SignaturePad.tsx
│   │   ├── filters/          # Filter components
│   │   │   ├── DayWiseFilter.tsx
│   │   │   ├── PeriodFilter.tsx
│   │   │   └── VehicleSearch.tsx
│   │   ├── scheduling/       # Scheduling module components
│   │   │   ├── AlertBar.tsx
│   │   │   ├── FacilityMap.tsx
│   │   │   ├── LoadingGateStatus.tsx
│   │   │   ├── ManualsList.tsx
│   │   │   ├── MultiSelectDropdown.tsx
│   │   │   ├── SchedulingParkingArea.tsx
│   │   │   ├── SchedulingParkingToggle.tsx
│   │   │   ├── Tabs.tsx
│   │   │   └── VehicleEntryTable.tsx
│   │   ├── reports/          # Reports module components
│   │   │   ├── InfoPanel.tsx
│   │   │   ├── ProcessTimeline.tsx
│   │   │   ├── SearchHeader.tsx
│   │   │   ├── SummaryCards.tsx
│   │   │   ├── SystemAlertsBanner.tsx
│   │   │   └── TotalTimeStackedBar.tsx
│   │   └── ui/               # Reusable UI components
│   │       ├── AlertModal.tsx
│   │       ├── Badge.tsx
│   │       ├── Button.tsx
│   │       ├── KPICard.tsx          # KPI card wrapper
│   │       ├── Modal.tsx
│   │       ├── ProgressBar.tsx
│   │       ├── TimeRangeHint.tsx    # Data range hint
│   │       └── TimeRangeToggle.tsx  # Time period selector
│   ├── hooks/                # Custom React hooks
│   │   ├── useRealTimeData.ts  # Data fetching and state management
│   │   └── useSchedulingState.ts
│   ├── services/             # API/data services
│   │   └── dashboardService.ts # Mock data and API calls
│   ├── types/                # TypeScript type definitions
│   │   ├── dashboard.ts      # Dashboard data types (ParkingData, etc.)
│   │   ├── kpi.ts            # KPI-related types (CapacityData, TurnaroundData, etc.)
│   │   ├── reports.ts        # Reports data types
│   │   └── vehicle.ts        # Vehicle-related types
│   └── utils/                # Utility functions
│       ├── formatters.ts     # Number and date formatting
│       ├── colors.ts         # Color utilities
│       ├── alerts.ts         # Alert utilities
│       └── range.ts          # Range calculation utilities
└── package.json              # Project dependencies and scripts
```

## Core Components & Features

### Dashboard (Home Page)
The main dashboard (`src/app/page.tsx`) displays:

1. **Time Range Controls** - Toggle between Today, Monthly, Yearly, or Compare views
2. **KPI Cards Grid** - Four key performance indicators:
   - **Capacity Utilization**: Current plant capacity usage with trend
   - **Turnaround Time**: Average TTR with historical comparison
   - **Vehicle Summary**: In/Out vehicles for day and cumulative
   - **Dispatch Summary**: Daily dispatch metrics and targets

3. **Parking Grid** - Visual representation of parking areas with availability status
4. **Vehicle Table** - List of active vehicles with progress, TTR, and stage tracking

### Navigation
- Main Dashboard
- Document Verification
- Scheduling
- Reports
- Alarms
- Historical Data
- Spare Tab

## Data Architecture

### Real-time Data Management
The application uses `useRealTimeData` hook for centralized data management:

- **KPI Data**: Capacity, turnaround, vehicle, and dispatch metrics
- **Vehicle Data**: Vehicle tracking with progress and stage information
- **Parking Data**: Two parking areas (AREA-1, AREA-2) with status tracking

Data is fetched from `dashboardService` and updated every 30 seconds for real-time visualization.

### State Management
- React hooks for local component state
- Custom `useRealTimeData` hook for shared dashboard state
- LocalStorage for persisting parking status overrides and vehicle-to-parking assignments

### Data Types

**KPI Data**:
```typescript
{
  capacity: { utilization, plantCapacity, trucksInside, trend }
  turnaround: { avgDay, avgCum, lastYear, trend, performanceColor, sparkline }
  vehicles: { inDay, outDay, inCum, outCum, trend, target }
  dispatch: { today, cumMonth, targetDay, trend }
}
```

**Vehicle Row**:
```typescript
{
  sn, regNo, rfidNo, tareWt, wtAfter, progress, ttr, timestamp,
  stages: { gateEntry, tareWeighing, loading, postLoadingWeighing, gateExit }
}
```

**Parking Data**:
```typescript
{
  'AREA-1': ParkingCell[][]
  'AREA-2': ParkingCell[][]
}
```

## Key Utilities

- **Formatters** (`utils/formatters.ts`): Number formatting, date/time display
- **Colors** (`utils/colors.ts`): Status-based color mapping
- **Alerts** (`utils/alerts.ts`): Alert message handling
- **Range** (`utils/range.ts`): Numeric range generation

## Configuration

### Tailwind CSS
Custom Tailwind configuration includes:
- Custom colors (cssPrimary, secondary, success, warning, danger, background, card)
- Custom box shadows (card shadow)
- Custom border radius (ui)
- Custom animations (ticker, pulseDot)

### Path Aliases
The project uses Vite's `vite-tsconfig-paths` for convenient imports:
- `@/components/*` → `src/components/*`
- `@/hooks/*` → `src/hooks/*`
- `@/services/*` → `src/services/*`
- `@/types/*` → `src/types/*`
- `@/utils/*` → `src/utils/*`

## Development Notes

- **Component Organization**: Components are organized by feature/module for better maintainability
- **TypeScript**: Full type safety across the application
- **Responsive Design**: Mobile-first approach with Tailwind CSS breakpoints (md, lg)
- **Mock Data**: `dashboardService` provides mock data for development. Replace with API calls when backend is ready
- **Real-time Updates**: Dashboard KPI data and vehicle progress update every 30 seconds
- **Persistent Storage**: Parking status and vehicle assignments persist across page navigation

## Building & Deployment

### Production Build
```bash
npm run build
```
Creates optimized bundles in `dist/` folder.

### Preview Production Build
```bash
npm start
```
Starts a preview server on port 3000.

### Performance Note
The current build has a large chunk size (~1MB). Consider implementing code-splitting with dynamic imports to optimize bundle size for production.

## Browser Support

- Modern browsers supporting ES2020
- React 18+ compatible
- Chrome, Firefox, Safari, Edge (latest versions)

---

# Backend Documentation

## Backend Tech Stack

The backend consists of two independent Django applications:

- **TTMS (Truck Turnaround Time Monitoring System)**: REST API for vehicle turnaround time management
- **PTMS (Project Task Management System)**: REST API for project and task management

### Technology Stack
- **Framework**: Django 4.2 with Django REST Framework
- **Database**: PostgreSQL 15
- **Authentication**: JWT (JSON Web Tokens) with SimpleJWT
- **API**: RESTful API with custom permissions
- **Server**: Gunicorn with Nginx (production)
- **Containerization**: Docker & Docker Compose

## Backend Structure

```
backend/
├── core/                          # Django core configuration
│   ├── base_settings.py          # Common settings (both apps)
│   ├── settings_ttms.py          # TTMS-specific settings
│   ├── settings_ptms.py          # PTMS-specific settings
│   ├── urls_ttms.py              # TTMS URL configuration
│   ├── urls_ptms.py              # PTMS URL configuration
│   └── ...
├── ttms/                          # TTMS Application
│   ├── auth/                      # TTMS Authentication
│   │   ├── models.py             # Custom TTMSUser model
│   │   ├── serializers.py        # JWT token serializers
│   │   ├── backends.py           # Authentication backend
│   │   ├── permissions.py        # Role-based permissions
│   │   ├── views.py              # Auth endpoints
│   │   └── admin.py              # Django admin interface
│   ├── models.py                 # TTMS data models
│   ├── serializers.py            # Data serializers
│   ├── views.py                  # API viewsets
│   └── urls.py                   # TTMS app URLs
├── ptms/                          # PTMS Application
│   ├── auth/                      # PTMS Authentication
│   │   └── (similar structure)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── common/                        # Shared utilities
│   ├── utils.py                  # Helper functions
│   ├── pagination.py             # Pagination classes
│   ├── responses.py              # Response formatting
│   ├── validators.py             # Validation functions
│   └── constants.py              # Constants and enums
├── Docker/                        # Docker configuration
│   ├── Dockerfile.ttms           # TTMS container
│   ├── Dockerfile.ptms           # PTMS container
│   ├── docker-compose.yml        # Development environment
│   ├── docker-compose.prod.yml   # Production environment
│   ├── entrypoint.ttms.sh        # TTMS startup script
│   ├── entrypoint.ptms.sh        # PTMS startup script
│   └── init-databases.sh         # Database initialization
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── manage.py                     # Django management
```

## Getting Started with Backend

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- (Or Python 3.11+, PostgreSQL 15+ for local development)

### Docker Setup (Recommended)

```bash
cd backend

# 1. Copy environment file
cp .env.example .env

# 2. Start services
docker-compose -f Docker/docker-compose.yml up -d

# 3. Services are ready:
# TTMS: http://localhost:8000
# PTMS: http://localhost:8001
# TTMS DB: localhost:5432
# PTMS DB: localhost:5433
```

### Local Development Setup

```bash
cd backend

# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup TTMS database
export DJANGO_SETTINGS_MODULE=core.settings_ttms
python manage.py migrate
python manage.py createsuperuser

# 4. Run TTMS server
python manage.py runserver

# 5. In a new terminal, setup PTMS
export DJANGO_SETTINGS_MODULE=core.settings_ptms
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8001
```

## API Authentication

Both applications use JWT (JSON Web Tokens) for authentication.

### Login to TTMS

```bash
curl -X POST http://localhost:8000/api/ttms/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ttms.local","password":"admin123"}'

# Response:
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
# }
```

### Use Access Token

```bash
curl http://localhost:8000/api/ttms/auth/users/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Refresh Token

```bash
curl -X POST http://localhost:8000/api/ttms/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGc..."}'
```

## API Endpoints

### TTMS Endpoints

**Authentication:**
- `POST /api/ttms/auth/login/` - Get JWT tokens
- `POST /api/ttms/auth/refresh/` - Refresh access token
- `POST /api/ttms/auth/verify/` - Verify token
- `GET /api/ttms/auth/users/me/` - Get current user
- `POST /api/ttms/auth/users/me/update/` - Update profile
- `POST /api/ttms/auth/users/me/change-password/` - Change password

**Data:**
- `GET/POST /api/ttms/kpi/` - KPI metrics
- `GET/POST /api/ttms/vehicles/` - Vehicle management
- `GET/POST /api/ttms/vehicle-stages/` - Vehicle stages
- `GET/POST /api/ttms/parking-cells/` - Parking management
- `GET/POST /api/ttms/alerts/` - System alerts

### PTMS Endpoints

**Authentication:** (Same structure as TTMS, prefixed with `/api/ptms/auth/`)
**Data:**
- `GET/POST /api/ptms/projects/` - Project management
- `GET/POST /api/ptms/tasks/` - Task management

## Database

Both applications use PostgreSQL 15 with completely separate databases:

- **TTMS Database**: `ttms_db`
- **PTMS Database**: `ptms_db`

### Creating Backups

```bash
# TTMS
docker-compose exec ttms_postgres pg_dump -U postgres ttms_db > ttms_backup.sql

# PTMS
docker-compose exec ptms_postgres pg_dump -U postgres ptms_db > ptms_backup.sql
```

## Deployment

For detailed Docker and production deployment instructions, see [DOCKER_SETUP.md](backend/DOCKER_SETUP.md)

### Production Checklist

- [ ] Set `DEBUG=False` in environment
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up database backups
- [ ] Enable HTTPS/SSL
- [ ] Configure email backend
- [ ] Set up log monitoring
- [ ] Enable rate limiting
- [ ] Set strong database passwords

## Development Workflow

### Running Tests

```bash
# TTMS tests
docker-compose exec ttms python manage.py test --settings=core.settings_ttms

# PTMS tests
docker-compose exec ptms python manage.py test --settings=core.settings_ptms
```

### Creating Migrations

```bash
# TTMS
docker-compose exec ttms python manage.py makemigrations --settings=core.settings_ttms

# PTMS
docker-compose exec ptms python manage.py makemigrations --settings=core.settings_ptms
```

### Admin Interfaces

- **TTMS Admin**: http://localhost:8000/admin/
- **PTMS Admin**: http://localhost:8001/admin/

## Architecture Highlights

### Independent Applications
- TTMS and PTMS run in separate containers
- Each has its own PostgreSQL database
- Completely independent authentication systems
- Can be deployed separately

### Role-Based Access Control (RBAC)

**TTMS Roles:**
- Operator, Supervisor, Manager, Admin, Viewer

**PTMS Roles:**
- Team Member, Team Lead, Project Manager, Admin, Viewer

### Security Features
- Password hashing with Django's built-in system
- JWT token expiration and refresh
- Token blacklisting for logout
- CSRF protection
- SQL injection prevention
- Email-based authentication

## Performance Considerations

- Database query optimization with indexes
- Connection pooling for database
- Caching layer support (Redis-ready)
- Pagination for large datasets
- Efficient serialization

## Troubleshooting Backend

```bash
# View logs
docker-compose logs -f ttms
docker-compose logs -f ptms

# Access database shell
docker-compose exec ttms_postgres psql -U postgres -d ttms_db

# Restart services
docker-compose restart ttms ptms

# See detailed error messages
docker-compose logs --tail=50 ttms
```

## Support & Documentation

- [Backend API Reference](backend/API_REFERENCE.md)
- [Database Schema](backend/DATABASE_SCHEMA.md)
- [Docker Setup Guide](backend/DOCKER_SETUP.md)
- [Phase Implementation Summaries](backend/)

---

## License

Proprietary - Truck Turnaround Time Monitoring System
