import streamlit as st
import pandas as pd
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.db_manager import DBManager

def render_courses_page():
    st.markdown("### 📚 Module 3: Course Catalog & Batch Management Portal")

    courses_df = DBManager.get_table_df("courses")
    batches_df = DBManager.get_table_df("batches")

    c_left, c_right = st.columns(2)

    with c_left:
        with st.expander("➕ Create New Course", expanded=False):
            with st.form("new_course_form"):
                c_name = st.text_input("Course Name *")
                c_duration = st.number_input("Duration (Months)", min_value=1, max_value=24, value=6)
                c_fee = st.number_input("Total Course Fee (₹)", min_value=1000.0, value=30000.0, step=1000.0)

                c_sub = st.form_submit_button("✅ Create Course")
                if c_sub and c_name:
                    conn = DBManager.get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO courses (course_name, duration_months, total_fee) VALUES (?, ?, ?)",
                        (c_name, c_duration, c_fee)
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"🎉 Course **{c_name}** Created Successfully!")
                    st.rerun()

    with c_right:
        with st.expander("➕ Create New Batch", expanded=False):
            with st.form("new_batch_form"):
                b_name = st.text_input("Batch Code/Name *")
                b_course = st.selectbox("Select Course", courses_df['course_name'].tolist() if not courses_df.empty else ["Data Science"])
                b_faculty = st.text_input("Assigned Faculty Name", value="Vikram Sir")
                b_slot = st.selectbox("Time Slot", ["09:00 AM - 11:00 AM", "11:30 AM - 01:30 PM", "04:00 PM - 06:00 PM"])

                b_sub = st.form_submit_button("✅ Create Batch")
                if b_sub and b_name:
                    conn = DBManager.get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO batches (batch_name, course_name, faculty_name, time_slot, capacity) VALUES (?, ?, ?, ?, ?)",
                        (b_name, b_course, b_faculty, b_slot, 35)
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"🎉 Batch **{b_name}** Created Successfully!")
                    st.rerun()

    st.markdown("---")
    t1, t2 = st.tabs(["📚 Course Catalog & Fees", "🕒 Active Batches & Time Slots"])

    with t1:
        st.subheader("📚 Active Offered Courses")
        st.dataframe(courses_df, use_container_width=True)

    with t2:
        st.subheader("🕒 Active Time-Slot Batches")
        st.dataframe(batches_df, use_container_width=True)

if __name__ == '__main__':
    render_courses_page()
