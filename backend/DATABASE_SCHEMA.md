# Database Schema Documentation

## Overview

The TTR Dashboard database uses PostgreSQL with the following key entities:

```
┌─────────────────────┐
│   KPIMetrics        │
├─────────────────────┤
│ • Capacity metrics  │
│ • Turnaround time   │
│ • Vehicle stats     │
│ • Dispatch data     │
└─────────────────────┘

┌─────────────────────────────────────────┐
│   Vehicle                               │
├───────────────────────────────────���─────┤
│ • Registration No. (PK)                 │
│ • RFID No.                              │
│ • Weight data (tare, after loading)     │
│ • Progress & turnaround time            │
└──────────────┬──────────────────────────┘
               │
               ├──→ VehicleStage (FK)
               │    • gateEntry
               │    • tareWeighing
               │    • loading
               │    • postLoadingWeighing
               │    • gateExit
               │
               ├──→ VehicleEntry (FK)
               │    • gate_entry_time
               │    • area
               │    • position
               │    • loading_gate
               │
               ├──→ SystemAlert (FK)
               │    • level
               │    • message
               │    • resolution status
               │
               └──→ ParkingCell (FK)
                    • area
                    • label
                    • status

┌──────────────────────┐
│ TurnaroundTimeSparkline │
├───────────────────��──┤
│ • timestamp          │
│ • value (minutes)    │
└──────────────────────┘
```

## Table Definitions

### 1. KPIMetrics

Stores key performance indicator data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PK | Primary key |
| created_at | DateTimeField | | Creation timestamp |
| updated_at | DateTimeField | | Last update timestamp |
| capacity_utilization | IntegerField | 0-100 | Capacity utilization % |
| plant_capacity | IntegerField | | Total plant capacity |
| trucks_inside | IntegerField | | Trucks currently inside |
| capacity_trend_direction | CharField | up/down | Capacity trend |
| capacity_trend_percentage | FloatField | | Capacity trend % |
| turnaround_avg_day | IntegerField | | Avg turnaround today (min) |
| turnaround_avg_cum | IntegerField | | Cumulative avg turnaround (min) |
| turnaround_last_year | IntegerField | | Last year turnaround (min) |
| turnaround_trend_direction | CharField | up/down | Trend direction |
| turnaround_trend_percentage | FloatField | | Trend percentage |
| turnaround_performance_color | CharField | green/yellow/red/blue | Performance color |
| vehicles_in_day | IntegerField | | Vehicles in today |
| vehicles_out_day | IntegerField | | Vehicles out today |
| vehicles_in_cum | IntegerField | | Cumulative vehicles in |
| vehicles_out_cum | IntegerField | | Cumulative vehicles out |
| vehicles_trend_direction | CharField | up/down | Trend |
| vehicles_trend_percentage | FloatField | | Trend % |
| vehicles_target | IntegerField | | Vehicle target |
| dispatch_today | IntegerField | | Dispatch today |
| dispatch_cum_month | IntegerField | | Cumulative dispatch this month |
| dispatch_target_day | IntegerField | | Daily dispatch target |
| dispatch_trend_direction | CharField | up/down | Trend |
| dispatch_trend_percentage | FloatField | | Trend % |

**Indexes:**
- id (PK)
- updated_at (for ordering)

---

### 2. Vehicle

Represents a vehicle in the system.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PK | Primary key |
| reg_no | CharField(50) | UNIQUE | Registration number |
| rfid_no | CharField(100) | UNIQUE, NULL | RFID number |
| created_at | DateTimeField | | Creation timestamp |
| updated_at | DateTimeField | | Last update timestamp |
| tare_weight | IntegerField | | Tare weight (kg) |
| weight_after_loading | IntegerField | | Weight after loading (kg) |
| progress | IntegerField | 0-100 | Progress percentage |
| turnaround_time | IntegerField | | Turnaround time (min) |
| timestamp | DateTimeField | | Last update timestamp |

**Indexes:**
- id (PK)
- reg_no (UNIQUE)
- rfid_no (UNIQUE)
- timestamp (for ordering)

**Constraints:**
- progress: 0-100 (validators)

---

### 3. VehicleStage

Tracks processing stages for each vehicle.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PK | Primary key |
| vehicle_id | BigAutoField | FK → Vehicle | Vehicle reference |
| stage | CharField(50) | | Stage name |
| state | CharField(20) | | Stage state (pending/active/completed) |
| wait_time | IntegerField | | Wait time (min) |
| standard_time | IntegerField | | Standard time (min) |
| created_at | DateTimeField | | Creation timestamp |
| updated_at | DateTimeField | | Last update timestamp |

**Indexes:**
- id (PK)
- vehicle_id (FK)
- (vehicle_id, stage) (UNIQUE)

**Valid Stages:**
- gateEntry
- tareWeighing
- loading
- postLoadingWeighing
- gateExit

**Valid States:**
- pending
- active
- completed

---

### 4. ParkingCell

Represents parking spaces/slots.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PK | Primary key |
| area | CharField(10) | | Parking area (AREA-1, AREA-2) |
| label | CharField(50) | | Slot label (e.g., S1, S2) |
| status | CharField(20) | | Status (available/occupied/reserved) |
| vehicle_id | BigAutoField | FK → Vehicle, NULL | Assigned vehicle |
| created_at | DateTimeField | | Creation timestamp |
| updated_at | DateTimeField | | Last update timestamp |

**Indexes:**
- id (PK)
- vehicle_id (FK)
- (area, label) (UNIQUE)
- area (for filtering)
- status (for filtering)

