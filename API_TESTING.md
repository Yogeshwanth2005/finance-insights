# API Testing Guide

## Quick API Testing

### Using Postman
1. Download & install [Postman](https://www.postman.com)
2. Create a new collection "Finance Insights"
3. Add requests from the examples below

### Using cURL (Command Line)

Make sure backend is running on `localhost:5000`

## Endpoint Testing

### 1. File Management Endpoints

#### Upload File
```bash
curl -X POST http://localhost:5000/api/files/upload \
  -F "file=@sample_payments.xlsx"
```

**Response:**
```json
{
  "success": true,
  "file_id": 1,
  "records_processed": 50,
  "message": "Successfully processed 50 records"
}
```

#### Preview File Before Upload
```bash
curl -X POST http://localhost:5000/api/files/preview \
  -F "file=@sample_payments.xlsx"
```

**Response:**
```json
{
  "columns": ["Customer", "Amount", "Due Date", "Payment Date"],
  "detected_mapping": {
    "customer": "Customer",
    "amount": "Amount",
    "due_date": "Due Date",
    "payment_date": "Payment Date"
  },
  "sample_rows": [...],
  "total_rows": 50
}
```

#### List All Uploaded Files
```bash
curl http://localhost:5000/api/files/list
```

**Response:**
```json
{
  "files": [
    {
      "id": 1,
      "filename": "sample_payments.xlsx",
      "upload_date": "2024-01-15T10:30:00",
      "record_count": 50,
      "status": "processed"
    }
  ]
}
```

#### Delete File
```bash
curl -X DELETE http://localhost:5000/api/files/1
```

---

### 2. Analysis Endpoints

#### Get Late Payments
```bash
curl http://localhost:5000/api/analysis/late-payments
```

**Response:**
```json
{
  "late_payments": [
    {
      "customer_name": "ABC Corp",
      "amount": 5000,
      "due_date": "2024-01-15T00:00:00",
      "payment_date": "2024-02-05T00:00:00",
      "days_late": 21,
      "status": "paid"
    },
    {
      "customer_name": "XYZ Ltd",
      "amount": 3000,
      "due_date": "2024-01-20T00:00:00",
      "payment_date": null,
      "days_late": 25,
      "status": "overdue"
    }
  ],
  "count": 2
}
```

#### Get Payment Trends (Last 6 Months)
```bash
curl "http://localhost:5000/api/analysis/trends?months=6"
```

**Response:**
```json
{
  "trends": [
    {
      "month": "2023-09",
      "total_due": 50000,
      "total_paid": 45000,
      "late_count": 3,
      "collection_rate": 90.0
    },
    {
      "month": "2023-10",
      "total_due": 55000,
      "total_paid": 52800,
      "late_count": 2,
      "collection_rate": 96.0
    }
  ]
}
```

#### Get Customer Behavior Analysis
```bash
curl http://localhost:5000/api/analysis/customer-behavior
```

**Response:**
```json
{
  "customers": [
    {
      "customer_id": 1,
      "customer_name": "ABC Corp",
      "total_transactions": 12,
      "late_payment_count": 3,
      "late_percentage": 25.0,
      "average_delay_days": 15,
      "total_amount": 60000,
      "risk_score": 25.0
    }
  ],
  "count": 10
}
```

#### Get Dashboard Summary
```bash
curl http://localhost:5000/api/analysis/summary
```

**Response:**
```json
{
  "total_invoices": 50,
  "total_amount": 175000,
  "paid_invoices": 45,
  "paid_amount": 162000,
  "overdue_invoices": 5,
  "overdue_amount": 13000,
  "pending_invoices": 0,
  "unique_customers": 10,
  "average_days_late": 18.5,
  "collection_rate": 92.57
}
```

#### Get Notifications & Insights
```bash
curl http://localhost:5000/api/analysis/notifications
```

**Response:**
```json
{
  "notifications": [
    {
      "type": "warning",
      "message": "⚠️ ABC Corp has 3 late payments",
      "severity": "high"
    },
    {
      "type": "alert",
      "message": "🚨 High-value overdue invoice from XYZ Ltd: $13,000.00",
      "severity": "critical"
    }
  ],
  "insights": [
    "💰 Revenue increased by 5.2% this month",
    "⚠️ Collection rate is 92.6% (target: 90%+)"
  ]
}
```

---

### 3. Dashboard Endpoints

#### Get All Dashboard Statistics
```bash
curl http://localhost:5000/api/dashboard/stats
```

**Response:**
```json
{
  "summary": {...},
  "trends": [...],
  "top_customers": [...],
  "high_risk_customers": [...],
  "all_customers": [...]
}
```

#### Export Report as JSON
```bash
curl http://localhost:5000/api/dashboard/export
```

**Response:**
```json
{
  "generated_at": "2024-01-15T10:30:00",
  "summary": {...},
  "trends": [...],
  "customer_behavior": [...],
  "late_payments": [...]
}
```

---

## Advanced Testing Scenarios

### Scenario 1: Full Workflow

```bash
# 1. Upload file
curl -X POST http://localhost:5000/api/files/upload \
  -F "file=@sample_payments.xlsx"

# 2. Get summary
curl http://localhost:5000/api/analysis/summary

# 3. Get late payments
curl http://localhost:5000/api/analysis/late-payments

# 4. Get trends
curl "http://localhost:5000/api/analysis/trends?months=12"

# 5. Get customer behavior
curl http://localhost:5000/api/analysis/customer-behavior

# 6. Get notifications
curl http://localhost:5000/api/analysis/notifications
```

### Scenario 2: Data with Different Statuses

Create Excel with:
```
Customer | Amount | Due Date   | Payment Date
---------|--------|------------|---------------
A        | 1000   | 2024-01-10 | 2024-01-15  (paid on time)
B        | 2000   | 2024-01-15 | 2024-02-05  (late payment)
C        | 3000   | 2024-02-01 |             (pending/future)
D        | 4000   | 2023-12-25 |             (overdue)
```

### Scenario 3: Multiple Files Upload

Upload different files to simulate:
- Monthly data updates
- Different departments
- Multiple time periods
- Trend analysis

---

## Testing with Postman (Step-by-Step)

### Setup Postman Collection

1. **Create Environment**
   - Click "Environments"
   - Create "Development"
   - Add variable: `base_url` = `http://localhost:5000`
   - Save

2. **Create Collection**
   - Click "Collections"
   - New Collection: "Finance Insights API"

3. **Add Requests**

#### Request 1: Upload File
- Method: `POST`
- URL: `{{base_url}}/api/files/upload`
- Body: Form-data
  - Key: `file` (type: File)
  - Value: Select your Excel file

#### Request 2: Get Summary
- Method: `GET`
- URL: `{{base_url}}/api/analysis/summary`
- Send

#### Request 3: Get Late Payments
- Method: `GET`
- URL: `{{base_url}}/api/analysis/late-payments`
- Send

#### Request 4: Get Trends
- Method: `GET`
- URL: `{{base_url}}/api/analysis/trends?months=6`
- Send

---

## Response Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET request successful |
| 201 | Created | File uploaded successfully |
| 400 | Bad Request | Invalid file format |
| 404 | Not Found | File ID doesn't exist |
| 500 | Server Error | Database error |

---

## Common Request/Response Patterns

### Multi-file Testing
```bash
# Upload multiple files in sequence
for file in *.xlsx; do
  echo "Uploading $file..."
  curl -X POST http://localhost:5000/api/files/upload -F "file=@$file"
done
```

### Export Data
```bash
# Export full report
curl http://localhost:5000/api/dashboard/export > report.json

# View report
cat report.json
```

### Filtering Trends
```bash
# Get last 3 months
curl "http://localhost:5000/api/analysis/trends?months=3"

# Get last 12 months
curl "http://localhost:5000/api/analysis/trends?months=12"
```

---

## Debugging Tips

### Enable Verbose Output in cURL
```bash
curl -v http://localhost:5000/api/analysis/summary
```

### Pretty Print JSON Response
```bash
# Linux/Mac
curl http://localhost:5000/api/analysis/summary | jq

# Windows PowerShell
curl http://localhost:5000/api/analysis/summary | ConvertFrom-Json | ConvertTo-Json
```

### Check Backend Logs
```bash
# Backend console will show:
INFO:werkzeug: POST /api/files/upload HTTP/1.1 200
ERROR:app: Failed to process file: ...
```

---

## Performance Testing

### Test with Large File
```bash
# Time the request
time curl -X POST http://localhost:5000/api/files/upload \
  -F "file=@large_payments.xlsx" \
  -o /dev/null -s -w "%{time_total}s\n"
```

### Test Trend Analysis with Many Data Points
```bash
curl "http://localhost:5000/api/analysis/trends?months=24"
```

---

## Success Indicators

✅ File upload returns success message  
✅ Summary shows correct totals  
✅ Late payments list shows overdue items  
✅ Trends show monthly progression  
✅ Customer risk scores calculated  
✅ Notifications generated for edge cases  

---

**Happy testing! 🧪**
