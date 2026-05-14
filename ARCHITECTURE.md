# Architecture & Advanced Features Guide

## System Architecture

### Backend Architecture
```
┌─────────────────────────────────────────────────────────┐
│                   Flask REST API                         │
├─────────────────────────────────────────────────────────┤
│  Routes Layer (Flask Blueprints)                        │
│  - FileRoutes (Upload, Preview, List)                  │
│  - AnalysisRoutes (Payment Analysis)                   │
│  - DashboardRoutes (Statistics Export)                 │
├─────────────────────────────────────────────────────────┤
│  Services Layer (Business Logic)                       │
│  - ExcelProcessor (File Reading & Validation)          │
│  - AnalysisService (Data Analysis)                     │
│  - NotificationService (Insights Generation)           │
│  - FileService (File Management)                       │
├─────────────────────────────────────────────────────────┤
│  Models Layer (SQLAlchemy ORM)                         │
│  - Payment (Invoice Records)                           │
│  - Customer (Customer Master)                          │
│  - FileUpload (File Tracking)                          │
├─────────────────────────────────────────────────────────┤
│  Database Layer (SQLite)                               │
│  - finance_insights.db                                 │
└─────────────────────────────────────────────────────────┘
```

### Frontend Architecture
```
┌──────────────────────────────────────────────────────────┐
│              React Application (localhost:3000)           │
├──────────────────────────────────────────────────────────┤
│  App.js (Main Component)                                │
│  - Navigation between pages                             │
│  - Page routing logic                                   │
├──────────────────────────────────────────────────────────┤
│  Components                                             │
│  - Dashboard.js (Charts & Stats)                        │
│  - FileUpload.js (Excel Upload)                         │
│  - LatePayments.js (Late Payment List)                  │
│  - FileManagement.js (File History)                     │
├──────────────────────────────────────────────────────────┤
│  API Client (api.js - Axios)                            │
│  - fileAPI (Upload & Preview)                           │
│  - analysisAPI (Analysis Results)                       │
│  - dashboardAPI (Dashboard Stats)                       │
└──────────────────────────────────────────────────────────┘
```

## Advanced Features

### 1. Intelligent Column Detection

**How It Works:**
- Reads Excel column headers
- Matches against common naming patterns
- Returns detected mappings to user
- Allows manual override if needed

**Code Location:** `backend/app/services/excel_processor.py`

```python
COMMON_COLUMN_NAMES = {
    'customer': ['customer', 'customer_name', 'name', 'company'],
    'amount': ['amount', 'invoice_amount', 'total', 'value'],
    'due_date': ['due_date', 'due', 'payment_due'],
    ...
}
```

### 2. Risk Scoring Algorithm

**Formula:**
```
Risk Score = (Late Payment Count / Total Transactions) × 100
Range: 0-100 (0=no risk, 100=maximum risk)
```

**Implementation:**
- Calculates for each customer
- Updates on new payment data
- Used for sorting and alerting

**Code:** `backend/app/models/customer.py` - `calculate_risk_score()`

### 3. Payment Status Management

**Status Transitions:**
```
Initial State (from Excel)
    ↓
pending → (if due_date < today and no payment_date) → overdue
paid ← (if payment_date exists)
```

**Auto-Calculation:**
- Days late = payment_date - due_date (if positive)
- Status determined automatically
- Updated on each transaction

**Code:** `backend/app/services/analysis_service.py`

### 4. Trend Analysis Engine

**Monthly Aggregation:**
- Groups transactions by month
- Calculates:
  - Total due amount
  - Total paid amount
  - Number of late payments
  - Collection rate (paid/due × 100)

**Data Points:**
```python
{
    'month': '2024-01',
    'total_due': 50000,
    'total_paid': 45000,
    'late_count': 5,
    'collection_rate': 90.0
}
```

### 5. Notification System

**Smart Alerts Generated:**

1. **Frequent Late Payers**
   - Triggered when: late_payment_count > 2
   - Message: "⚠️ Customer X has N late payments"

2. **High-Value Overdue**
   - Triggered when: amount > average_amount AND overdue
   - Message: "🚨 High-value overdue invoice..."

3. **Revenue Drops**
   - Triggered when: current_month_paid < previous_month_paid by >5%
   - Message: "💰 Revenue decreased by X%"

4. **Collection Rate Warnings**
   - Triggered when: collection_rate < 80%
   - Message: "⚠️ Collection rate is X% (target: 90%+)"

**Code:** `backend/app/services/notification_service.py`

### 6. Dynamic Charts & Visualizations

**Using Recharts Library:**

1. **Line Chart** - Payment Trends
   - X-axis: Month
   - Y-axis: Amount
   - Lines: Total Due vs Total Paid

2. **Bar Chart** - Collection Rate
   - X-axis: Month
   - Y-axis: Collection Rate %

