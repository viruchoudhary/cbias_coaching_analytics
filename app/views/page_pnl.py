import streamlit as st
import pandas as pd
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.db_manager import DBManager

def render_pnl_page():
    st.markdown("### 💵 Module 10: Real-Time Financial Profit & Loss (P&L) Statement")

    payments_df = DBManager.get_table_df("payments")
    expenses_df = DBManager.get_table_df("expenses")

    total_revenue = payments_df['amount_paid'].sum() if not payments_df.empty else 0.0
    total_expenses = expenses_df['amount'].sum() if not expenses_df.empty else 0.0
    net_profit = total_revenue - total_expenses
    net_margin = round((net_profit / total_revenue) * 100.0, 1) if total_revenue > 0 else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Gross Fee Revenue", f"₹{total_revenue:,.2f}")
    c2.metric("💸 Total Operating Expenses", f"₹{total_expenses:,.2f}")
    c3.metric("💵 Net Operating Profit", f"₹{net_profit:,.2f}", f"P&L Net Margin: {net_margin}%")
    c4.metric("📈 Profitability Health", "Healthy" if net_margin > 20 else "Audit Needed")

    st.markdown("---")

    st.subheader("📑 Executive P&L Statement Summary")
    pnl_summary = pd.DataFrame([
        {"Financial Line Item": "Gross Fee Collections (Revenue)", "Amount (₹)": f"₹{total_revenue:,.2f}", "P&L Category": "Income"},
        {"Financial Line Item": "Total Operational Expenses (Rent, Salary, Ads)", "Amount (₹)": f"₹{total_expenses:,.2f}", "P&L Category": "Cost"},
        {"Financial Line Item": "Net Operating Profit (EBITDA)", "Amount (₹)": f"₹{net_profit:,.2f}", "P&L Category": "Bottom Line"}
    ])
    st.dataframe(pnl_summary, use_container_width=True)

if __name__ == '__main__':
    render_pnl_page()
