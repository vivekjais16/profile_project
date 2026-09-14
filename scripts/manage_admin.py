"""
Admin User Management CLI (Django-style CLI for FastAPI)
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import sys
import getpass
import argparse
from pathlib import Path

# Ensure root directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal, init_db
from app.models.admin import AdminUser, hash_password


def create_super_user(username: str = None, email: str = None, password: str = None):
    """Create a new admin user in the SQLite database (like Django createsuperuser)."""
    init_db()
    db = SessionLocal()
    try:
        if not username:
            username = input("Enter admin username: ").strip()
        if not username:
            print("❌ Error: Username cannot be empty.")
            return

        existing = db.query(AdminUser).filter(AdminUser.username == username).first()
        if existing:
            print(f"⚠️ User '{username}' already exists. Use 'changepassword' instead.")
            return

        if not email:
            email = input("Enter admin email (optional): ").strip()

        if not password:
            while True:
                p1 = getpass.getpass("Enter password: ")
                if not p1 or len(p1) < 4:
                    print("❌ Password must be at least 4 characters.")
                    continue
                p2 = getpass.getpass("Confirm password: ")
                if p1 != p2:
                    print("❌ Passwords do not match. Try again.")
                    continue
                password = p1
                break

        new_admin = AdminUser(
            username=username,
            password_hash=hash_password(password),
            email=email if email else None,
        )
        db.add(new_admin)
        db.commit()
        print(f"✅ Superuser '{username}' created successfully in SQLite database!")
    finally:
        db.close()


def change_password(username: str = None, new_password: str = None):
    """Change password for an existing admin user (like Django changepassword)."""
    init_db()
    db = SessionLocal()
    try:
        if not username:
            username = input("Enter username to change password: ").strip()

        user = db.query(AdminUser).filter(AdminUser.username == username).first()
        if not user:
            print(f"❌ Error: User '{username}' not found in database.")
            return

        if not new_password:
            while True:
                p1 = getpass.getpass(f"Enter new password for '{username}': ")
                if not p1 or len(p1) < 4:
                    print("❌ Password must be at least 4 characters.")
                    continue
                p2 = getpass.getpass("Confirm new password: ")
                if p1 != p2:
                    print("❌ Passwords do not match. Try again.")
                    continue
                new_password = p1
                break

        user.set_password(new_password)
        db.commit()
        print(f"✅ Password for '{username}' updated successfully in SQLite database!")
    finally:
        db.close()


def list_users():
    """List all registered admin users."""
    init_db()
    db = SessionLocal()
    try:
        users = db.query(AdminUser).all()
        if not users:
            print("ℹ️ No admin users found in database.")
            return

        print("\n========================================================")
        print("  👤 Registered Admin Users in SQLite")
        print("========================================================")
        for u in users:
            print(f"• ID: {u.id} | Username: {u.username} | Email: {u.email or 'N/A'} | Created: {u.created_at}")
        print("========================================================\n")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="FastAPI Admin CLI Management Tool (Django-style)")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # createsuperuser subcommand
    create_parser = subparsers.add_parser("createsuperuser", help="Create a new admin user")
    create_parser.add_argument("--username", help="Admin username")
    create_parser.add_argument("--email", help="Admin email")
    create_parser.add_argument("--password", help="Admin password")

    # changepassword subcommand
    change_parser = subparsers.add_parser("changepassword", help="Change password for an existing admin user")
    change_parser.add_argument("username", nargs="?", help="Username whose password to change")
    change_parser.add_argument("--password", help="New password (optional, prompted securely if omitted)")

    # listusers subcommand
    subparsers.add_parser("listusers", help="List all admin users in SQLite database")

    args = parser.parse_args()

    if args.command == "createsuperuser":
        create_super_user(args.username, args.email, args.password)
    elif args.command == "changepassword":
        change_password(args.username, args.password)
    elif args.command == "listusers":
        list_users()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
