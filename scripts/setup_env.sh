#!/usr/bin/env bash
# ==============================================================================
# Environment Setup and Dependency Bootstrap Script
# Author: Vivek Jaiswal <vivekjais16@gmail.com>
# Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
# ==============================================================================

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "================================================================="
echo "  🐍 Initializing Isolated Python Virtual Environment (venv)"
echo "================================================================="

if [ ! -d "venv" ]; then
    echo "Creating new virtual environment in ./venv ..."
    python3 -m venv venv
else
    echo "Existing ./venv detected."
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip & installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Initializing SQLite database with resume data..."
python scripts/seed_db.py

echo ""
echo "================================================================="
echo "✅ Environment ready! Activate it with:"
echo "   source venv/bin/activate"
echo "Launch server with:"
echo "   python scripts/run_server.py"
echo "================================================================="
