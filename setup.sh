#!/bin/bash

# MCP Project Setup Script
# This script automates the installation and setup process

echo "🚀 Starting MCP Project Setup..."
echo ""

# Step 1: Check Python version
echo "📌 Step 1: Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python is installed"
echo ""

# Step 2: Create virtual environment
echo "📌 Step 2: Creating virtual environment..."
if [ ! -d "MCp" ]; then
    python3 -m venv MCp
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Step 3: Activate virtual environment and install dependencies
echo "📌 Step 3: Installing dependencies..."
source MCp/bin/activate
pip install --upgrade pip
pip install mcp google-generativeai python-dotenv
echo "✅ Dependencies installed"
echo ""

# Step 4: Check if .env file exists
echo "📌 Step 4: Checking API key configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating template..."
    echo "GEMINI_API_KEY=your_api_key_here" > .env
    echo "📝 Please edit .env file and add your Gemini API key"
else
    echo "✅ .env file exists"
fi
echo ""

echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source MCp/bin/activate"
echo "2. Set your API key in .env or client.py"
echo "3. Run the client: python3 client.py"
echo ""
echo "For more information, see README.md"