3. **Table** - Customer Risk Matrix
   - Color coded by risk level
   - Sortable columns
   - Interactive rows

## Database Schema

### Payments Table
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER FOREIGN KEY,
    amount FLOAT,
    due_date DATETIME,
    payment_date DATETIME,
    status VARCHAR(20),
    days_late INTEGER,
    file_upload_id INTEGER,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Customers Table
```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    email VARCHAR(255),
    phone VARCHAR(20),
    total_transactions INTEGER,
    late_payment_count INTEGER,
    total_amount FLOAT,
    risk_score FLOAT,
    created_at DATETIME,
    updated_at DATETIME
);
```

### File Uploads Table
```sql
CREATE TABLE file_uploads (
    id INTEGER PRIMARY KEY,
    filename VARCHAR(255),
    original_filename VARCHAR(255),
    file_path VARCHAR(255),
    upload_date DATETIME,
    record_count INTEGER,
    status VARCHAR(20),
    error_message TEXT,
    created_at DATETIME
);
```

## Data Processing Flow

### Upload Flow
```
1. User selects Excel file
   ↓
2. Frontend sends file to /api/files/preview
   ↓
3. Backend reads file & detects columns
   ↓
4. Frontend displays preview & column mapping
   ↓
5. User reviews and adjusts mapping (optional)
   ↓
6. User clicks "Upload & Process"
   ↓
7. Frontend sends file + mapping to /api/files/upload
   ↓
8. Backend:
   a. Reads Excel with mapping
   b. Validates data
   c. For each row:
      - Get/create Customer
      - Create Payment record
      - Calculate status & days_late
      - Update Customer stats & risk score
   d. Commits to database
   ↓
9. Returns success response
   ↓
10. Frontend refreshes dashboard
```

### Analysis Flow
```
1. Frontend loads Dashboard component
   ↓
2. Calls multiple analysis endpoints in parallel:
   - /api/analysis/summary
   - /api/analysis/trends
   - /api/analysis/customer-behavior
   - /api/analysis/notifications
   ↓
3. Backend queries database:
   - Aggregates payment data
   - Calculates statistics
   - Generates insights
   ↓
4. Returns data to frontend
   ↓
5. React renders charts & tables with Recharts
```

## Performance Optimizations

### Backend Optimizations
1. **Query Optimization**
   - Eager loading relationships (backref)
   - Indexed columns (customer_id, status, date fields)
   - Aggregate queries for summaries

2. **File Processing**
   - Streaming reads for large files
   - Batch inserts for multiple records
   - Transaction rollback on error

3. **Caching Strategy** (Future)
   - Cache dashboard summaries (5-minute TTL)
   - Cache trend data (1-hour TTL)
   - Invalidate on new uploads

### Frontend Optimizations
1. **Component Rendering**
   - React memoization for charts
   - Lazy loading of components
   - Efficient state management

2. **API Calls**
   - Parallel requests for independent data
   - Error handling with retry logic
   - Request debouncing for searches

## Security Considerations

### Current Implementation
- ✅ File upload validation (type & size)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ CORS enabled for development
- ✅ Input sanitization for file names

### Recommended Enhancements
- 🔒 User authentication & authorization
- 🔒 API rate limiting
- 🔒 HTTPS/TLS for production
- 🔒 Data encryption at rest
- 🔒 Audit logging for file access
- 🔒 Request signing for API calls

## Scaling Considerations

### Horizontal Scaling
- Stateless Flask API (can run multiple instances)
- Load balancer in front of API
- Separate database server
- Redis cache layer

### Vertical Scaling
- Increase server resources
- Database query optimization
- File processing optimization
- Memory management improvements

### For Large Datasets (100K+ records)
- Implement pagination in tables
- Add data export to CSV/Excel
- Archive old data to separate DB
- Implement background jobs (Celery)

## Monitoring & Logging

### Key Metrics to Monitor
- File upload success rate
- Average processing time
- API response times
- Database query performance
- Error rates by endpoint

### Logging Strategy
```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Processed {record_count} records")
logger.error(f"Failed to process file: {error}")
```

## Future Enhancement Ideas

1. **Machine Learning**
   - Predict late payments
   - Identify payment patterns
   - Automated dunning recommendations

2. **Integrations**
   - QuickBooks/Xero API
   - Email notifications
   - SMS reminders
   - Slack/Teams webhooks

3. **Advanced Analytics**
   - Cohort analysis
   - Seasonality detection
   - Customer segmentation
   - Predictive modeling

4. **UI Improvements**
   - Custom date range filtering
   - Export to PDF reports
   - Email report scheduling
   - Mobile app version

5. **Automation**
   - Automatic file processing
   - Scheduled imports from email
   - Bulk payment recording
   - Auto-reconciliation

---

**This architecture is designed for scalability, maintainability, and future growth.**
