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

# 3. COMPLETE LIGHT & CRISP THEME OVERRIDE FOR ALL STREAMLIT WIDGETS & TABLES
st.markdown("""
<style>
    /* NATIVE HEADER BAR MUST BE VISIBLE FOR TOGGLE ARROW */
    header[data-testid="stHeader"] {
        display: flex !important;
        visibility: visible !important;
        background-color: #ffffff !important;
        border-bottom: 1px solid #e2e8f0 !important;
        height: 3.5rem !important;
        z-index: 99999 !important;
    }

    /* ALWAYS KEEP SIDEBAR OPEN BUTTON VISIBLE IN TOP-LEFT WITH EMERALD STYLING */
    button[data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        background-color: #059669 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        margin-left: 10px !important;
        margin-top: 6px !important;
        box-shadow: 0 4px 10px rgba(5, 150, 105, 0.4) !important;
        border: 1px solid #047857 !important;
    }
    button[data-testid="stSidebarCollapsedControl"] * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* LIGHT & CRISP APP BACKGROUND */
    .stAppViewContainer, .main, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    
    /* GLOBAL HIGH CONTRAST TEXT */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #0f172a !important;
    }

    /* 1. SELECTBOXES & DROPDOWNS LIGHT THEME */
    div[data-baseweb="select"] > div, div[data-baseweb="select"] * {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-color: #cbd5e1 !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], div[data-baseweb="menu"] * {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    ul[role="listbox"], li[role="option"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    /* 2. TEXT INPUTS & TEXT AREAS LIGHT THEME */
    div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div, textarea, input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-color: #cbd5e1 !important;
    }

    /* 3. EXPANDERS & ACCORDIONS LIGHT THEME */
    .stExpander, div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
    }
    .stExpander *, div[data-testid="stExpander"] * {
        color: #0f172a !important;
    }

    /* 4. DATAFRAMES & TABLES LIGHT THEME */
    .stDataFrame, div[data-testid="stTable"], table, div[data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
    [data-testid="stTable"] th, [data-testid="stTable"] td, table th, table td {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-color: #cbd5e1 !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }

    /* 5. FILE UPLOADERS LIGHT THEME */
    div[data-testid="stFileUploader"], section[data-testid="stFileUploadDropzone"] {
        background-color: #ffffff !important;
        border: 2px dashed #059669 !important;
        color: #0f172a !important;
        border-radius: 10px !important;
    }
    section[data-testid="stFileUploadDropzone"] * {
        color: #0f172a !important;
    }

    /* 6. BUTTONS LIGHT THEME */
    .stButton > button, .stFormSubmitButton > button, button[kind="primary"], button[kind="secondary"] {
        background: linear-gradient(90deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3) !important;
    }
    .stButton > button *, .stFormSubmitButton > button * {
        color: #ffffff !important;
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
        margin-top: 10px;
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

    /* HIDE ONLY GITHUB & DEPLOY BUTTONS ON RIGHT SIDE */
    div[data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    .stAppDeployButton {
        display: none !important;
    }
    #MainMenu {
        visibility: hidden !important;
    }
    footer {
        visibility: hidden !important;
    }
    a[href*="github.com"] {
        display: none !important;
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