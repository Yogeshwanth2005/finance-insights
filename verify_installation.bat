@echo off
REM Installation verification script for Windows

echo.
echo 🔍 Finance Insights Installation Verification
echo =============================================
echo.

REM Check Python
echo ✓ Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo   ✅ !PYTHON_VERSION!
) else (
    echo   ❌ Python not found
    exit /b 1
)

REM Check Node.js
echo ✓ Checking Node.js...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo   ✅ !NODE_VERSION!
) else (
    echo   ❌ Node.js not found
    exit /b 1
)

REM Check npm
echo ✓ Checking npm...
npm --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
    echo   ✅ npm !NPM_VERSION!
) else (
    echo   ❌ npm not found
    exit /b 1
)

REM Check backend structure
echo.
echo ✓ Checking backend structure...
if exist "backend\app" (
    echo   ✅ Backend app directory found
) else (
    echo   ❌ Backend app directory not found
)

if exist "backend\requirements.txt" (
    echo   ✅ requirements.txt found
) else (
    echo   ❌ requirements.txt not found
)

REM Check frontend structure
echo.
echo ✓ Checking frontend structure...
if exist "frontend\src" (
    echo   ✅ Frontend src directory found
) else (
    echo   ❌ Frontend src directory not found
)

if exist "frontend\package.json" (
    echo   ✅ package.json found
) else (
    echo   ❌ package.json not found
)

REM Summary
echo.
echo =============================================
echo ✅ Installation verification complete!
echo.
echo 📝 Next steps:
echo 1. Create .env files from .env.example
echo 2. Terminal 1: cd backend ^& venv\Scripts\activate ^& python run.py
echo 3. Terminal 2: cd frontend ^& npm start
echo 4. Open: http://localhost:3000
echo.
