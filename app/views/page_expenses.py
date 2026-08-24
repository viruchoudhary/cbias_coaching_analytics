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
try:
    from components.charts import create_donut_chart, create_bar_chart
except Exception:
    from app.components.charts import create_donut_chart, create_bar_chart

def render_expenses_page():
    st.markdown("### 💸 Module 9: Operational Expense Ledger Management")

    expenses_df = DBManager.get_table_df("expenses")

    # 1. Log New Expense Form with Custom Category Feature
    with st.expander("💸 Log New Operational Expense Bill", expanded=True):
        with st.form("new_expense_form"):
            c1, c2 = st.columns(2)
            
            # Preset Categories + Explicit Custom Option
            cat_options = [
                "Faculty Salary", 
                "Building Rent", 
                "Meta & Google Ads", 
                "Electricity & Utilities", 
                "Tea & Office Snacks", 
                "Printing & Stationery",
                "Wi-Fi & Internet Bill",
                "Furniture Repair & Maintenance",
                "➕ Type Custom Category Manually..."
            ]
            selected_cat = c1.selectbox("Expense Category *", cat_options)
            custom_cat = c1.text_input("Enter Custom Category Name (if selected Custom above):", placeholder="e.g. AC Repair Bill")

            amount = c2.number_input("Amount (₹) *", min_value=0.0, value=5000.0, step=500.0)

            c3, c4 = st.columns(2)
            exp_date = c3.date_input("Expense Date")
            description = c4.text_input("Description", placeholder="e.g. Monthly AC Repair Bill")

            submit = st.form_submit_button("✅ Record Expense Bill")
            if submit and amount > 0:
                if "Custom" in selected_cat and custom_cat.strip():
                    final_category = custom_cat.strip()
                elif "Custom" in selected_cat and not custom_cat.strip():
                    final_category = "General Operational Expense"
                else:
                    final_category = selected_cat

                conn = DBManager.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO expenses (category, amount, expense_date, description) VALUES (?, ?, ?, ?)",
                    (final_category, amount, str(exp_date), description)
                )
                conn.commit()
                conn.close()
                st.success(f"🎉 Expense Bill of **₹{amount:,.2f}** recorded under Category: **{final_category}**!")
                st.rerun()

    st.markdown("---")

    # 2. Expense Metrics & Analytics Charts
    if not expenses_df.empty:
        total_exp = expenses_df['amount'].sum()
        st.metric("💸 Total Operating Expenses", f"₹{total_exp:,.2f}")

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("📊 Category-wise Expense Breakdown")
            fig_pie = create_donut_chart(expenses_df, names_col='category', values_col='amount', title="Expenses by Category")
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            st.subheader("📋 Expenses Log Ledger")
            st.dataframe(expenses_df, use_container_width=True)

if __name__ == '__main__':
    render_expenses_page()
