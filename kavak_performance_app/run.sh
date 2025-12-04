#!/bin/bash
# Script to run the Kavak Performance App

echo "🚗 Iniciando Kavak Performance App..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  No se encontró el entorno virtual. Creando..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
fi

# Activate virtual environment
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Instalando dependencias..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Todo listo!"
echo "🌐 Abriendo aplicación en el navegador..."
echo ""

# Run streamlit
streamlit run app.py
