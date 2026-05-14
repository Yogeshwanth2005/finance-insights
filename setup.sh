#!/bin/bash
# Setup script for macOS/Linux

echo "🚀 Finance Insights Setup"
echo "=========================="

# Backend setup
echo -e "\n📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Backend dependencies installed"

# Generate sample data
echo -e "\n📊 Generating sample data..."
python generate_sample_data.py

# Frontend setup
echo -e "\n🎨 Setting up frontend..."
cd ../frontend
npm install
echo "✅ Frontend dependencies installed"

echo -e "\n✅ Setup complete!"
echo -e "\n📝 Next steps:"
echo "1. Terminal 1 (Backend): cd backend && source venv/bin/activate && python run.py"
echo "2. Terminal 2 (Frontend): cd frontend && npm start"
echo -e "\n🌐 Dashboard will open at http://localhost:3000"
