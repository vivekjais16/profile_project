#!/usr/bin/env python
"""
Vivek Jaiswal Portfolio Platform — Management Utility
Django-style CLI management tool for FastAPI applications.
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import sys
import os
import uvicorn
from pathlib import Path

# Ensure root directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from scripts.manage_admin import create_super_user, change_password, list_users
from scripts.seed_db import main as seed_main


def print_help():
    print("""
========================================================================
🚀 Vivek Jaiswal Portfolio — CLI Management Utility (FastAPI / SQLite)
========================================================================

Usage:
  python manage.py <command> [options]

Available Commands:
  createsuperuser       Create a new admin superuser interactively
  changepassword [user] Change password for an admin user
  listusers             List all admin users in SQLite database
  seed [--force]        Seed SQLite database with resume data
  runserver [--port N]  Start development uvicorn web server
  test                  Run automated Pytest test suite

Examples:
  python manage.py createsuperuser
  python manage.py changepassword vivekjais16
  python manage.py runserver --port 8000
  python manage.py seed --force
========================================================================
""")


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "createsuperuser":
        username = sys.argv[2] if len(sys.argv) > 2 else None
        create_super_user(username=username)

    elif cmd == "changepassword":
        username = sys.argv[2] if len(sys.argv) > 2 else None
        change_password(username=username)

    elif cmd == "listusers":
        list_users()

    elif cmd == "seed":
        force = "--force" in sys.argv
        sys.argv = [sys.argv[0]] + (["--force"] if force else [])
        seed_main()

    elif cmd == "runserver":
        port = 8000
        if "--port" in sys.argv:
            idx = sys.argv.index("--port")
            if idx + 1 < len(sys.argv):
                port = int(sys.argv[idx + 1])
        print(f"🚀 Starting development server on http://127.0.0.1:{port} ...")
        uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

    elif cmd == "test":
        import pytest
        sys.exit(pytest.main(["tests/", "-v"]))

    else:
        print(f"❌ Unknown command: '{cmd}'")
        print_help()


if __name__ == "__main__":
    main()
