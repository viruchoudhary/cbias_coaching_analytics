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

# 2. Add root, src, and app directories to Python path (Linux Cloud Container Fix)
app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '..'))
src_dir = os.path.join(root_dir, 'src')

for d in [root_dir, src_dir, app_dir]:
    if d not in sys.path:
        sys.path.insert(0, d)

# Fail-safe module imports for Cloud Servers
try:
    from src.data_seeder import DataSeeder
    from src.auth import AuthManager
except Exception:
    try:
        from data_seeder import DataSeeder
        from auth import AuthManager
    except Exception as e:
        st.error(f"Module Import Error: {e}")

DataSeeder.seed_data()
AuthManager.seed_default_users()

# Initialize Authentication State
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# 3. HIGH-CONTRAST LIGHT THEME + BULLETPROOF BUTTON & SIDEBAR TOGGLE
st.markdown("""
<style>
    /* ALWAYS KEEP SIDEBAR TOGGLE BUTTON FIXED AT TOP-LEFT (EMERALD GREEN) */
    [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        background-color: #059669 !important;
        color: #ffffff !important;
        position: fixed !important;
        top: 14px !important;
        left: 14px !important;
        z-index: 9999999 !important;
        border-radius: 8px !important;
        padding: 6px 12px !important;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.5) !important;
        border: 1px solid #047857 !important;
    }
    [data-testid="stSidebarCollapsedControl"] * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* ALL BUTTONS (LOGIN, SUBMIT, ACTIONS) HIGH CONTRAST WHITE TEXT ON EMERALD */
    .stButton button, div.stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(90deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 20px !important;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3) !important;
    }
    .stButton button *, div.stButton > button *, .stFormSubmitButton > button * {
        color: #ffffff !important;
    }

    /* HIDE ONLY GITHUB FORK & DEPLOY BUTTONS IN TOP RIGHT */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    div[data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    #MainMenu {
        visibility: hidden !important;
    }
    footer {
        visibility: hidden !important;
    }
    .stAppDeployButton {
        display: none !important;
    }
    a[href*="github.com"] {
        display: none !important;
    }

    /* LIGHT & CRISP BACKGROUND */
    .stAppViewContainer {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    .main {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    
    /* HIGH CONTRAST TEXT */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #0f172a !important;
    }

    /* SIDEBAR LIGHT STYLING */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.05);
    }
    section[data-testid="stSidebar"] * {
        color: #0f172a !important;
    }

    /* MAIN HEADER GRADIENT */
    .main-header {
        background: linear-gradient(90deg, #059669 0%, #0284c7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 900;
        margin-bottom: 0.2rem;
    }

    /* TOP EXECUTIVE BANNER LIGHT */
    .top-banner {
        background: linear-gradient(135deg, #ecfdf5 0%, #e0f2fe 100%);
        border: 1px solid #a7f3d0;
        border-radius: 14px;
        padding: 18px 24px;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }
    .top-banner h2 {
        color: #047857 !important;
    }
    .top-banner p {
        color: #334155 !important;
    }

    /* ROLE BADGE */
    .role-badge-emerald {
        background: #059669;
        color: #ffffff !important;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    /* INPUT BOX & BUTTON READABILITY */
    .stTextInput input, .stSelectbox select {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
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

    # STRICT MANDATORY LOGIN ENFORCEMENT
    if not st.session_state.get('authenticated', False):
        st.sidebar.warning("🔒 Mandatory Security Check")
        st.sidebar.info("🔑 **Default System Accounts**:\n\n• Director: `director` / `director123`\n• Admin: `admin` / `admin123`\n• Accountant: `accountant` / `accountant123`\n• Teacher: `teacher` / `teacher123`")
        
        st.markdown("""
        <div class='top-banner'>
            <h2 style='margin:0; color:#047857;'>🔐 CBIAS Security & Access Control Portal</h2>
            <p style='margin:4px 0 0 0; color:#334155;'>System Status: <b style='color:#dc2626;'>● Authentication Required</b> | All Coaching Modules Are Locked Until Login.</p>
        </div>
        """, unsafe_allow_html=True)
        
        render_login_page()
        return

    # LOGGED IN USER PROFILE
    user_name = st.session_state.get('active_name', 'User')
    user_role = st.session_state.get('active_role', 'Admin')

    st.sidebar.markdown(f"👤 Logged in: **{user_name}**")
    st.sidebar.markdown(f"Active Role: <span class='role-badge-emerald'>{user_role}</span>", unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state['authenticated'] = False
        st.session_state['active_user'] = None
        st.session_state['active_role'] = None
        st.session_state['active_name'] = None
        st.rerun()

    st.sidebar.markdown("---")

    # Module Navigation (Unlocked ONLY after valid login)
    menu_options = {
        "📊 Executive Dashboard": render_dashboard_page,
        "🏢 Multi-Tenant SaaS Portal": render_tenants_page,
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
        "💡 Business Insights": render_insights_page,
        "🔑 Password & User Security": render_login_page
    }

    choice = st.sidebar.radio("Navigate Coaching BI", list(menu_options.keys()))

    # Top Executive Banner
    st.markdown(f"""
    <div class='top-banner'>
        <h2 style='margin:0; color:#047857;'>🎓 CBIAS Coaching Intelligence & Analytics System</h2>
        <p style='margin:4px 0 0 0; color:#334155;'>Active Module: <b>{choice}</b> | User: <b style='color:#059669;'>{user_name} ({user_role})</b> | Status: <b style='color:#059669;'>● Authenticated</b></p>
    </div>
    """, unsafe_allow_html=True)

    # Render selected view
    menu_options[choice]()

if __name__ == '__main__':
    main()