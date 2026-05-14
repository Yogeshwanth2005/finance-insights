# File Index & Structure Guide

## 📑 Complete File Listing

### Root Directory Files

| File | Purpose |
|------|---------|
| `README.md` | 📖 Complete documentation (full API reference, features, setup) |
| `QUICKSTART.md` | 🚀 5-minute setup guide (fastest way to get started) |
| `PROJECT_SUMMARY.md` | 📋 Project overview (features, tech stack, roadmap) |
| `ARCHITECTURE.md` | 🏗️ Technical architecture (system design, algorithms) |
| `API_TESTING.md` | 🧪 API endpoint testing guide (cURL examples, Postman) |
| `FILE_INDEX.md` | 📑 This file - file structure guide |
| `setup.bat` | 💻 Windows automated setup script |
| `setup.sh` | 🐧 Linux/macOS automated setup script |
| `verify_installation.bat` | ✅ Windows verification script |
| `verify_installation.sh` | ✅ Linux/macOS verification script |
| `docker-compose.yml` | 🐳 Docker containerization config |
| `.gitignore` | 🚫 Git ignore patterns |

---

## Backend Directory Structure

### `backend/`

#### Root Backend Files

| File | Purpose |
|------|---------|
| `run.py` | 🚀 Flask app entry point |
| `requirements.txt` | 📦 Python dependencies |
| `Dockerfile` | 🐳 Docker image for backend |
| `.env.example` | ⚙️ Environment config template |
| `generate_sample_data.py` | 📊 Test data generator |

#### `backend/app/` - Main Application

| File | Purpose |
|------|---------|
| `__init__.py` | 🔧 Flask app initialization, config, DB setup |

#### `backend/app/models/` - Database Models

| File | Purpose | Key Classes |
|------|---------|-------------|
| `__init__.py` | Package init | - |
| `payment.py` | 💳 Payment records model | `Payment` |
| `customer.py` | 👤 Customer master data | `Customer` |
| `file_upload.py` | 📁 File upload tracking | `FileUpload` |

**Model Relationships:**
```
Customer (1) ─── (many) Payment
FileUpload (1) ─── (many) Payment
```

#### `backend/app/routes/` - API Endpoints

| File | Purpose | Endpoints |
|------|---------|-----------|
| `__init__.py` | Package init | - |
| `file_routes.py` | 📤 File upload endpoints | `/api/files/*` |
| `analysis_routes.py` | 📊 Analysis endpoints | `/api/analysis/*` |
| `dashboard_routes.py` | 📈 Dashboard endpoints | `/api/dashboard/*` |

**Available Endpoints:**
```
POST   /api/files/upload
GET    /api/files/list
POST   /api/files/preview
DELETE /api/files/<id>

GET /api/analysis/late-payments
GET /api/analysis/trends
GET /api/analysis/customer-behavior
GET /api/analysis/summary
GET /api/analysis/notifications

GET /api/dashboard/stats
GET /api/dashboard/export
```

#### `backend/app/services/` - Business Logic

| File | Purpose | Main Classes |
|------|---------|-------------|
| `__init__.py` | Package init | - |
| `excel_processor.py` | 📄 Excel file processing | `ExcelProcessor` |
| `analysis_service.py` | 🧮 Data analysis & calculations | `AnalysisService` |
| `notification_service.py` | 🔔 Alerts & insights | `NotificationService` |
| `file_service.py` | 📁 File management | `FileService` |

**Service Functions:**
```
ExcelProcessor:
  - detect_columns()
  - read_excel()
  - parse_date()
  - validate_and_process()

AnalysisService:
  - calculate_days_late()
  - determine_status()
  - get_late_payments()
  - get_payment_trends()
  - get_customer_behavior()
  - get_dashboard_summary()

NotificationService:
  - generate_notifications()
  - generate_summary_text()

FileService:
  - process_uploaded_file()
  - get_uploaded_files()
```

#### `backend/uploads/` Directory
- 📁 Uploaded Excel files stored here
- Auto-created on first upload
- Files organized by upload date

#### `backend/finance_insights.db`
- 🗄️ SQLite database
- Contains: payments, customers, file_uploads tables
- Auto-created on first run

---

## Frontend Directory Structure

### `frontend/`

#### Root Frontend Files

| File | Purpose |
|------|---------|
| `package.json` | 📦 Node.js dependencies & scripts |
| `Dockerfile` | 🐳 Docker image for frontend |
| `.env.example` | ⚙️ Environment config template |
| `.gitignore` | 🚫 Git ignore patterns |

#### `frontend/public/`

| File | Purpose |
|------|---------|
| `index.html` | 📄 HTML entry point |

#### `frontend/src/` - React Application

| File | Purpose |
|------|---------|
| `index.js` | 🚀 React app entry point |
| `index.css` | 🎨 Global styles |
| `App.js` | 📱 Main app component |
| `api.js` | 🔌 API client (Axios) |

#### `frontend/src/components/` - React Components

| File | Purpose | Exports |
|------|---------|---------|
| `FileUpload.js` | 📤 File upload form | `FileUpload` component |
| `FileUpload.css` | 🎨 File upload styles | - |
| `Dashboard.js` | 📊 Main dashboard | `Dashboard` component |
| `Dashboard.css` | 🎨 Dashboard styles | - |
| `LatePayments.js` | ⏰ Late payment list | `LatePayments` component |
| `LatePayments.css` | 🎨 Late payment styles | - |
| `FileManagement.js` | 📁 File history view | `FileManagement` component |
| `FileManagement.css` | 🎨 File history styles | - |

