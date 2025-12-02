#!/usr/bin/env python3
"""
Simple script to test database connection and verify tables are created.
Run this before starting the main application to ensure database is properly configured.
"""

from dependencies.database import engine, Base
from dependencies.config import conf
from models import orders, order_details, recipes, sandwiches, resources
from models import user, payment, review, promo
from sqlalchemy import inspect

def test_connection():
    """Test if we can connect to the database."""
    try:
        with engine.connect() as conn:
            print("✓ Successfully connected to database!")
            print(f"  Database: {conf.db_name}")
            print(f"  Host: {conf.db_host}:{conf.db_port}")
            print(f"  User: {conf.db_user}")
            if conf.db_host != "localhost":
                print(f"  ⚠ Connecting to REMOTE database at {conf.db_host}")
            return True
    except Exception as e:
        error_msg = str(e).lower()
        print(f"✗ Failed to connect to database: {e}")
        print("\nTroubleshooting:")
        
        if conf.db_host != "localhost":
            print("  REMOTE DATABASE CONNECTION:")
            print("  1. Verify remote MySQL server is running")
            print("  2. Check remote MySQL bind-address (should be 0.0.0.0 or your IP)")
            print("  3. Verify firewall allows port 3306 on remote PC")
            print("  4. Check if user has permission to connect from your IP")
            print("  5. Test network connectivity: ping", conf.db_host)
        else:
            print("  LOCAL DATABASE CONNECTION:")
            print("  1. MySQL server is running")
            print("  2. Database exists (CREATE DATABASE sandwich_maker_api;)")
        
        print("  3. Username and password in api/dependencies/config.py are correct")
        
        if "access denied" in error_msg or "password" in error_msg:
            print("\n  → Check username and password")
        elif "can't connect" in error_msg or "refused" in error_msg:
            print("\n  → Check if MySQL server is running and accessible")
            if conf.db_host != "localhost":
                print("  → For remote: check bind-address and firewall settings")
        elif "unknown database" in error_msg:
            print("\n  → Database does not exist. Create it first.")
        
        return False

def create_tables():
    """Create all database tables."""
    try:
        Base.metadata.create_all(engine)
        print("✓ Database tables created/verified successfully!")
        return True
    except Exception as e:
        print(f"✗ Failed to create tables: {e}")
        return False

def list_tables():
    """List all tables in the database."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if tables:
            print(f"\n✓ Found {len(tables)} table(s):")
            for table in sorted(tables):
                print(f"  - {table}")
        else:
            print("\n⚠ No tables found in database")
        return tables
    except Exception as e:
        print(f"✗ Failed to list tables: {e}")
        return []

if __name__ == "__main__":
    print("=" * 50)
    print("Database Connection Test")
    print("=" * 50)
    print()
    
    if test_connection():
        print()
        if create_tables():
            print()
            list_tables()
            print()
            print("=" * 50)
            print("✓ Database setup complete! You can now start the API server.")
            print("=" * 50)
        else:
            print()
            print("=" * 50)
            print("✗ Database setup failed. Please check the errors above.")
            print("=" * 50)
    else:
        print()
        print("=" * 50)
        print("✗ Cannot proceed without database connection.")
        print("=" * 50)

