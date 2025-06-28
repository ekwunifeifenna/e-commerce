#!/bin/bash
# Setup script for Autonomous AI Agent with FREE Ollama

echo "🚀 Setting up Autonomous AI Agent with FREE Ollama"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "autonomous_agent_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv autonomous_agent_env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source autonomous_agent_env/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "🤖 Installing Ollama (FREE AI model server)..."
    curl -fsSL https://ollama.ai/install.sh | sh
else
    echo "✅ Ollama already installed"
fi

# Pull the Llama 3 model
echo "🧠 Downloading Llama 3 model (this may take a few minutes)..."
ollama pull llama3

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Start Ollama server: ollama serve"
echo "2. Run the agent API: python agent_api.py"
echo "3. Test the endpoints from your Express app"
echo ""
echo "🌐 API will be available at: http://localhost:5000"
echo ""
echo "💡 No OpenAI API key needed - completely FREE!"