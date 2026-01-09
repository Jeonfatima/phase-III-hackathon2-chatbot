#!/usr/bin/env python
"""
Database migration script to add missing hashed_password column to user table.
"""

import sqlite3
from typing import Optional

def add_missing_columns():
    # Connect to the database
    conn = sqlite3.connect('todoapp.db')
    cursor = conn.cursor()

    # Check if hashed_password column exists
    cursor.execute("PRAGMA table_info(user)")
    columns = [column[1] for column in cursor.fetchall()]

    print(f"Current columns in user table: {columns}")

    if 'hashed_password' not in columns:
        print("Adding hashed_password column to user table...")
        # Add the missing column
        cursor.execute("ALTER TABLE user ADD COLUMN hashed_password TEXT NOT NULL DEFAULT 'temp_default'")

        print("hashed_password column added successfully!")
    else:
        print("hashed_password column already exists.")

    # Check if username column exists (to maintain compatibility with existing data)
    if 'username' not in columns:
        print("Adding username column to user table for compatibility...")
        cursor.execute("ALTER TABLE user ADD COLUMN username TEXT UNIQUE")
        print("username column added successfully.")

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database migration completed successfully!")

if __name__ == "__main__":
    add_missing_columns()