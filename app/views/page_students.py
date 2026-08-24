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

    with st.expander("➕ Register New Student Admission", expanded=False):
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
