# Quick Start Guide - Finance Insights Dashboard

## 5-Minute Setup

### Step 1: Backend Setup
```bash
cd finance-insights/backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start server
python run.py
```
✅ Backend runs on `http://localhost:5000`

### Step 2: Frontend Setup (New Terminal)
```bash
cd finance-insights/frontend

# Install dependencies
npm install

# Start React app
npm start
```
✅ Frontend opens on `http://localhost:3000`

## Testing the Application

### Option 1: Create Sample Excel File

Create a file named `sample_payments.xlsx` with these columns:

```
Customer | Amount | Due Date   | Payment Date
---------|--------|------------|---------------
ABC Corp | 5000   | 2024-01-15 | 2024-01-20
XYZ Ltd  | 3000   | 2024-01-20 |
Tech Inc | 7500   | 2024-01-10 | 2024-02-05
```

Then:
1. Go to Dashboard → Upload tab
2. Select `sample_payments.xlsx`
3. Review column mapping
4. Click "Upload & Process"

### Option 2: Test API Directly

```bash
# Using curl or Postman
POST http://localhost:5000/api/files/upload
- Select Excel file
- Submit

GET http://localhost:5000/api/analysis/summary
GET http://localhost:5000/api/analysis/late-payments
GET http://localhost:5000/api/analysis/trends?months=12
```

## What You Can Do

### On the Dashboard
- 📊 View payment summaries and statistics
- 📈 See payment trends with interactive charts
- 👥 Analyze customer risk scores
- 🔔 Get notifications about late payments

### Late Payments Tab
- ⏰ View all overdue invoices
- 📋 See days late for each payment
- 👤 Find which customers pay late

### Upload Tab
- 📤 Upload Excel files
- 🔍 Auto-detect column mappings
- ✏️ Manually adjust if needed

## Sample Data Interpretation

After uploading data:

**Summary Section Shows:**
- Total Invoices: All records uploaded
- Collection Rate: % of invoices paid
- Avg Days Late: Average delay when overdue
- High-value Overdue: Large unpaid invoices

**Trends Chart Shows:**
- Monthly revenue received (green line)
- Monthly revenue due (blue line)
- How collection is tracking

**Risk Analysis Table:**
- Risk Score 0-100 (red=high, green=low)
- Customer payment history
- Late payment percentage

## Troubleshooting

### Backend won't start?
```bash
# Check Python version (need 3.8+)
python --version

# Try different port
# Edit backend/run.py, change port 5000 to 5001
```

### Frontend shows connection error?
- Make sure backend is running on localhost:5000
- Check browser console (F12) for errors
- Make sure CORS is enabled in backend

### Excel upload fails?
- Verify file is .xlsx or .xls format
- Check column names match expected names
- Ensure no empty rows at top of file
- Verify dates are in standard format (YYYY-MM-DD)

### Database errors?
```bash
# Reset database
rm finance_insights.db
python run.py
```

## File Structure Reference

```
TECHSPIRE/finance-insights/
├── backend/
│   ├── app/
│   ├── uploads/          ← Your Excel files go here
│   ├── requirements.txt
│   ├── run.py
│   └── finance_insights.db ← SQLite database
└── frontend/
    ├── public/
    ├── src/
    ├── package.json
    └── node_modules/     ← Created after npm install
```

## Next Steps

1. ✅ Run both backend and frontend
2. ✅ Upload sample Excel file
3. ✅ Explore Dashboard tab
4. ✅ Check Late Payments tab
5. ✅ Try uploading multiple files for trends
6. ✅ Monitor risk scores updating

## Common Commands

```bash
# Frontend
npm start          # Start dev server
npm build          # Build for production
npm test           # Run tests

# Backend
python run.py      # Start Flask server
pip install -r requirements.txt  # Install deps
python manage.py db upgrade      # If using migrations
```

## API Quick Reference

```
GET  /api/analysis/summary           → Dashboard stats
GET  /api/analysis/late-payments     → Overdue list
GET  /api/analysis/trends            → Monthly trends
GET  /api/analysis/customer-behavior → Customer analysis
POST /api/files/upload               → Upload Excel
GET  /api/files/list                 → Uploaded files
```

## Performance Tips

- Keep uploaded Excel files under 10,000 rows
- Archive old files after 6-12 months
- Run on machine with 4GB+ RAM for large datasets
- Use modern browser (Chrome, Firefox, Edge)

---

**Ready to analyze payments? 🚀 Start uploading!**
