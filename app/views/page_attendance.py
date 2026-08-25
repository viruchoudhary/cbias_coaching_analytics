import streamlit as st
import pandas as pd
from datetime import datetime
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.db_manager import DBManager

def render_attendance_page():
    st.markdown("### 📝 Module 5: Attendance Tracking & Low-Attendance Alerts (<60%)")

    students_df = DBManager.get_table_df("students")
    batches_df = DBManager.get_table_df("batches")
    attendance_df = DBManager.get_table_df("attendance")

    # Build Composite Unique Student Options (ID + Name + Mobile + Batch)
    student_options = []
    student_map = {}
    if not students_df.empty:
        for idx, row in students_df.iterrows():
            s_id = row.get('id', idx + 1)
            name = row.get('full_name', 'Student')
            mob = row.get('parent_mobile', 'N/A')
            batch = row.get('batch_name', 'General')
            
            opt_str = f"ID: #{s_id} - {name} | Mob: {mob} | Batch: {batch}"
            student_options.append(opt_str)
            student_map[opt_str] = (name, s_id)
    else:
        opt_str = "ID: #1 - Aarav Sharma | Mob: 9876543210 | Batch: Batch-A"
        student_options = [opt_str]
        student_map[opt_str] = ("Aarav Sharma", 1)

    st.subheader("⚠️ Low Attendance Warnings (<60% Threshold)")
    if not attendance_df.empty:
        att_counts = attendance_df.groupby(['student_name', 'status'])['attendance_id'].count().unstack(fill_value=0)
        if 'Present' in att_counts.columns:
            att_counts['Total_Classes'] = att_counts.sum(axis=1)
            att_counts['Attendance_Pct'] = round((att_counts['Present'] / att_counts['Total_Classes']) * 100.0, 1)

            low_att_df = att_counts[att_counts['Attendance_Pct'] < 60.0].reset_index()
            if not low_att_df.empty:
                st.error(f"🚨 **{len(low_att_df)} Students** have Attendance Below 60%!")
                st.dataframe(low_att_df[['student_name', 'Present', 'Total_Classes', 'Attendance_Pct']], use_container_width=True)
            else:
                st.success("✅ Excellent! All active students have Attendance >= 60%.")

    st.markdown("---")

    with st.expander("📝 Mark Daily Student Attendance", expanded=False):
        with st.form("mark_attendance_form"):
            ac1, ac2 = st.columns(2)
            batch_sel = ac1.selectbox("Select Batch *", batches_df['batch_name'].tolist() if not batches_df.empty else ["DATA-Batch-01"])
            selected_option = ac2.selectbox("Select Student (Unique ID & Mobile) *", student_options)
            
            raw_name, selected_id = student_map.get(selected_option, ("Student", 1))

            att_date = ac1.date_input("Attendance Date")
            att_status = ac2.radio("Status *", ["Present", "Absent", "Leave"], horizontal=True)

            att_sub = st.form_submit_button("✅ Record Attendance Log")
            if att_sub and selected_option:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO attendance (student_name, batch_name, attendance_date, status) VALUES (?, ?, ?, ?)",
                    (f"{raw_name} (ID: #{selected_id})", batch_sel, str(att_date), att_status)
                )
                conn.commit()
                conn.close()
                st.success(f"🎉 Attendance Recorded: **{raw_name} (ID: #{selected_id})** marked **{att_status}** for {batch_sel}!")
                st.rerun()

    st.markdown("---")
    st.subheader("📋 Master Attendance Logs Directory")
    st.dataframe(attendance_df, use_container_width=True)

if __name__ == '__main__':
    render_attendance_page()
