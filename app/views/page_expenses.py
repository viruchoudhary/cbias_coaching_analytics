import streamlit as st
import pandas as pd
from datetime import datetime
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
    from components.charts import create_donut_chart
except Exception:
    from app.components.charts import create_donut_chart

def render_expenses_page():
    st.markdown("### 💸 Module 9: Operational Expense Ledger Management")

    expenses_df = DBManager.get_table_df("expenses")

    with st.expander("💸 Log New Operational Expense Bill", expanded=False):
        with st.form("new_expense_form"):
            ec1, ec2 = st.columns(2)
            cat = ec1.selectbox("Expense Category *", ["Faculty Salary", "Office Rent", "Marketing & Meta Ads", "Electricity & Utilities", "Software Subscriptions"])
            amt = ec2.number_input("Amount (₹) *", min_value=100.0, value=15000.0, step=500.0)
            ex_date = ec1.date_input("Expense Date")
            desc = ec2.text_input("Description", placeholder="e.g. Monthly rent bill")

            ex_sub = st.form_submit_button("✅ Record Expense Bill")
            if ex_sub and amt > 0:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO expenses (category, amount, expense_date, description) VALUES (?, ?, ?, ?)",
                    (cat, amt, str(ex_date), desc)
                )
                conn.commit()
                conn.close()
                st.success(f"🎉 Expense Bill of **₹{amt:,.2f}** recorded for {cat}!")
                st.rerun()

    st.markdown("---")

    if not expenses_df.empty:
        st.subheader("📊 Category-wise Expense Breakdown")
        cat_exp = expenses_df.groupby('category')['amount'].sum().reset_index()
        fig_donut = create_donut_chart(cat_exp, names_col='category', values_col='amount', title="Expense Distribution (₹)")
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Master Operational Expense Ledger")
    st.dataframe(expenses_df, use_container_width=True)

if __name__ == '__main__':
    render_expenses_page()
