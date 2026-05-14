#!/bin/bash
# Installation verification script

echo "🔍 Finance Insights Installation Verification"
echo "=============================================="
echo ""

# Check Python
echo "✓ Checking Python..."
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    echo "  ✅ $PYTHON_VERSION"
else
    echo "  ❌ Python not found"
    exit 1
fi

# Check pip
echo "✓ Checking pip..."
if command -v pip &> /dev/null; then
    echo "  ✅ pip found"
else
    echo "  ❌ pip not found"
    exit 1
fi

# Check Node.js
echo "✓ Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "  ✅ $NODE_VERSION"
else
    echo "  ❌ Node.js not found"
    exit 1
fi

# Check npm
echo "✓ Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "  ✅ npm $NPM_VERSION"
else
    echo "  ❌ npm not found"
    exit 1
fi

# Check backend dependencies
echo ""
echo "✓ Checking backend dependencies..."
if [ -d "backend/venv" ] || [ -d "backend/.venv" ]; then
    echo "  ✅ Virtual environment found"
    
    # Activate venv and check packages
    source backend/venv/bin/activate 2>/dev/null || source backend/.venv/bin/activate 2>/dev/null
    
    if python -c "import flask" 2>/dev/null; then
        echo "  ✅ Flask installed"
    else
        echo "  ⚠️  Flask not installed (run: pip install -r requirements.txt)"
    fi
else
    echo "  ⚠️  Virtual environment not found (run: python -m venv venv)"
fi

# Check frontend dependencies
echo ""
echo "✓ Checking frontend dependencies..."
if [ -d "frontend/node_modules" ]; then
    echo "  ✅ Node modules found"
    
    if grep -q '"react"' "frontend/package.json"; then
        echo "  ✅ React configured"
    else
        echo "  ❌ React not configured"
    fi
else
    echo "  ⚠️  Node modules not found (run: npm install in frontend)"
fi

# Check project structure
echo ""
echo "✓ Checking project structure..."
if [ -d "backend/app" ]; then
    echo "  ✅ Backend app directory found"
else
    echo "  ❌ Backend app directory not found"
fi

if [ -d "frontend/src" ]; then
    echo "  ✅ Frontend src directory found"
else
    echo "  ❌ Frontend src directory not found"
fi

# Summary
echo ""
echo "=============================================="
echo "✅ Installation verification complete!"
echo ""
echo "📝 Next steps:"
echo "1. Create .env files from .env.example"
echo "2. Run: cd backend && venv/bin/activate && python run.py"
echo "3. Run (new terminal): cd frontend && npm start"
echo "4. Open: http://localhost:3000"
