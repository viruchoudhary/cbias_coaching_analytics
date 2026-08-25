import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.db_manager import DBManager

def safe_insert_student(data_dict):
    """Dynamically inserts data into students table matching available columns safely."""
    conn = DBManager.get_connection()
    cursor = conn.cursor()
    
    DBManager.init_db()
    
    cursor.execute("PRAGMA table_info(students)")
    existing_cols = [c[1] for c in cursor.fetchall()]
    
    # Provide mandatory default values for NOT NULL columns
    if 'course_name' not in data_dict or not data_dict.get('course_name'):
        data_dict['course_name'] = "General Course"
    if 'batch_name' not in data_dict or not data_dict.get('batch_name'):
        data_dict['batch_name'] = "Batch-01"
    if 'admission_date' not in data_dict or not data_dict.get('admission_date'):
        data_dict['admission_date'] = str(datetime.now().date())
    if 'status' not in data_dict or not data_dict.get('status'):
        data_dict['status'] = "Active"
    
    valid_dict = {}
    for k, v in data_dict.items():
        if k in existing_cols:
            if pd.isna(v):
                valid_dict[k] = ""
            else:
                valid_dict[k] = v

    cols = ", ".join(valid_dict.keys())
    placeholders = ", ".join(["?"] * len(valid_dict))
    sql = f"INSERT INTO students ({cols}) VALUES ({placeholders})"
    
    cursor.execute(sql, tuple(valid_dict.values()))
    conn.commit()
    conn.close()

def render_students_page():
    st.markdown("### 👥 Module 2: Complete Student Master Profiles (18 Fields Schema)")

    students_df = DBManager.get_table_df("students")
    courses_df = DBManager.get_table_df("courses")
    batches_df = DBManager.get_table_df("batches")

    c_single, c_bulk = st.columns(2)

    # 1. 18-Fields Single Student Registration Form
    with c_single:
        with st.expander("➕ Register Student (18 Fields Detailed Profile)", expanded=False):
            with st.form("new_student_18_form"):
                st.markdown("##### 👤 Personal & Family Info")
                c1, c2 = st.columns(2)
                name = c1.text_input("Full Name *")
                phone = c2.text_input("Student Mobile *")
                f_name = c1.text_input("Father's Name")
                m_name = c2.text_input("Mother's Name")
                p_phone = c1.text_input("Parent Mobile *")
                email = c2.text_input("Email Address")
                address = st.text_area("Permanent Address", height=70)

                st.markdown("##### 📚 Academic & Fee Details")
                c3, c4 = st.columns(2)
                course = c3.selectbox("Select Course *", courses_df['course_name'].tolist() if not courses_df.empty else ["Data Science"])
                batch = c4.selectbox("Assign Batch *", batches_df['batch_name'].tolist() if not batches_df.empty else ["Batch-01"])
                adm_date = c3.date_input("Admission Date")
                join_date = c4.date_input("Batch Joining Date")

                c5, c6, c7 = st.columns(3)
                tot_fee = c5.number_input("Total Fee (₹)", min_value=0.0, value=30000.0, step=1000.0)
                paid_fee = c6.number_input("Paid Fee (₹)", min_value=0.0, value=10000.0, step=1000.0)
                pend_fee = max(0.0, tot_fee - paid_fee)
                c7.metric("Pending Dues (₹)", f"₹{pend_fee:,.2f}")

                notes = st.text_input("Special Remarks / Notes")
                photo_file = st.file_uploader("Upload Student Photo", type=["jpg", "png", "jpeg"])

                submit = st.form_submit_button("✅ Register Complete Student Profile")
                if submit and name and phone:
                    photo_name = photo_file.name if photo_file else "default.png"
                    
                    student_data = {
                        "full_name": name,
                        "father_name": f_name,
                        "mother_name": m_name,
                        "phone": phone,
                        "parent_mobile": p_phone,
                        "email": email,
                        "address": address,
                        "course_name": course,
                        "batch_name": batch,
                        "admission_date": str(adm_date),
                        "joining_date": str(join_date),
                        "total_fees": float(tot_fee),
                        "paid_fees": float(paid_fee),
                        "pending_fees": float(pend_fee),
                        "pending_dues": float(pend_fee),
                        "status": "Active",
                        "photo_path": photo_name,
                        "notes": notes
                    }
                    
                    safe_insert_student(student_data)
                    st.success(f"🎉 Complete Profile Registered for **{name}**!")
                    st.rerun()

    # 2. 500+ Bulk Excel / CSV Data Importer Section
    with c_bulk:
        with st.expander("📥 1-Click Bulk Excel / CSV Upload (500+ Students)", expanded=True):
            st.markdown("Upload Excel (`.xlsx`) or CSV (`.csv`) containing student profiles to import 500+ students at once.")
            
            sample_df = pd.DataFrame([
                {"full_name": "Aarav Sharma", "father_name": "Rajesh Sharma", "mother_name": "Sunita Sharma", "phone": "9876543210", "parent_mobile": "9876543299", "email": "aarav@gmail.com", "address": "Jaipur", "course_name": "Master in Data Science & AI", "batch_name": "MAST-Batch-01", "admission_date": "2024-01-15", "joining_date": "2024-01-20", "total_fees": 45000, "paid_fees": 20000, "pending_fees": 25000, "status": "Active", "notes": "Good Student"}
            ])
            st.download_button("📥 Download 18-Fields Sample Excel Template", sample_df.to_csv(index=False).encode('utf-8'), "sample_18_fields_students.csv", "text/csv")

            uploaded_file = st.file_uploader("Choose Excel or CSV File", type=["csv", "xlsx"])
            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        imp_df = pd.read_csv(uploaded_file)
                    else:
                        imp_df = pd.read_excel(uploaded_file)

                    count = 0
                    for _, r in imp_df.iterrows():
                        r_dict = r.to_dict()
                        if 'full_name' in r_dict and pd.notna(r_dict['full_name']):
                            safe_insert_student(r_dict)
                            count += 1

                    st.success(f"🎉 Successfully Imported **{count} Students** into Master Database!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"❌ Excel Upload Error: {ex}")

    st.markdown("---")
    st.subheader("📋 Active Master Student Roster")
    st.dataframe(students_df, use_container_width=True)

if __name__ == '__main__':
    render_students_page()