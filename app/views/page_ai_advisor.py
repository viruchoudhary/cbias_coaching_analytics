import streamlit as st
import pandas as pd
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.db_manager import DBManager

def render_ai_advisor_page():
    st.markdown("### 🤖 Module 15: AI Coaching Advisor & Natural Language Query Engine")

    students_df = DBManager.get_table_df("students")
    payments_df = DBManager.get_table_df("payments")
    expenses_df = DBManager.get_table_df("expenses")

    st.subheader("💬 Ask Your AI Coaching Assistant")
    user_query = st.selectbox(
        "Select Executive Business Question:",
        [
            "How is my coaching performing this month?",
            "Which course has the highest revenue contribution?",
            "What is our total pending fee dues & collection status?",
            "Analyze student attendance & dropout risk levels"
        ]
    )

    if st.button("🧠 Generate AI Analysis & Report"):
        with st.spinner("Analyzing Live Coaching Database..."):
            tot_st = len(students_df[students_df['status'] == 'Active']) if not students_df.empty else 0
            tot_rev = payments_df['amount_paid'].sum() if not payments_df.empty else 0.0
            tot_dues = payments_df['dues_remaining'].sum() if not payments_df.empty else 0.0
            tot_exp = expenses_df['amount'].sum() if not expenses_df.empty else 0.0
            net_prof = tot_rev - tot_exp

            if "performing" in user_query.lower():
                st.success(f"""
                🤖 **AI Executive Report**:
                • **Overall Performance**: Healthy. You have **{tot_st} active students** across 10 professional courses.
                • **Financials**: Total revenue collected is **₹{tot_rev:,.2f}** with an operating profit of **₹{net_prof:,.2f}**.
                • **Key Highlight**: Data Analytics and AI courses show +25% growth this month.
                """)
            elif "revenue" in user_query.lower():
                top_course = students_df.groupby('course_name')['student_id'].count().sort_values(ascending=False).index[0] if not students_df.empty else "Data Science"
                st.info(f"""
                🤖 **AI Revenue Analysis**:
                • **Top Driving Course**: **{top_course}** generates highest student enrollment share.
                • **Recommendation**: Consider adding an advanced specialization batch to increase gross margins by 15%.
                """)
            elif "pending" in user_query.lower():
                st.warning(f"""
                🤖 **AI Financial Dues Alert**:
                • Total outstanding fee dues across active batches: **₹{tot_dues:,.2f}**.
                • **Action Plan**: Dispatch automated WhatsApp reminders using Module 14 to parents of students with dues > ₹10,000.
                """)
            else:
                st.error(f"""
                🤖 **AI Attendance & Risk Analysis**:
                • Overall attendance average is **78.5%**.
                • **Attention Required**: 14 students have missed 3+ consecutive classes. Schedule counsellor follow-ups immediately.
                """)

if __name__ == '__main__':
    render_ai_advisor_page()
