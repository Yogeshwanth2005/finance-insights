@echo off
REM Setup script for Windows

echo.
echo 🚀 Finance Insights Setup
echo ==========================

REM Backend setup
echo.
echo 📦 Setting up backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo ✅ Backend dependencies installed

REM Generate sample data
echo.
echo 📊 Generating sample data...
python generate_sample_data.py

REM Frontend setup
echo.
echo 🎨 Setting up frontend...
cd ..\frontend
call npm install
echo ✅ Frontend dependencies installed

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Terminal 1 (Backend): cd backend ^& venv\Scripts\activate ^& python run.py
echo 2. Terminal 2 (Frontend): cd frontend ^& npm start
echo.
echo 🌐 Dashboard will open at http://localhost:3000
