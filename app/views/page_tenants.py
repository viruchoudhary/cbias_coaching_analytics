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

    DBManager.init_db()
    tenants_df = DBManager.get_table_df("tenants")

    t1, t2 = st.tabs(["➕ Onboard New Coaching Institute", "📋 Registered Tenant Coaching Network"])

    # 1. Register New Tenant Coaching
    with t1:
        st.subheader("➕ Onboard Coaching Client (Multi-Tenant SaaS)")
        with st.form("new_tenant_form"):
            tc1, tc2 = st.columns(2)
            c_name = tc1.text_input("Coaching Institute Name *", placeholder="e.g. Ramdev Bishnoi Classes")
            d_name = tc2.text_input("Director / Owner Name *", placeholder="e.g. Ramdev Bishnoi")
            c_phone = tc1.text_input("Mobile / WhatsApp *", placeholder="9876543210")
            c_city = tc2.text_input("City / Location *", placeholder="e.g. Jodhpur")
            sub_tier = st.selectbox("Assign Subscription Tier", ["Professional (₹1,999/mo)", "Standard (₹999/mo)", "Basic (₹499/mo)"])

            t_sub = st.form_submit_button("🚀 Onboard Coaching Institute")
            if t_sub and c_name and d_name and c_phone:
                t_count = len(tenants_df) + 1
                t_id = f"TNT-{t_count:03d}"
                plan_name = sub_tier.split(" (")[0]
                onboard_date = str(datetime.now().date())

                conn = DBManager.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO tenants (tenant_id, institute_name, director, phone, city, plan, status, onboard_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (t_id, c_name, d_name, c_phone, c_city if c_city else "Jaipur", plan_name, "Active", onboard_date)
                )
                conn.commit()
                conn.close()

                st.success(f"🎉 SUCCESS! **{c_name}** ({c_city}) onboarded as Tenant **{t_id}**! Data Isolation Enabled.")
                st.rerun()

    # 2. Network Directory
    with t2:
        st.subheader("🌐 Active Multi-Tenant Coaching Network")
        if not tenants_df.empty:
            st.dataframe(tenants_df, use_container_width=True)
        else:
            st.info("No tenants registered yet.")

if __name__ == '__main__':
    render_tenants_page()