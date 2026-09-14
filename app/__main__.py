"""
FastAPI Module Execution Entrypoint (`python -m app`)
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import sys
import uvicorn
from app.cli import main as cli_main


def run_app():
    if len(sys.argv) > 1 and sys.argv[1] in ["admin", "db", "profile", "--help", "-h"]:
        cli_main()
    else:
        port = 8000
        if "--port" in sys.argv:
            idx = sys.argv.index("--port")
            if idx + 1 < len(sys.argv):
                port = int(sys.argv[idx + 1])
        print(f"🚀 Launching FastAPI Application on http://127.0.0.1:{port}")
        uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    run_app()
