"""
FastAPI Native CLI Controller
Standard FastAPI / Python CLI interface for database, credentials, and profile management.
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import sys
import argparse
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal, init_db
from app.models.admin import AdminUser, hash_password
from app.models.profile import Profile
from app.services.seeder_service import seed_portfolio_data
from app.core.config import settings


def set_admin_credentials(username: str, password: str, email: str = None):
    """Native FastAPI command to set or update admin credentials."""
    init_db()
    db = SessionLocal()
    try:
        user = db.query(AdminUser).filter(AdminUser.username == username).first()
        if user:
            user.set_password(password)
            if email:
                user.email = email
            db.commit()
            print(f"✓ Admin user '{username}' password updated successfully in SQLite database.")
        else:
            new_user = AdminUser(
                username=username,
                password_hash=hash_password(password),
                email=email if email else settings.AUTHOR_EMAIL,
            )
            db.add(new_user)
            db.commit()
            print(f"✓ New admin user '{username}' created successfully in SQLite database.")
    finally:
        db.close()


def update_profile_field(field: str, value: str):
    """Native FastAPI command to update a specific profile field in SQLite."""
    init_db()
    db = SessionLocal()
    try:
        profile = db.query(Profile).first()
        if not profile:
            print("❌ Profile not found. Run database seeder first.")
            return

        if hasattr(profile, field):
            setattr(profile, field, value)
            db.commit()
            print(f"✓ Profile field '{field}' updated to: '{value}'")
        else:
            print(f"❌ Invalid profile field: '{field}'")
    finally:
        db.close()


def seed_database(force: bool = False):
    """Seed or reset the SQLite database."""
    init_db()
    db = SessionLocal()
    try:
        seed_portfolio_data(db, force=force)
        print(f"✓ Database seeded successfully (force={force}).")
    finally:
        db.close()


def list_admin_users():
    """List all registered admin users."""
    init_db()
    db = SessionLocal()
    try:
        users = db.query(AdminUser).all()
        print(f"Found {len(users)} admin user(s):")
        for u in users:
            print(f"  • Username: {u.username} | Email: {u.email} | Updated: {u.updated_at}")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        prog="python -m app",
        description="FastAPI Native CLI for Database & Credentials Management",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="FastAPI subcommands")

    # admin command
    admin_parser = subparsers.add_parser("admin", help="Manage admin credentials")
    admin_parser.add_argument("--set-user", metavar="USERNAME", help="Admin username")
    admin_parser.add_argument("--password", metavar="PASSWORD", help="Admin password")
    admin_parser.add_argument("--email", metavar="EMAIL", help="Admin email")
    admin_parser.add_argument("--list", action="store_true", help="List all admin accounts")

    # profile command
    profile_parser = subparsers.add_parser("profile", help="Manage profile fields in DB")
    profile_parser.add_argument("--set", nargs=2, metavar=("FIELD", "VALUE"), help="Update profile field (e.g. headline 'New Headline')")

    # db command
    db_parser = subparsers.add_parser("db", help="Database operations")
    db_parser.add_argument("--seed", action="store_true", help="Seed database with resume data")
    db_parser.add_argument("--force", action="store_true", help="Force overwrite existing data")

    args = parser.parse_args()

    if args.subcommand == "admin":
        if args.set_user and args.password:
            set_admin_credentials(args.set_user, args.password, args.email)
        elif args.list:
            list_admin_users()
        else:
            admin_parser.print_help()

    elif args.subcommand == "profile":
        if args.set:
            update_profile_field(args.set[0], args.set[1])
        else:
            profile_parser.print_help()

    elif args.subcommand == "db":
        if args.seed:
            seed_database(force=args.force)
        else:
            db_parser.print_help()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
