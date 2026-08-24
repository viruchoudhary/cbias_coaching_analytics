import streamlit as st
import pandas as pd
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.db_manager import DBManager

def render_risk_page():
    st.markdown("### ⚠️ Module 11: Student Dropout At-Risk Detection Engine")

    students_df = DBManager.get_table_df("students")
    attendance_df = DBManager.get_table_df("attendance")
    payments_df = DBManager.get_table_df("payments")

    if students_df.empty or attendance_df.empty:
        st.info("📂 Student records missing for risk calculation.")
        return

    att_counts = attendance_df.groupby(['student_name', 'status'])['attendance_id'].count().unstack(fill_value=0)
    if 'Present' in att_counts.columns:
        att_counts['Total_Classes'] = att_counts.sum(axis=1)
        att_counts['Attendance_Pct'] = round((att_counts['Present'] / att_counts['Total_Classes']) * 100.0, 1)

    dues_df = payments_df.groupby('student_name')['dues_remaining'].last().reset_index()

    merged_risk = pd.merge(students_df, att_counts[['Attendance_Pct']], left_on='full_name', right_index=True, how='left').fillna(75.0)
    merged_risk = pd.merge(merged_risk, dues_df, left_on='full_name', right_on='student_name', how='left').fillna(0.0)

    def classify_risk(row):
        att = row['Attendance_Pct']
        dues = row['dues_remaining']
        if att < 60.0 and dues > 5000.0:
            return '🔴 High Dropout Risk'
        elif att < 60.0 or dues > 5000.0:
            return '🟡 Medium Risk'
        return '🟢 Safe & Active'

    merged_risk['Risk_Category'] = merged_risk.apply(classify_risk, axis=1)

    high_risk_cnt = len(merged_risk[merged_risk['Risk_Category'] == '🔴 High Dropout Risk'])
    med_risk_cnt = len(merged_risk[merged_risk['Risk_Category'] == '🟡 Medium Risk'])
    safe_cnt = len(merged_risk[merged_risk['Risk_Category'] == '🟢 Safe & Active'])

    rc1, rc2, rc3 = st.columns(3)
    rc1.error(f"🔴 High Dropout Risk: {high_risk_cnt:,} Students")
    rc2.warning(f"🟡 Medium Risk: {med_risk_cnt:,} Students")
    rc3.success(f"🟢 Safe & Active: {safe_cnt:,} Students")

    st.markdown("---")
    st.subheader("📋 At-Risk Students Action Plan Directory")
    st.dataframe(merged_risk[['full_name', 'phone', 'course_name', 'batch_name', 'Attendance_Pct', 'dues_remaining', 'Risk_Category']], use_container_width=True)

if __name__ == '__main__':
    render_risk_page()
