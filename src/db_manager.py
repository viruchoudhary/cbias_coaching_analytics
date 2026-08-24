import sqlite3
import pandas as pd
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cbias.db'))

class DBManager:
    """
    SQLite Relational Database Manager Engine for CBIAS.
    Manages 7 core tables: users, students, courses, batches, payments, attendance, leads, expenses.
    """

    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def init_db():
        conn = DBManager.get_connection()
        cursor = conn.cursor()

        # 1. Users Table (Authentication & Roles)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
        """)

        # 2. Courses Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT UNIQUE NOT NULL,
            duration_months INTEGER NOT NULL,
            total_fee REAL NOT NULL
        )
        """)

        # 3. Batches Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS batches (
            batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_name TEXT UNIQUE NOT NULL,
            course_name TEXT NOT NULL,
            faculty_name TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            capacity INTEGER DEFAULT 30
        )
        """)

        # 4. Students Master Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            course_name TEXT NOT NULL,
            batch_name TEXT NOT NULL,
            admission_date DATE NOT NULL,
            status TEXT DEFAULT 'Active'
        )
        """)

        # 5. Payments Ledger Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_no TEXT UNIQUE NOT NULL,
            student_name TEXT NOT NULL,
            amount_paid REAL NOT NULL,
            payment_mode TEXT NOT NULL,
            payment_date DATE NOT NULL,
            dues_remaining REAL DEFAULT 0.0
        )
        """)

        # 6. Attendance Logs Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            batch_name TEXT NOT NULL,
            attendance_date DATE NOT NULL,
            status TEXT NOT NULL
        )
        """)

        # 7. CRM Leads Pipeline Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            lead_source TEXT NOT NULL,
            status TEXT DEFAULT 'New',
            enquiry_date DATE NOT NULL
        )
        """)

        # 8. Operational Expenses Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            expense_date DATE NOT NULL,
            description TEXT
        )
        """)

        conn.commit()
        conn.close()

    @staticmethod
    def get_table_df(table_name):
        conn = DBManager.get_connection()
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df

if __name__ == '__main__':
    DBManager.init_db()
    print("CBIAS SQLite Database initialized successfully!")