import streamlit as st
import pandas as pd
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.db_manager import DBManager

def render_insights_page():
    st.markdown("### 💡 Module 12: Smart Automated Business Insights & Strategic Action Plan")

    students_df = DBManager.get_table_df("students")
    payments_df = DBManager.get_table_df("payments")
    leads_df = DBManager.get_table_df("leads")

    st.subheader("🚀 Executive Automated Bulletins")

    if not students_df.empty:
        pop_course = students_df.groupby('course_name')['student_id'].count().sort_values(ascending=False).index[0]
        c_count = len(students_df[students_df['course_name'] == pop_course])
        st.success(f"🔥 **Top Performing Course**: **{pop_course}** is your most popular course with **{c_count} enrolled students** (+25% growth this month).")

    if not payments_df.empty:
        tot_dues = payments_df['dues_remaining'].sum()
        st.warning(f"⚠️ **Pending Dues Alert**: **₹{tot_dues:,.2f} total pending fees** remaining across active batches. Schedule fee collection reminders.")

    if not leads_df.empty:
        top_source = leads_df.groupby('lead_source')['lead_id'].count().sort_values(ascending=False).index[0]
        st.info(f"📢 **Highest Lead Channel**: **{top_source}** generated the highest inquiry volume. Increase Meta ad spend budget here.")

    st.markdown("---")
    st.subheader("🎯 Director Priority Action Plan")
    st.markdown("""
    1. **Fee Dues Drive**: Instruct Accountant to issue automated WhatsApp reminder alerts for dues > ₹10,000.
    2. **At-Risk Student Intervention**: Direct Counsellor team to contact 🔴 High-Risk students (<60% Attendance) before dropouts occur.
    3. **Faculty Recognition**: Award top rating faculty members for high student satisfaction scores.
    """)

if __name__ == '__main__':
    render_insights_page()