#### `frontend/node_modules/` Directory
- 📦 NPM dependencies (created after `npm install`)
- Excluded from Git

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────┐
│            User Browser (React)                 │
│  App.js → FileUpload.js / Dashboard.js          │
└────────────────┬────────────────────────────────┘
                 │
         API Calls (Axios)
                 │
┌────────────────▼────────────────────────────────┐
│        Flask REST API (Backend)                 │
│  ┌──────────────────────────────────────────┐  │
│  │  Routes (Flask Blueprints)               │  │
│  │  - file_routes.py                        │  │
│  │  - analysis_routes.py                    │  │
│  │  - dashboard_routes.py                   │  │
│  └───────────┬──────────────────────────────┘  │
│              │                                  │
│  ┌───────────▼──────────────────────────────┐  │
│  │  Services (Business Logic)               │  │
│  │  - excel_processor.py                    │  │
│  │  - analysis_service.py                   │  │
│  │  - notification_service.py               │  │
│  │  - file_service.py                       │  │
│  └───────────┬──────────────────────────────┘  │
│              │                                  │
│  ┌───────────▼──────────────────────────────┐  │
│  │  Models (SQLAlchemy ORM)                 │  │
│  │  - payment.py                            │  │
│  │  - customer.py                           │  │
│  │  - file_upload.py                        │  │
│  └───────────┬──────────────────────────────┘  │
└────────────────┬────────────────────────────────┘
                 │
         SQL Queries
                 │
┌────────────────▼────────────────────────────────┐
│        SQLite Database                          │
│  - payments table                               │
│  - customers table                              │
│  - file_uploads table                           │
└─────────────────────────────────────────────────┘
```

---

## Configuration Files Reference

### Backend Configuration

**`backend/.env.example`** → Copy to `.env`
```
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///finance_insights.db
MAX_UPLOAD_SIZE=16777216
PORT=5000
```

**`backend/requirements.txt`**
```
Flask==2.3.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.3
pandas==2.0.0
openpyxl==3.10.5
...
```

### Frontend Configuration

**`frontend/.env.example`** → Copy to `.env`
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

**`frontend/package.json`**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "axios": "^1.3.0",
    "recharts": "^2.10.3"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}
```

---

## File Size Reference

Typical file sizes:
- Backend files: 5-15 KB each
- Frontend components: 3-10 KB each
- CSS files: 2-5 KB each
- Total project: ~200 KB (without node_modules/venv)

---

## Reading Order Guide

### For Quick Start:
1. ✅ `QUICKSTART.md` - Get running in 5 minutes
2. ✅ Upload sample data
3. ✅ Explore dashboard

### For Understanding the System:
1. 📖 `README.md` - Overview of features
2. 🏗️ `ARCHITECTURE.md` - System design
3. 🧪 `API_TESTING.md` - How API works

### For Development:
1. 🔧 `QUICKSTART.md` - Setup
2. 📁 This file (`FILE_INDEX.md`) - Understand structure
3. 🏗️ `ARCHITECTURE.md` - Dive into code
4. 📖 `README.md` - Reference documentation

### For API Integration:
1. 🧪 `API_TESTING.md` - All endpoints explained
2. 🌐 Test with cURL or Postman
3. 📊 `backend/app/routes/*.py` - Review endpoint code

---

## Key Directories

```
finance-insights/
├── 📖 Documentation (*.md files)
├── 🐳 Docker files
├── ⚙️ Configuration (.env.example)
├── 📦 Backend code & database
│   └── app/ → Models, Routes, Services
├── 🎨 Frontend code
│   └── src/ → React components, API client
└── 📁 Runtime directories (created)
    ├── backend/venv/ (Python environment)
    ├── backend/uploads/ (Excel files)
    ├── backend/finance_insights.db (Database)
    └── frontend/node_modules/ (NPM packages)
```

---

## Important Files to Know

### Must Read Before Coding:
- ✅ `README.md` - Complete documentation
- ✅ `ARCHITECTURE.md` - System design
- ✅ `backend/app/__init__.py` - DB setup

### Must Edit for Custom Setup:
- ⚙️ `backend/.env` - Backend config
- ⚙️ `frontend/.env` - Frontend config
- 🔧 `backend/run.py` - Backend entry point

### Must Review for API Integration:
- 🧪 `API_TESTING.md` - All endpoints
- 🌐 `frontend/src/api.js` - API client code
- 📄 `backend/app/routes/` - Endpoint handlers

### Sample Data:
- 📊 `backend/generate_sample_data.py` - Create test data
- 📝 Run this first to populate database

---

## File Organization Logic

**Backend Organization:**
- `models/` - What data looks like
- `services/` - How to process data
- `routes/` - API endpoints that use services
- `run.py` - Start here

**Frontend Organization:**
- `components/` - What user sees
- `api.js` - How to talk to backend
- `App.js` - Navigation and layout
- `index.js` - Start here

**Documentation Organization:**
- Quick Reference → QUICKSTART.md
- Complete Reference → README.md
- Technical Deep Dive → ARCHITECTURE.md
- API Examples → API_TESTING.md
- This Guide → FILE_INDEX.md

---

## Next Steps

1. ✅ Read `QUICKSTART.md` to get started
2. ✅ Understand this file structure
3. ✅ Run `setup.bat` or `setup.sh`
4. ✅ Upload sample data
5. ✅ Review `API_TESTING.md` for endpoints
6. ✅ Read `ARCHITECTURE.md` for deep dive

---

**Happy exploring! 🚀**
