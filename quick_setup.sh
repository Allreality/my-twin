#!/bin/bash
set -e

echo "🚀 Setting up Digital Twin Virtual Environment..."

# Create venv
echo "Creating virtual environment..."
python3 -m venv venv

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create project structure
echo "Creating project structure..."
mkdir -p twin_project/{agents,memory,utils,tests,logs,data}

# Create .env template
cat > .env << 'ENVEOF'
# Digital Twin Configuration
CLAUDE_API_KEY=your_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=your_token
INFLUXDB_ORG=your_org
INFLUXDB_BUCKET=twin_memory
ENVEOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys: nano .env"
echo "2. Activate venv: source venv/bin/activate"
echo "3. Start building!"
