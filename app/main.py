import streamlit as st
import pandas as pd
import os
import sys

# 1. Set Streamlit Page Config (Must be very first command)
st.set_page_config(
    page_title="CBIAS - Coaching Business Intelligence System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Add root directory to Python path (Fail-safe for Linux Cloud Containers)
app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '..'))
sys.path.insert(0, root_dir)
sys.path.insert(0, app_dir)

# Auto-seed database & default hashed users with fail-safe imports
try:
    from src.data_seeder import DataSeeder
except Exception:
    from data_seeder import DataSeeder

try:
    from src.auth import AuthManager
except Exception:
    from auth import AuthManager

DataSeeder.seed_data()
AuthManager.seed_default_users()

# 3. Futuristic Cyberpunk 3D Styling
st.markdown("""
<style>
    .main {
        background-color: #030712;
        color: #f3f4f6;
    }
    .stAppViewContainer {
        background: radial-gradient(circle at 50% 0%, #064e3b 0%, #022c22 40%, #030712 90%);
    }
    .main-header {
        background: linear-gradient(90deg, #10b981 0%, #06b6d4 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.4rem;
        font-weight: 900;
        margin-bottom: 0.2rem;
    }
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9) !important;
        backdrop-filter: blur(24px);
        border-right: 1px solid rgba(16, 185, 129, 0.2);
    }
    .top-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 16px;
        padding: 20px 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .role-badge-emerald {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.5);
    }
</style>
""", unsafe_allow_html=True)

from views.page_login import render_login_page
from views.page_dashboard import render_dashboard_page
from views.page_students import render_students_page
from views.page_courses import render_courses_page
from views.page_fees import render_fees_page
from views.page_attendance import render_attendance_page
from views.page_tests import render_tests_page
from views.page_crm import render_crm_page
from views.page_marketing import render_marketing_page
from views.page_faculty import render_faculty_page
from views.page_expenses import render_expenses_page
from views.page_pnl import render_pnl_page
from views.page_risk import render_risk_page
from views.page_insights import render_insights_page
from views.page_notifications import render_notifications_page
from views.page_ai_advisor import render_ai_advisor_page
from views.page_tenants import render_tenants_page

def main():
    st.sidebar.markdown("<h1 class='main-header'>🎓 CBIAS 3D</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("*Coaching ERP & Analytics System v3.0*")
    st.sidebar.markdown("---")

    # Role Selection System
    st.sidebar.subheader("🔐 Current User Persona")
    user_role = st.sidebar.selectbox(
        "Active Role Access:",
        ["👑 Owner / Director", "🛠️ Admin", "💰 Accountant", "📞 Counsellor", "👨‍🏫 Faculty / Teacher"]
    )
    st.sidebar.markdown(f"Active Role: <span class='role-badge-emerald'>{user_role}</span>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    # Module Navigation
    menu_options = {
        "🔐 Security & Login Portal": render_login_page,
        "🏢 Multi-Tenant SaaS Portal": render_tenants_page,
        "📊 Executive Dashboard": render_dashboard_page,
        "👥 Student Master": render_students_page,
        "📚 Courses & Batches": render_courses_page,
        "💰 Fee Ledger & Receipts": render_fees_page,
        "📝 Attendance Alerts": render_attendance_page,
        "🏆 Test & Examinations": render_tests_page,
        "🔔 Parent WhatsApp Alerts": render_notifications_page,
        "🤖 AI Coaching Advisor": render_ai_advisor_page,
        "📞 Lead & CRM Pipeline": render_crm_page,
        "📈 Marketing ROI": render_marketing_page,
        "👨‍🏫 Faculty Analytics": render_faculty_page,
        "💸 Expense Management": render_expenses_page,
        "💵 Real-Time P&L": render_pnl_page,
        "⚠️ Student Risk Matrix": render_risk_page,
        "💡 Business Insights": render_insights_page
    }

    choice = st.sidebar.radio("Navigate Coaching BI", list(menu_options.keys()))

    # Top Executive Banner
    st.markdown(f"""
    <div class='top-banner'>
        <h2 style='margin:0; color:#10b981;'>🎓 CBIAS Coaching Intelligence & Analytics System</h2>
        <p style='margin:4px 0 0 0; color:#9ca3af;'>Active Module: <b>{choice}</b> | Persona Access: <b style='color:#10b981;'>{user_role}</b> | System Status: <b style='color:#34d399;'>● Live Online</b></p>
    </div>
    """, unsafe_allow_html=True)

    # Render selected view
    menu_options[choice]()

if __name__ == '__main__':
    main()