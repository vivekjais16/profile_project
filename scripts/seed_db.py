"""
CLI Database Seeder Script
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import sys
import argparse
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import init_db, SessionLocal
from app.services.seeder_service import seed_portfolio_data


def main():
    parser = argparse.ArgumentParser(description="Seed Vivek Jaiswal Portfolio Database")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing data")
    args = parser.parse_args()

    print("Initializing SQLite database schemas...")
    init_db()

    db = SessionLocal()
    try:
        print(f"Seeding portfolio data (force={args.force})...")
        seed_portfolio_data(db, force=args.force)
        print("✓ Database successfully seeded with Vivek Jaiswal's full profile & resume data!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
