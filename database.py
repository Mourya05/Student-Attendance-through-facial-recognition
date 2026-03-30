"""
Database connection and management module for the Attendance System
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
from config import DB_CONFIG


class AttendanceDatabase:
    """Manages database operations for the attendance system"""

    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            print("[DATABASE] Connected to MySQL database successfully")
            self._create_tables()
            return True
        except Error as err:
            print(f"[DATABASE ERROR] Failed to connect to database: {err}")
            return False

    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
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
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("[DATABASE] Attendance table verified/created")
        except Error as err:
            print(f"[DATABASE ERROR] Failed to create tables: {err}")

    def is_already_marked(self, name):
        """
        Check if a person has already been marked present today

        Args:
            name (str): Name of the person

        Returns:
            bool: True if already marked, False otherwise
        """
        try:
            query = """
            SELECT COUNT(*) FROM attendance 
            WHERE name = %s AND date = CURDATE()
            """
            self.cursor.execute(query, (name,))
            result = self.cursor.fetchone()
            return result[0] > 0
        except Error as err:
            print(f"[DATABASE ERROR] Failed to check attendance: {err}")
            return False

    def mark_attendance(self, name):
        """
        Mark attendance for a person in the database

        Args:
            name (str): Name of the person

        Returns:
            bool: True if marked successfully, False otherwise
        """
        try:
            # Check if already marked today
            if self.is_already_marked(name):
                print(f"[DATABASE] {name} already marked for today")
                return False

            # Insert new attendance record
            insert_query = """
            INSERT INTO attendance (name, timestamp, date) 
            VALUES (%s, %s, CURDATE())
            """
            current_time = datetime.now()
            self.cursor.execute(insert_query, (name, current_time))
            self.connection.commit()
            print(f"[DATABASE] Attendance marked for {name} at {current_time}")
            return True

        except Error as err:
            print(f"[DATABASE ERROR] Failed to mark attendance: {err}")
            self.connection.rollback()
            return False

    def get_today_attendance(self):
        """
        Retrieve all attendance records for today

        Returns:
            list: List of tuples with (id, name, timestamp, date)
        """
        try:
            query = """
            SELECT id, name, timestamp, date FROM attendance 
            WHERE date = CURDATE() 
            ORDER BY timestamp DESC
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as err:
            print(f"[DATABASE ERROR] Failed to retrieve attendance: {err}")
            return []

    def disconnect(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("[DATABASE] Disconnected from MySQL database")
        except Error as err:
            print(f"[DATABASE ERROR] Error during disconnection: {err}")
