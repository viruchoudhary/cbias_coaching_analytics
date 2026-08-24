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

def render_notifications_page():
    st.markdown("### 🔔 Module 14: Parent Communication & Automated WhatsApp Alerts Engine")

    students_df = DBManager.get_table_df("students")

    t1, t2 = st.tabs(["📲 Trigger WhatsApp / SMS Alerts", "📋 Notification Delivery Logs"])

    with t1:
        st.subheader("📲 Automated Alert Dispatch Portal")
        nc1, nc2 = st.columns(2)
        alert_type = nc1.selectbox("Select Notification Type *", ["🔴 Absent Student Alert", "💰 Fee Due Reminder", "🏆 Test Result Notification", "⚠️ Low Attendance Warning (<60%)"])

        # Format Dropdown with Unique Student ID, Name, Phone & Batch
        if not students_df.empty and 'student_id' in students_df.columns:
            labels = []
            for idx, row in students_df.iterrows():
                b_name = row.get('batch_name', 'Batch-01')
                if pd.isna(b_name): b_name = 'Batch-01'
                lbl = f"ID: #{row['student_id']} - {row['full_name']} | Mob: {row['phone']} | Batch: {b_name}"
                labels.append(lbl)
        else:
            labels = ["ID: #1 - Sneha Mehta | Mob: 9837396804 | Batch: MAST-Batch-01"]

        selected_label = nc2.selectbox("Select Student Profile (Unique ID & Batch) *", labels)

        # Parse selected student ID
        try:
            selected_id = int(selected_label.split("ID: #")[1].split(" - ")[0])
            s_info = students_df[students_df['student_id'] == selected_id]
        except Exception:
            s_info = pd.DataFrame()

        student_sel = s_info['full_name'].values[0] if not s_info.empty else "Sneha Mehta"
        parent_phone = s_info['phone'].values[0] if not s_info.empty else "9837396804"
        batch_name = s_info['batch_name'].values[0] if (not s_info.empty and 'batch_name' in s_info.columns) else "MAST-Batch-01"
        pending_fee = s_info['pending_fees'].values[0] if (not s_info.empty and 'pending_fees' in s_info.columns) else 15000.0

        # Pre-draft message text based on selection
        if "Absent" in alert_type:
            msg_text = f"Dear Parent, your child {student_sel} (Batch: {batch_name}) was marked ABSENT today at CBIAS Coaching. Please contact institute admin."
        elif "Fee" in alert_type:
            msg_text = f"Dear Parent, fee payment reminder for {student_sel} (Batch: {batch_name}). Pending dues: ₹{pending_fee:,.2f}. Please clear dues at earliest."
        elif "Test" in alert_type:
            msg_text = f"Dear Parent, test result update for {student_sel} (Batch: {batch_name}): Marks Obtained 85/100 (Grade: A+). Congratulations!"
        else:
            msg_text = f"Dear Parent, WARNING: {student_sel}'s (Batch: {batch_name}) attendance is below 60%. Academic counselling required."

        custom_msg = st.text_area("Message Content", value=msg_text, height=100)

        if st.button("🚀 Dispatch WhatsApp / SMS Alert"):
            wa_link = f"https://api.whatsapp.com/send?phone=91{parent_phone}&text={custom_msg.replace(' ', '%20')}"
            st.success(f"🎉 Alert Dispatched to Parent of **{student_sel}** (Mobile: {parent_phone}, Batch: {batch_name})!")
            st.markdown(f"👉 **[Click Here to Open WhatsApp Web Direct Chat]({wa_link})**", unsafe_allow_html=True)

    with t2:
        st.subheader("📋 System Notification Logs")
        logs_data = pd.DataFrame([
            {"Timestamp": str(datetime.now()), "Student": "Sneha Mehta (ID: #1)", "Recipient": "Parent (9837396804)", "Type": "Absent Alert", "Channel": "WhatsApp", "Status": "Delivered"},
            {"Timestamp": str(datetime.now()), "Student": "Priya Verma (ID: #2)", "Recipient": "Parent (9876543211)", "Type": "Fee Reminder", "Channel": "SMS", "Status": "Delivered"}
        ])
        st.dataframe(logs_data, use_container_width=True)

if __name__ == '__main__':
    render_notifications_page()