**Valid Areas:**
- AREA-1
- AREA-2

**Valid Statuses:**
- available
- occupied
- reserved

---

### 5. VehicleEntry

Records vehicle entries in the scheduling system.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PK | Primary key |
| vehicle_id | BigAutoField | FK → Vehicle | Vehicle reference |
| gate_entry_time | DateTimeField | | When vehicle entered |
| area | CharField(20) | | Parking area |
| position | CharField(200) | | Parking position(s) |
| loading_gate | CharField(50) | | Loading gate assigned |
| created_at | DateTimeField | | Creation timestamp |
| updated_at | DateTimeField | | Last update timestamp |

**Indexes:**
- id (PK)
- vehicle_id (FK)
- gate_entry_time (for ordering)

---

### 6. SystemAlert

Stores system alerts and notifications.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PK | Primary key |
| level | CharField(20) | | Alert level (critical/warning/info/success) |
| message | TextField | | Alert message |
| vehicle_id | BigAutoField | FK → Vehicle, NULL | Related vehicle |
| is_resolved | BooleanField | | Resolution status |
| created_at | DateTimeField | | Creation timestamp |
| resolved_at | DateTimeField | NULL | Resolution timestamp |

**Indexes:**
- id (PK)
- vehicle_id (FK)
- created_at (for ordering)
- is_resolved (for filtering)

**Valid Levels:**
- critical
- warning
- info
- success

---

### 7. TurnaroundTimeSparkline

Historical turnaround time data for charts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PK | Primary key |
| timestamp | DateTimeField | | Data point timestamp |
| value | IntegerField | | Turnaround time (min) |

**Indexes:**
- id (PK)
- timestamp (for ordering)

---

## Relationships

### One-to-Many Relationships

1. **Vehicle → VehicleStage** (1:many)
   - One vehicle has multiple processing stages
   - Delete cascade: If vehicle deleted, stages deleted

2. **Vehicle → VehicleEntry** (1:many)
   - One vehicle can have multiple entries
   - Delete cascade: If vehicle deleted, entries deleted

3. **Vehicle → SystemAlert** (1:many)
   - One vehicle can have multiple alerts
   - Null allowed: Alert can exist without vehicle

4. **Vehicle → ParkingCell** (1:many)
   - One vehicle can be assigned to one cell at a time
   - Null allowed: Cell can be empty

---

## Migration Strategy

### Initial Setup
1. Run `python manage.py makemigrations` to create migration files
2. Run `python manage.py migrate` to apply migrations to database

### Adding New Fields
1. Modify models.py
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`

### Data Preservation
- All migrations preserve existing data
- Default values provided for new non-nullable fields
- Backward compatible changes recommended

---

## Indexing Strategy

### Primary Indexes (Automatic)
- All primary keys indexed
- Foreign keys indexed automatically

### Secondary Indexes (For Performance)
- `Vehicle.timestamp`: Quick ordering by timestamp
- `Vehicle.reg_no`: Search by registration
- `ParkingCell.area`: Filter by area
- `SystemAlert.created_at`: Timeline queries
- `TurnaroundTimeSparkline.timestamp`: Chart data queries

---

## Query Examples

### Find all vehicles in a specific area
```sql
SELECT v.* FROM api_vehicle v
JOIN api_parkingcell pc ON v.id = pc.vehicle_id
WHERE pc.area = 'AREA-1';
```

### Get vehicles with active stages
```sql
SELECT DISTINCT v.* FROM api_vehicle v
JOIN api_vehiclestage vs ON v.id = vs.vehicle_id
WHERE vs.state IN ('active', 'pending')
ORDER BY v.timestamp DESC;
```

### Get recent alerts
```sql
SELECT * FROM api_systemalert
WHERE is_resolved = false
ORDER BY created_at DESC
LIMIT 10;
```

### Calculate average turnaround time
```sql
SELECT AVG(turnaround_time) FROM api_vehicle
WHERE timestamp > NOW() - INTERVAL '1 day';
```

### Get parking occupancy
```sql
SELECT area, status, COUNT(*) as count
FROM api_parkingcell
GROUP BY area, status;
```

---

## Performance Considerations

### Query Optimization
1. Use `select_related()` for foreign keys
2. Use `prefetch_related()` for reverse relations
3. Limit fields retrieved with `.values()` or `.values_list()`

### Database Optimization
1. Regular `VACUUM ANALYZE` on PostgreSQL
2. Index columns frequently used in WHERE/ORDER BY
3. Partition large tables if needed

### Caching Strategy
- Cache KPI data (updates every 30 seconds)
- Cache parking grid (updates as needed)
- Invalidate on data changes

---

## Backup Strategy

### Daily Backups
```bash
pg_dump ttr_dashboard > backup_$(date +%Y%m%d).sql
```

### Restore from Backup
```bash
psql ttr_dashboard < backup_20240115.sql
```

### Automated Backups (Recommended)
Set up cron job or database-specific backup tools

---

## Security Considerations

1. **Access Control**: Use Django permissions
2. **Data Validation**: Use Django validators
3. **SQL Injection**: Use ORM (protected by default)
4. **Encryption**: Consider encrypting sensitive fields
5. **Audit Trail**: Add created_by, updated_by fields if needed

---

## Future Enhancements

1. **Partitioning**: Partition large tables by date
2. **Read Replicas**: Set up read replicas for scaling
3. **Time Series DB**: Consider InfluxDB for metrics
4. **Archive Tables**: Archive old data periodically
5. **Full Text Search**: Add search capabilities
