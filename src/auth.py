import hashlib
import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.db_manager import DBManager

class AuthManager:
    """
    Role-Based Access Control (RBAC), Custom User Registration,
    Change Password & SHA-256 Password Hashing Engine.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return AuthManager.hash_password(password) == hashed

    @staticmethod
    def seed_default_users():
        DBManager.init_db()
        conn = DBManager.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
        except sqlite3.OperationalError:
            pass

        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            default_users = [
                ("director", AuthManager.hash_password("owner123"), "👑 Owner / Director", "Virendra Choudhary"),
                ("admin", AuthManager.hash_password("admin123"), "🛠️ Admin", "Coaching Administrator"),
                ("accountant", AuthManager.hash_password("pay123"), "💰 Accountant", "Senior Accountant"),
                ("teacher", AuthManager.hash_password("teach123"), "👨‍🏫 Faculty / Teacher", "Dr. Sharma")
            ]
            for u, p_hash, r, f_name in default_users:
                cursor.execute(
                    "INSERT OR REPLACE INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                    (u, p_hash, r, f_name)
                )

            conn.commit()
        conn.close()

    @staticmethod
    def authenticate_user(username, password):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        p_hash = AuthManager.hash_password(password)
        cursor.execute("SELECT username, role, full_name FROM users WHERE username=? AND password_hash=?", (username, p_hash))
        row = cursor.fetchone()
        conn.close()
        return row

    # 1. Custom User Registration (User Khud Password Set Karega)
    @staticmethod
    def register_user(username, password, role, full_name):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        p_hash = AuthManager.hash_password(password)
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                (username, p_hash, role, full_name)
            )
            conn.commit()
            conn.close()
            return True, "User Created Successfully!"
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Username already exists!"

    # 2. Change Password Engine (Password Badalne Ke Liye)
    @staticmethod
    def change_password(username, old_password, new_password):
        if not AuthManager.authenticate_user(username, old_password):
            return False, "Incorrect Old Password!"
        
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        new_p_hash = AuthManager.hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash=? WHERE username=?", (new_p_hash, username))
        conn.commit()
        conn.close()
        return True, "Password Changed Successfully!"

if __name__ == '__main__':
    AuthManager.seed_default_users()
    print("Auth Engine with Custom User & Password Change initialized!")