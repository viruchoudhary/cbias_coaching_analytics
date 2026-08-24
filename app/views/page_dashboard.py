import streamlit as st
import pandas as pd
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if os.path.join(root_dir, 'app') not in sys.path:
    sys.path.insert(0, os.path.join(root_dir, 'app'))

from src.db_manager import DBManager
try:
    from components.charts import create_line_chart, create_donut_chart, create_gauge_chart
except Exception:
    from app.components.charts import create_line_chart, create_donut_chart, create_gauge_chart

def render_dashboard_page():
    st.markdown("### 📊 Executive BI Dashboard & Key Performance Indicators")

    students_df = DBManager.get_table_df("students")
    payments_df = DBManager.get_table_df("payments")
    expenses_df = DBManager.get_table_df("expenses")

    if students_df.empty or payments_df.empty:
        st.warning("⚠️ Database records empty. Please seed database.")
        return

    total_students = len(students_df[students_df['status'] == 'Active'])
    total_revenue = payments_df['amount_paid'].sum()
    total_dues = payments_df['dues_remaining'].sum()
    total_expenses = expenses_df['amount'].sum() if not expenses_df.empty else 0.0
    net_profit = total_revenue - total_expenses

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Active Students", f"{total_students:,}", "+12% MoM")
    c2.metric("💰 Collected Revenue", f"₹{total_revenue:,.2f}", "+18% Target")
    c3.metric("⚠️ Pending Fee Dues", f"₹{total_dues:,.2f}", "-5% Dues Alert")
    c4.metric("💵 Net Operating Profit", f"₹{net_profit:,.2f}", f"P&L Margin: {round(net_profit/total_revenue*100, 1) if total_revenue>0 else 0}%")

    st.markdown("---")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📈 Monthly Revenue Collection Trend")
        payments_df['payment_date'] = pd.to_datetime(payments_df['payment_date'])
        payments_df['YearMonth'] = payments_df['payment_date'].dt.strftime('%Y-%m')
        monthly_rev = payments_df.groupby('YearMonth')['amount_paid'].sum().reset_index()

        fig_line = create_line_chart(monthly_rev, x_col='YearMonth', y_col='amount_paid', title="Monthly Revenue Trend (₹)")
        st.plotly_chart(fig_line, use_container_width=True)

    with col_right:
        st.subheader("🎯 Target Collection Gauge")
        target_revenue = total_revenue * 1.25
        fig_gauge = create_gauge_chart(value=total_revenue, title="Revenue vs Target (₹)", target=target_revenue)
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")
    st.subheader("📚 Course Enrollment Share")
    course_dist = students_df.groupby('course_name')['student_id'].count().reset_index()
    course_dist.columns = ['course_name', 'student_count']
    fig_donut = create_donut_chart(course_dist, names_col='course_name', values_col='student_count', title="Students per Course")
    st.plotly_chart(fig_donut, use_container_width=True)

if __name__ == '__main__':
    render_dashboard_page()
