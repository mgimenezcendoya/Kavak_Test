#!/bin/bash

# Kavak Performance App Launcher
# Quick launch script for the Streamlit application

echo "🚗 Kavak Performance App - Launcher"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found"
    echo "Please run this script from the kavak_performance_app directory"
    exit 1
fi

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed"
    exit 1
fi

# Check if Streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Launch the app
echo "🚀 Launching Kavak Performance App..."
echo ""
echo "The app will open automatically in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
