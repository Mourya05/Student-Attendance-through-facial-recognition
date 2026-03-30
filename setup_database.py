"""
Database setup utility for initializing MySQL database
Run this script once before running the main application
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def setup_database():
    """Create the database if it doesn't exist"""
    try:
        print("[DATABASE SETUP] Connecting to MySQL server...")

        # Connect without specifying database
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )

        cursor = connection.cursor()
        print("[DATABASE SETUP] Connected successfully")

        # Create database
        database_name = DB_CONFIG['database']
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
        cursor.execute(create_db_query)
        print(f"[DATABASE SETUP] Database '{database_name}' created/verified")

        cursor.close()
        connection.close()

        # Now connect to the specific database
        print("[DATABASE SETUP] Connecting to the attendance database...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Create attendance table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            date DATE NOT NULL,
            INDEX idx_name_date (name, date)
        )
        """

        cursor.execute(create_table_query)
        connection.commit()
        print("[DATABASE SETUP] Attendance table created/verified")

        cursor.close()
        connection.close()

        print("[DATABASE SETUP] Database setup completed successfully!")
        print("[DATABASE SETUP] You can now run: python main.py")

    except Error as err:
        print(f"[DATABASE SETUP ERROR] {err}")
        print("\n[HELP] Please ensure:")
        print("  1. MySQL server is running")
        print("  2. Update config.py with correct MySQL credentials")
        print("  3. Check host, user, and password in config.py")


if __name__ == "__main__":
    setup_database()
