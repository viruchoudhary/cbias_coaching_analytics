import sqlite3
import pandas as pd
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cbias.db'))

class DBManager:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def init_db():
        conn = DBManager.get_connection()
        cursor = conn.cursor()

        # Users Table
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, role TEXT NOT NULL, full_name TEXT NOT NULL)")
        # Courses Table
        cursor.execute("CREATE TABLE IF NOT EXISTS courses (course_id INTEGER PRIMARY KEY AUTOINCREMENT, course_name TEXT UNIQUE NOT NULL, duration_months INTEGER NOT NULL, total_fee REAL NOT NULL)")
        # Batches Table
        cursor.execute("CREATE TABLE IF NOT EXISTS batches (batch_id INTEGER PRIMARY KEY AUTOINCREMENT, batch_name TEXT UNIQUE NOT NULL, course_name TEXT NOT NULL, faculty_name TEXT NOT NULL, time_slot TEXT NOT NULL, capacity INTEGER DEFAULT 30)")
        
        # 4. Students Master Table (Expanded 18 Fields Schema)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            father_name TEXT,
            mother_name TEXT,
            phone TEXT NOT NULL,
            parent_mobile TEXT,
            email TEXT,
            address TEXT,
            course_name TEXT NOT NULL,
            batch_name TEXT NOT NULL,
            admission_date DATE NOT NULL,
            joining_date DATE,
            total_fees REAL DEFAULT 0.0,
            paid_fees REAL DEFAULT 0.0,
            pending_fees REAL DEFAULT 0.0,
            pending_dues REAL DEFAULT 0.0,
            status TEXT DEFAULT 'Active',
            photo_path TEXT,
            notes TEXT
        )
        """)

        # Automated Column Migration (Ensures existing tables get new 18 fields safely)
        cursor.execute("PRAGMA table_info(students)")
        existing_student_cols = [c[1] for c in cursor.fetchall()]

        required_student_cols = [
            ("father_name", "TEXT"), ("mother_name", "TEXT"), ("parent_mobile", "TEXT"),
            ("address", "TEXT"), ("joining_date", "DATE"), ("total_fees", "REAL DEFAULT 0.0"),
            ("paid_fees", "REAL DEFAULT 0.0"), ("pending_fees", "REAL DEFAULT 0.0"),
            ("pending_dues", "REAL DEFAULT 0.0"), ("photo_path", "TEXT"), ("notes", "TEXT")
        ]

        for col_name, col_type in required_student_cols:
            if col_name not in existing_student_cols:
                try:
                    cursor.execute(f"ALTER TABLE students ADD COLUMN {col_name} {col_type}")
                except Exception:
                    pass

        # Payments Table
        cursor.execute("CREATE TABLE IF NOT EXISTS payments (payment_id INTEGER PRIMARY KEY AUTOINCREMENT, receipt_no TEXT UNIQUE NOT NULL, student_name TEXT NOT NULL, amount_paid REAL NOT NULL, payment_mode TEXT NOT NULL, payment_date DATE NOT NULL, dues_remaining REAL DEFAULT 0.0)")
        # Attendance Table
        cursor.execute("CREATE TABLE IF NOT EXISTS attendance (attendance_id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT NOT NULL, batch_name TEXT NOT NULL, attendance_date DATE NOT NULL, status TEXT NOT NULL)")
        # Leads Table
        cursor.execute("CREATE TABLE IF NOT EXISTS leads (lead_id INTEGER PRIMARY KEY AUTOINCREMENT, lead_name TEXT NOT NULL, phone TEXT NOT NULL, lead_source TEXT NOT NULL, status TEXT DEFAULT 'New', enquiry_date DATE NOT NULL)")
        # Expenses Table
        cursor.execute("CREATE TABLE IF NOT EXISTS expenses (expense_id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL, amount REAL NOT NULL, expense_date DATE NOT NULL, description TEXT)")
        
        # Tenants Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tenants (
            tenant_id TEXT PRIMARY KEY,
            institute_name TEXT NOT NULL,
            director TEXT NOT NULL,
            phone TEXT NOT NULL,
            city TEXT NOT NULL,
            plan TEXT NOT NULL,
            status TEXT DEFAULT 'Active',
            onboard_date DATE NOT NULL
        )
        """)

        # Seed Default Tenants if empty
        cursor.execute("SELECT COUNT(*) FROM tenants")
        if cursor.fetchone()[0] == 0:
            default_tenants = [
                ("TNT-001", "Viru Choudhary BI Academy", "Viru Choudhary", "9876543210", "Jaipur", "Professional", "Active", "2024-01-01"),
                ("TNT-002", "Kota Science Analytics Institute", "Dr. Sharma", "9876543211", "Kota", "Standard", "Active", "2024-01-10"),
                ("TNT-003", "Delhi Commerce Hub", "Rajesh Verma", "9876543212", "Delhi", "Basic", "Active", "2024-02-01")
            ]
            cursor.executemany("INSERT INTO tenants (tenant_id, institute_name, director, phone, city, plan, status, onboard_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", default_tenants)

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
    print("CBIAS SQLite Database initialized successfully with Tenants Table!")