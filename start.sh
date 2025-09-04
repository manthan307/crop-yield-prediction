#!/bin/bash

# Exit immediately on any error
set -e

echo "========== Starting Environment Setup =========="

# 1️⃣ Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "No virtual environment found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

# 2️⃣ Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "========== Training Models =========="

# 3️⃣ Train Rain Model
echo "Training rain model..."
python models/prediction-of-rainfall.py

# 4️⃣ Train Crop Yield Model
echo "Training crop yield model..."
python models/prediction-of-yield.py

# 5️⃣ Train Fertilizer Model
echo "Training fertilizer model..."
python models/fertilizer-suggestion.py

echo "========== Starting Backend (FastAPI) =========="

# Start FastAPI in background
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

BACKEND_PID=$!
echo "Backend running with PID $BACKEND_PID"

echo "========== Starting Frontend (Next.js) =========="

# Navigate to frontend folder
cd frontend

# Install frontend dependencies if not installed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start Next.js in development mode
npm run dev

# Wait for backend process to exit when frontend stops
wait $BACKEND_PID
