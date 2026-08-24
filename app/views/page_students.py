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
                pend_fee = tot_fee - paid_fee
                c7.metric("Pending Dues (₹)", f"₹{pend_fee:,.2f}")

                notes = st.text_input("Special Remarks / Notes")
                photo_file = st.file_uploader("Upload Student Photo", type=["jpg", "png", "jpeg"])

                submit = st.form_submit_button("✅ Register Complete Student Profile")
                if submit and name and phone:
                    photo_name = photo_file.name if photo_file else "default.png"
                    conn = DBManager.get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """INSERT INTO students (full_name, father_name, mother_name, phone, parent_mobile, email, address, course_name, batch_name, admission_date, joining_date, total_fees, paid_fees, pending_fees, status, photo_path, notes) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (name, f_name, m_name, phone, p_phone, email, address, course, batch, str(adm_date), str(join_date), tot_fee, paid_fee, pend_fee, "Active", photo_name, notes)
                    )
                    conn.commit()
                    conn.close()
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
    st.subheader("📋 Registered Students Master Directory (18 Fields)")
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