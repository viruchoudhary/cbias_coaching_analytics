import streamlit as st
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.auth import AuthManager
from src.db_manager import DBManager

def render_login_page():
    st.markdown("### 🔐 Security & Access Control Portal (RBAC & Hashing)")

    t1, t2, t3, t4 = st.tabs(["🔐 User Login", "➕ Register New User", "🔑 Change Password", "🗑️ Reset / Start Fresh Data"])

    # 1. Login Tab
    with t1:
        st.subheader("🔐 Login to CBIAS SaaS")
        with st.form("login_form"):
            username = st.text_input("Username *", value="admin")
            password = st.text_input("Password *", type="password", value="admin123")

            log_sub = st.form_submit_button("🚀 Authenticate & Login")
            if log_sub and username and password:
                user = AuthManager.authenticate_user(username, password)
                if user:
                    st.session_state['authenticated'] = True
                    st.session_state['active_user'] = user[0]
                    st.session_state['active_role'] = user[1]
                    st.session_state['active_name'] = user[2]
                    st.success(f"🎉 Welcome **{user[2]}**! Logged in as **{user[1]}**.")
                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password!")

    # 2. Register New User Account
    with t2:
        st.subheader("➕ Create New Staff / User Account")
        with st.form("reg_user_form"):
            r_uname = st.text_input("New Username *", placeholder="e.g. rohan_teacher")
            r_pass = st.text_input("Set Custom Password *", type="password")
            r_name = st.text_input("Full Name *", placeholder="e.g. Rohan Sharma")
            r_role = st.selectbox("Assign Access Role *", ["👑 Owner / Director", "🛠️ Admin", "💰 Accountant", "👨‍🏫 Faculty / Teacher"])

            reg_sub = st.form_submit_button("✅ Create Account")
            if reg_sub and r_uname and r_pass and r_name:
                ok, msg = AuthManager.register_user(r_uname, r_pass, r_role, r_name)
                if ok:
                    st.success(f"🎉 Account Created! Username: **{r_uname}** | Role: {r_role}")
                else:
                    st.error(f"❌ {msg}")

    # 3. Change Password Portal
    with t3:
        st.subheader("🔑 Change Password")
        with st.form("change_pass_form"):
            c_uname = st.text_input("Username *", value="admin")
            c_old_p = st.text_input("Current Old Password *", type="password")
            c_new_p = st.text_input("New Password *", type="password")

            cp_sub = st.form_submit_button("🔄 Update Password")
            if cp_sub and c_uname and c_old_p and c_new_p:
                ok, msg = AuthManager.change_password(c_uname, c_old_p, c_new_p)
                if ok:
                    st.success(f"🎉 Password Changed Successfully for **{c_uname}**!")
                else:
                    st.error(f"❌ {msg}")

    # 4. Reset & Start Fresh Coaching Data
    with t4:
        st.subheader("🗑️ Reset & Start Fresh Coaching Data")
        st.warning("⚠️ **Attention Directors**: This action will clear all demo student records, payment ledgers, and attendance logs so your new coaching institute can start with **0 Students and ₹0 Revenue**!")
        
        with st.form("reset_coaching_data_form"):
            st.markdown("Confirm Reset: Type `CONFIRM_RESET` in the box below:")
            reset_key = st.text_input("Security Reset Key *", placeholder="CONFIRM_RESET")
            reset_submit = st.form_submit_button("💥 Clear Demo Data & Start Fresh")
            
            if reset_submit and reset_key == "CONFIRM_RESET":
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students;")
                cursor.execute("DELETE FROM payments;")
                cursor.execute("DELETE FROM attendance;")
                cursor.execute("DELETE FROM test_scores;")
                cursor.execute("DELETE FROM leads;")
                cursor.execute("DELETE FROM expenses;")
                conn.commit()
                conn.close()
                st.success("🎉 All Demo Data Cleared Successfully! Your Coaching Institute is now 100% Fresh (0 Students, ₹0 Revenue)!")
                st.rerun()

if __name__ == '__main__':
    render_login_page()