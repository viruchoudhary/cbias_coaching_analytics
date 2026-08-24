import streamlit as st
import pandas as pd
import sqlite3
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.db_manager import DBManager

def render_students_page():
    st.markdown("### 👥 Module 2: Student Master Profiles & Enrollment Portal")

    students_df = DBManager.get_table_df("students")
    courses_df = DBManager.get_table_df("courses")
    batches_df = DBManager.get_table_df("batches")

    # 1. Single Student Registration Form
    with st.expander("➕ Register Single Student Admission", expanded=False):
        with st.form("new_student_form"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Full Name *")
            phone = c2.text_input("Mobile Phone Number *")
            email = c1.text_input("Email Address")
            course = c2.selectbox("Select Course *", courses_df['course_name'].tolist() if not courses_df.empty else ["Data Science"])
            batch = c1.selectbox("Assign Batch *", batches_df['batch_name'].tolist() if not batches_df.empty else ["Batch-01"])
            adm_date = c2.date_input("Admission Date")

            submit = st.form_submit_button("✅ Submit Student Admission")
            if submit and name and phone:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO students (full_name, phone, email, course_name, batch_name, admission_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (name, phone, email, course, batch, str(adm_date), "Active")
                )
                conn.commit()
                conn.close()
                st.success(f"🎉 Admission Successful for **{name}** in {course}!")
                st.rerun()

    # 2. 500+ Bulk Excel / CSV Data Importer Section (Expanded by default)
    with st.expander("📥 1-Click Bulk Excel / CSV Student Upload (500+ Students)", expanded=True):
        st.markdown("Upload Excel (`.xlsx`) or CSV (`.csv`) containing student profiles to import 500+ students at once.")
        
        # Sample Template Download Button
        sample_df = pd.DataFrame([
            {"full_name": "Aarav Sharma", "phone": "9876543210", "email": "aarav@gmail.com", "course_name": "Master in Data Science & AI", "batch_name": "MAST-Batch-01", "admission_date": "2024-01-15", "status": "Active"},
            {"full_name": "Priya Verma", "phone": "9876543211", "email": "priya@gmail.com", "course_name": "Full Stack Web Development", "batch_name": "FULL-Batch-01", "admission_date": "2024-01-16", "status": "Active"}
        ])
        st.download_button("📥 Download Sample Excel Template", sample_df.to_csv(index=False).encode('utf-8'), "sample_students_template.csv", "text/csv")

        uploaded_file = st.file_uploader("Choose Excel or CSV File", type=["csv", "xlsx"])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    bulk_df = pd.read_csv(uploaded_file)
                else:
                    bulk_df = pd.read_excel(uploaded_file)

                st.info(f"Loaded **{len(bulk_df)} student records** from file.")
                if st.button("🚀 Confirm & Import Students to Database"):
                    conn = DBManager.get_connection()
                    bulk_df.to_sql("students", conn, if_exists="append", index=False)
                    conn.close()
                    st.success(f"🎉 SUCCESS! **{len(bulk_df)} Student Profiles** imported into Database!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error importing file: {e}")

    st.markdown("---")
    st.subheader("📋 Registered Students Directory")
    fc1, fc2 = st.columns([1, 2])

    status_filter = fc1.selectbox("Filter Status:", ["All", "Active", "Completed", "Dropped"])
    search_query = fc2.text_input("🔍 Search Student by Name or Phone:", placeholder="e.g. Aarav Sharma")

    filtered_df = students_df.copy()
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['status'] == status_filter]

    if search_query:
        filtered_df = filtered_df[
            filtered_df['full_name'].str.contains(search_query, case=False, na=False) |
            filtered_df['phone'].str.contains(search_query, case=False, na=False)
        ]

    st.dataframe(filtered_df, use_container_width=True)

if __name__ == '__main__':
    render_students_page()
