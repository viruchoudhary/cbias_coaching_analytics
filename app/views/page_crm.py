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

def render_crm_page():
    st.markdown("### 📞 Module 6: Lead Management & CRM Pipeline Portal")

    leads_df = DBManager.get_table_df("leads")

    with st.expander("📞 Register New Enquiry Lead", expanded=False):
        with st.form("new_lead_form"):
            lc1, lc2 = st.columns(2)
            l_name = lc1.text_input("Prospect Full Name *")
            l_phone = lc2.text_input("Mobile Phone Number *")
            l_source = lc1.selectbox("Lead Source Channel *", ["Instagram Ads", "Facebook Ads", "YouTube Ads", "Google Search", "Walk-in Enquiry", "Friend Referral"])
            l_status = lc2.selectbox("Pipeline Status *", ["New Lead", "Follow-up", "Converted Admission", "Closed Lost"])

            lead_sub = st.form_submit_button("✅ Register Enquiry Lead")
            if lead_sub and l_name and l_phone:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO leads (lead_name, phone, lead_source, status, enquiry_date) VALUES (?, ?, ?, ?, ?)",
                    (l_name, l_phone, l_source, l_status, str(datetime.now().date()))
                )
                conn.commit()
                conn.close()
                st.success(f"🎉 Lead **{l_name}** Registered via {l_source}!")
                st.rerun()

    st.markdown("---")
    st.subheader("📊 CRM Pipeline Conversion Funnel")
    if not leads_df.empty:
        new_cnt = len(leads_df[leads_df['status'] == 'New Lead'])
        fup_cnt = len(leads_df[leads_df['status'] == 'Follow-up'])
        conv_cnt = len(leads_df[leads_df['status'] == 'Converted Admission'])
        lost_cnt = len(leads_df[leads_df['status'] == 'Closed Lost'])

        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("📥 New Leads", f"{new_cnt:,}")
        mc2.metric("📞 In Follow-up", f"{fup_cnt:,}")
        mc3.metric("🎉 Converted Admissions", f"{conv_cnt:,}", f"Rate: {round(conv_cnt/len(leads_df)*100, 1)}%")
        mc4.metric("❌ Closed Lost", f"{lost_cnt:,}")

    st.markdown("---")
    st.subheader("📋 Master CRM Enquiry Directory")
    ls_filter = st.selectbox("Filter Lead Source Channel:", ["All", "Instagram Ads", "Facebook Ads", "YouTube Ads", "Google Search", "Walk-in Enquiry", "Friend Referral"])

    filtered_leads = leads_df.copy()
    if ls_filter != "All":
        filtered_leads = filtered_leads[filtered_leads['lead_source'] == ls_filter]

    st.dataframe(filtered_leads, use_container_width=True)

if __name__ == '__main__':
    render_crm_page()
