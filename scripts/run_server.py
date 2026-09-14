"""
Local Development Server Runner
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import sys
from pathlib import Path
import uvicorn

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def run():
    print("=========================================================")
    print("🚀 Launching Vivek Jaiswal Portfolio Platform (FastAPI)")
    print("📍 URL: http://127.0.0.1:8000")
    print("📖 OpenAPI Specs: http://127.0.0.1:8000/docs")
    print("=========================================================")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
