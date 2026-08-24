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

def render_fees_page():
    st.markdown("### 💰 Module 4: Fee Collection & Printable Receipt Generator")

    students_df = DBManager.get_table_df("students")
    payments_df = DBManager.get_table_df("payments")

    with st.expander("💵 Collect Fee & Issue Digital Receipt", expanded=False):
        with st.form("fee_collection_form"):
            c1, c2 = st.columns(2)
            student_name = c1.selectbox("Select Student *", students_df['full_name'].tolist() if not students_df.empty else ["Aarav Sharma"])
            amount_paid = c2.number_input("Amount Collected (₹) *", min_value=500.0, value=5000.0, step=500.0)
            pay_mode = c1.selectbox("Payment Mode *", ["UPI (PhonePe/GPay)", "Cash", "Bank Transfer", "Credit Card"])
            dues_remaining = c2.number_input("Remaining Dues (₹)", min_value=0.0, value=15000.0, step=500.0)

            rec_submit = st.form_submit_button("🧾 Record Payment & Generate Receipt")
            if rec_submit and student_name:
                receipt_no = f"REC-2024-{len(payments_df)+1:04d}"
                pay_date = str(datetime.now().date())

                conn = DBManager.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO payments (receipt_no, student_name, amount_paid, payment_mode, payment_date, dues_remaining) VALUES (?, ?, ?, ?, ?, ?)",
                    (receipt_no, student_name, amount_paid, pay_mode, pay_date, dues_remaining)
                )
                conn.commit()
                conn.close()

                st.success(f"🎉 Payment Recorded Successfully! Receipt No: **{receipt_no}**")
                st.markdown(f"""
                <div style='background:#1e293b; padding:20px; border-radius:12px; border:1px solid #10b981;'>
                    <h4 style='color:#10b981; margin:0;'>🧾 OFFICIAL FEE RECEIPT - CBIAS</h4>
                    <p><b>Receipt No:</b> {receipt_no} | <b>Date:</b> {pay_date}</p>
                    <p><b>Student Name:</b> {student_name}</p>
                    <p><b>Amount Paid:</b> <span style='font-size:1.2rem; color:#34d399;'>₹{amount_paid:,.2f}</span> via {pay_mode}</p>
                    <p><b>Dues Remaining:</b> ₹{dues_remaining:,.2f}</p>
                    <p style='font-size:0.8rem; color:#94a3b8;'>Status: Verified & Authorized Signature Stamp</p>
                </div>
                """, unsafe_allow_html=True)
                st.rerun()

    st.markdown("---")
    st.subheader("📋 Master Payment Transaction Ledger")
    mc1, mc2 = st.columns([1, 2])
    mode_filter = mc1.selectbox("Filter Payment Mode:", ["All", "UPI (PhonePe/GPay)", "Cash", "Bank Transfer", "Credit Card"])
    p_search = mc2.text_input("🔍 Search Receipt or Student Name:", placeholder="e.g. REC-2024 or Aarav")

    filtered_pay = payments_df.copy()
    if mode_filter != "All":
        filtered_pay = filtered_pay[filtered_pay['payment_mode'] == mode_filter]

    if p_search:
        filtered_pay = filtered_pay[
            filtered_pay['receipt_no'].str.contains(p_search, case=False, na=False) |
            filtered_pay['student_name'].str.contains(p_search, case=False, na=False)
        ]

    st.dataframe(filtered_pay, use_container_width=True)

if __name__ == '__main__':
    render_fees_page()
