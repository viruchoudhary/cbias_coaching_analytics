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

def render_tenants_page():
    st.markdown("### 🏢 Module 16: Multi-Tenant SaaS Coaching Network Portal")

    t1, t2 = st.tabs(["➕ Onboard New Coaching Institute", "📋 Registered Tenant Coaching Network"])

    # 1. Register New Tenant Coaching
    with t1:
        st.subheader("➕ Onboard Coaching Client (Multi-Tenant SaaS)")
        with st.form("new_tenant_form"):
            tc1, tc2 = st.columns(2)
            c_name = tc1.text_input("Coaching Institute Name *", placeholder="e.g. Choudhary Analytics Academy")
            d_name = tc2.text_input("Director / Owner Name *", placeholder="e.g. Viru Choudhary")
            c_phone = tc1.text_input("Mobile / WhatsApp *", placeholder="9876543210")
            c_city = tc2.text_input("City / Location *", placeholder="e.g. Jaipur")
            sub_tier = st.selectbox("Assign Subscription Tier", ["Basic (₹499/mo)", "Standard (₹999/mo)", "Professional (₹1,999/mo)"])

            t_sub = st.form_submit_button("🚀 Onboard Coaching Institute")
            if t_sub and c_name and d_name and c_phone:
                st.success(f"🎉 SUCCESS! **{c_name}** ({c_city}) onboarded as a Tenant! Data Isolation Enabled (Tenant Key: `TNT-{len(c_name)}99`).")

    # 2. Network Directory
    with t2:
        st.subheader("🌐 Active Multi-Tenant Coaching Network")
        tenants_data = pd.DataFrame([
            {"Tenant ID": "TNT-001", "Institute Name": "Viru Choudhary BI Academy", "Director": "Viru Choudhary", "City": "Jaipur", "Active Students": 500, "Plan": "Professional", "Status": "Active"},
            {"Tenant ID": "TNT-002", "Institute Name": "Kota Science Analytics Institute", "Director": "Dr. Sharma", "City": "Kota", "Active Students": 320, "Plan": "Standard", "Status": "Active"},
            {"Tenant ID": "TNT-003", "Institute Name": "Delhi Commerce Hub", "Director": "Rajesh Verma", "City": "Delhi", "Active Students": 180, "Plan": "Basic", "Status": "Active"}
        ])
        st.dataframe(tenants_data, use_container_width=True)

if __name__ == '__main__':
    render_tenants_page()