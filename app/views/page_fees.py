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

    # Build Composite Unique Student Options (ID + Name + Mobile + Batch + Dues)
    student_options = []
    student_map = {}
    if not students_df.empty:
        for idx, row in students_df.iterrows():
            s_id = row.get('student_id', row.get('id', idx + 1))
            name = row.get('full_name', 'Student')
            mob = row.get('parent_mobile', row.get('phone', 'N/A'))
            batch = row.get('batch_name', 'General')
            dues = row.get('pending_dues', row.get('pending_fees', 15000.0))
            if pd.isna(dues): dues = 15000.0
            
            opt_str = f"ID: #{s_id} - {name} | Mob: {mob} | Batch: {batch}"
            student_options.append(opt_str)
            student_map[opt_str] = (name, s_id, float(dues))
    else:
        opt_str = "ID: #1 - Aarav Sharma | Mob: 9876543210 | Batch: Batch-A"
        student_options = [opt_str]
        student_map[opt_str] = ("Aarav Sharma", 1, 15000.0)

    with st.expander("💵 Collect Fee & Issue Digital Receipt", expanded=False):
        with st.form("fee_collection_form"):
            c1, c2 = st.columns(2)
            selected_option = c1.selectbox("Select Student (Unique ID & Mobile) *", student_options)
            
            # Extract student details from selected composite string
            raw_name, selected_id, auto_dues = student_map.get(selected_option, ("Student", 1, 15000.0))

            amount_paid = c2.number_input("Amount Collected (₹) *", min_value=500.0, value=5000.0, step=500.0)
            pay_mode = c1.selectbox("Payment Mode *", ["UPI (PhonePe/GPay)", "Cash", "Bank Transfer", "Credit Card"])
            dues_remaining = c2.number_input("Remaining Dues (₹)", min_value=0.0, value=float(max(0.0, auto_dues - amount_paid)), step=500.0)

            rec_submit = st.form_submit_button("🧾 Record Payment & Generate Receipt")
            if rec_submit and selected_option:
                receipt_no = f"REC-2024-{len(payments_df)+1:04d}"
                pay_date = str(datetime.now().date())

                conn = DBManager.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO payments (receipt_no, student_name, amount_paid, payment_mode, payment_date, dues_remaining) VALUES (?, ?, ?, ?, ?, ?)",
                    (receipt_no, f"{raw_name} (ID: #{selected_id})", amount_paid, pay_mode, pay_date, dues_remaining)
                )
                conn.commit()

                # Fail-safe update for students table if pending_dues or pending_fees exists
                try:
                    cursor.execute("UPDATE students SET pending_dues = ? WHERE student_id = ?", (dues_remaining, selected_id))
                    conn.commit()
                except Exception:
                    try:
                        cursor.execute("UPDATE students SET pending_fees = ? WHERE student_id = ?", (dues_remaining, selected_id))
                        conn.commit()
                    except Exception:
                        pass

                conn.close()

                st.success(f"🎉 Payment Recorded Successfully for **{raw_name} (ID: #{selected_id})**! Receipt No: **{receipt_no}**")
                st.markdown(f"""
                <div style='background:#ffffff; padding:20px; border-radius:12px; border:2px solid #059669; box-shadow: 0 4px 12px rgba(0,0,0,0.05);'>
                    <h4 style='color:#047857; margin:0;'>🧾 OFFICIAL FEE RECEIPT - CBIAS</h4>
                    <p><b>Receipt No:</b> {receipt_no} | <b>Date:</b> {pay_date}</p>
                    <p><b>Student Name:</b> {raw_name} (ID: #{selected_id})</p>
                    <p><b>Amount Paid:</b> <span style='font-size:1.2rem; color:#059669;'>₹{amount_paid:,.2f}</span> via {pay_mode}</p>
                    <p><b>Dues Remaining:</b> ₹{dues_remaining:,.2f}</p>
                    <p style='font-size:0.8rem; color:#64748b;'>Status: Verified & Authorized Signature Stamp</p>
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
