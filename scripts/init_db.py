#!/usr/bin/env python3
"""
Script to initialize the SQLite database for the Medical Data Management System.
This creates all necessary tables based on the SQLAlchemy models.
"""

import os
import sys
import traceback

# Add parent directory to path to import utils module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from sqlalchemy import inspect

from utils.database import get_engine, init_database


def main() -> int:
    # Load environment variables from .env file
    load_dotenv()

    # Check if DATABASE_URL is set
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in environment variables")
        print("Please ensure .env file exists and contains DATABASE_URL")
        return 1

    print(f"📊 Database URL: {database_url}")
    print("🔧 Initializing database...")

    try:
        # Initialize the database (creates all tables)
        init_database()
        print("✅ Database initialized successfully!")

        # Verify the database was created
        engine = get_engine()
        print(f"✅ Database engine created: {engine.url}")

        # List the tables that were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"\n📋 Created {len(tables)} tables:")
        for table in tables:
            print(f"   • {table}")

        print("\n🎉 Database setup complete! You can now run the application.")
        return 0

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
