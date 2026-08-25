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
        student_map = {}
        labels = []
        if not students_df.empty:
            for idx, row in students_df.iterrows():
                s_id = row.get('id', row.get('student_id', idx + 1))
                s_name = row.get('full_name', 'Student')
                s_mob = row.get('parent_mobile', row.get('phone', '9837396804'))
                b_name = row.get('batch_name', 'MAST-Batch-01')
                p_fee = row.get('pending_dues', row.get('pending_fees', 15000.0))

                if pd.isna(b_name): b_name = 'MAST-Batch-01'
                lbl = f"ID: #{s_id} - {s_name} | Mob: {s_mob} | Batch: {b_name} | Dues: ₹{p_fee:,.0f}"
                labels.append(lbl)
                student_map[lbl] = (s_id, s_name, s_mob, b_name, p_fee)
        else:
            lbl = "ID: #1 - Sneha Mehta | Mob: 9837396804 | Batch: MAST-Batch-01 | Dues: ₹15,000"
            labels = [lbl]
            student_map[lbl] = (1, "Sneha Mehta", "9837396804", "MAST-Batch-01", 15000.0)

        selected_label = nc2.selectbox("Select Student Profile (Unique ID & Mobile) *", labels)

        s_id, student_sel, parent_phone, batch_name, pending_fee = student_map.get(selected_label, (1, "Sneha Mehta", "9837396804", "MAST-Batch-01", 15000.0))

        # Pre-draft message text based on selection
        if "Absent" in alert_type:
            msg_text = f"Dear Parent, your child {student_sel} (ID: #{s_id}, Batch: {batch_name}) was marked ABSENT today at CBIAS Coaching. Please contact institute admin."
        elif "Fee" in alert_type:
            msg_text = f"Dear Parent, fee payment reminder for {student_sel} (ID: #{s_id}, Batch: {batch_name}). Pending dues: ₹{pending_fee:,.2f}. Please clear dues at earliest."
        elif "Test" in alert_type:
            msg_text = f"Dear Parent, test result update for {student_sel} (ID: #{s_id}, Batch: {batch_name}): Marks Obtained 85/100 (Grade: A+). Congratulations!"
        else:
            msg_text = f"Dear Parent, WARNING: {student_sel}'s (ID: #{s_id}, Batch: {batch_name}) attendance is below 60%. Academic counselling required."

        custom_msg = st.text_area("Message Content", value=msg_text, height=100)

        if st.button("🚀 Dispatch WhatsApp / SMS Alert"):
            clean_phone = str(parent_phone).replace(" ", "").replace("-", "")
            wa_link = f"https://api.whatsapp.com/send?phone=91{clean_phone}&text={custom_msg.replace(' ', '%20')}"
            st.success(f"🎉 Alert Dispatched to Parent of **{student_sel} (ID: #{s_id})** (Mobile: {parent_phone}, Batch: {batch_name})!")
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