"""
app.py - B.Tech Student Performance Advisor
===========================================
A Rule-Based AI System for Academic Performance Analysis and Personalized Student Guidance.
- Allows student to select either:
  1. 📋 Subject-Wise Academic Marks (auto-calculates averages)
  2. 📊 Overall Academic Marks (direct entry)
- In 1st Year 1st Semester: evaluates purely on Mid Exam marks (0-30) since semester exams have not yet occurred.
- In subsequent semesters: evaluates Mid (0-30) and Semester (0-70) marks (0-100 total).
- Generates short, concise recommendations and targeted study roadmaps.
"""

import importlib
import streamlit as st
import rules
importlib.reload(rules)

# ------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & LIGHT THEME STYLING
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="B.Tech Student Performance Advisor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom light-theme CSS with clean typography, high readability, and responsive cards
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
        background-color: #F8FAFC;
    }

    /* Completely hide Streamlit Header, Toolbar, Deploy button, and Three Dots Menu */
    header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    .stAppDeployButton, [data-testid="stAppDeployButton"] {
        display: none !important;
        visibility: hidden !important;
    }
    footer {
        display: none !important;
        visibility: hidden !important;
    }

    /* Completely hide top-left sidebar control & sidebar navigation */
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* =========================================================================
       STRICT FORCED LIGHT THEME (Overrides Dark Mode on All Devices & Accounts)
       ========================================================================= */
    :root, [data-theme="dark"], [data-theme="light"], body {
        color-scheme: light !important;
        --background-color: #F8FAFC !important;
        --secondary-background-color: #FFFFFF !important;
        --text-color: #0F172A !important;
        --primary-color: #1D4ED8 !important;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }

    /* Main Container */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
        max-width: 1120px;
        background-color: #F8FAFC !important;
    }

    /* Force all text in labels and markdown to light-theme colors */
    [data-testid="stWidgetLabel"] p, label, .stMarkdown p, .stMarkdown span {
        color: #1E293B !important;
    }

    /* Dropdown popover and menu light background */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
    }

    /* Header Banner */
    .app-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 50%, #3B82F6 100%);
        color: white;
        padding: 2rem 2.2rem;
        border-radius: 14px;
        box-shadow: 0 8px 24px -4px rgba(37, 99, 235, 0.25);
        margin-bottom: 1.8rem;
    }
    .app-header h1 {
        color: #FFFFFF !important;
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
    }
    .app-header p {
        color: #DBEAFE !important;
        font-size: 1.05rem;
        margin: 0;
        line-height: 1.45;
        font-weight: 400;
    }

    /* Content Cards */
    .card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.3rem;
        box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.3rem;
    }

    /* Section Headings */
    .section-title {
        color: #1E293B;
        font-size: 1.22rem;
        font-weight: 800;
        margin-bottom: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 0.55rem;
    }

    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #1E3A8A;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #64748B;
        margin-top: 0.3rem;
        font-weight: 600;
    }

    /* Clear Structured Advice Cards */
    .advice-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #2563EB;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.55rem;
        box-shadow: 0 2px 5px rgba(15, 23, 42, 0.03);
    }

    /* Target Improvement Box */
    .target-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 1.5px solid #86EFAC;
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1.3rem;
    }
    .target-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #166534;
        margin-bottom: 0.35rem;
    }
    .target-body {
        font-size: 0.93rem;
        color: #14532D;
        line-height: 1.55;
    }

    /* Subject Breakdown Row */
    .subject-row {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Study Plan Cards */
    .plan-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 0.9rem;
        margin-top: 0.85rem;
    }
    .plan-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .plan-box h4 {
        margin: 0;
        font-size: 0.78rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.03em;
    }
    .plan-box p {
        margin: 0.35rem 0 0 0;
        font-size: 1.2rem;
        font-weight: 800;
        color: #1E3A8A;
    }

    /* Category Banner */
    .category-banner {
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.3rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .footer-note {
        text-align: center;
        color: #64748B;
        font-size: 0.85rem;
        margin-top: 2.5rem;
        padding-top: 1.2rem;
        border-top: 1px solid #E2E8F0;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        letter-spacing: 0.01em;
        padding: 0.65rem 1.2rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 12px -2px rgba(37, 99, 235, 0.35) !important;
    }
    .stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #334155 !important;
        border: 1.5px solid #CBD5E1 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #F1F5F9 !important;
        color: #1E3A8A !important;
        border-color: #94A3B8 !important;
    }

    /* Highlighted Input Section Cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 14px !important;
        padding: 1.3rem 1.5rem !important;
        box-shadow: 0 4px 14px -2px rgba(15, 23, 42, 0.05), 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        margin-bottom: 1.3rem !important;
        transition: all 0.25s ease-in-out !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #93C5FD !important;
        box-shadow: 0 6px 20px -2px rgba(37, 99, 235, 0.09) !important;
    }

    /* Highlighted Form Controls (Inputs, Selectboxes, Number Inputs) */
    div[data-baseweb="input"] {
        border-radius: 9px !important;
        border: 1.5px solid #CBD5E1 !important;
        background-color: #F8FAFC !important;
        transition: all 0.2s ease !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #2563EB !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.18) !important;
    }
    div[data-baseweb="select"] > div {
        border-radius: 9px !important;
        border: 1.5px solid #CBD5E1 !important;
        background-color: #F8FAFC !important;
        transition: all 0.2s ease !important;
    }
    div[data-baseweb="select"]:focus-within > div {
        border-color: #2563EB !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.18) !important;
    }
    label[data-testid="stWidgetLabel"] p {
        font-weight: 700 !important;
        color: #1E293B !important;
        font-size: 0.92rem !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 2. SESSION STATE MANAGEMENT
# ------------------------------------------------------------------------------
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "branch" not in st.session_state:
    st.session_state.branch = rules.BRANCH_OPTIONS[0]
if "year" not in st.session_state:
    st.session_state.year = rules.YEAR_OPTIONS[0]
if "semester" not in st.session_state:
    st.session_state.semester = rules.SEMESTER_OPTIONS[0]
if "marks_entry_mode" not in st.session_state:
    st.session_state.marks_entry_mode = "Subject-Wise Academic Marks"
if "mid_marks" not in st.session_state:
    st.session_state.mid_marks = 20.0
if "semester_marks" not in st.session_state:
    st.session_state.semester_marks = 45.0
if "sgpa" not in st.session_state:
    st.session_state.sgpa = 7.5
if "cgpa" not in st.session_state:
    st.session_state.cgpa = 7.2
if "attendance" not in st.session_state:
    st.session_state.attendance = 75.0
if "study_performance" not in st.session_state:
    st.session_state.study_performance = "Good"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "No major difficulty"
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "num_subjects" not in st.session_state:
    st.session_state.num_subjects = 5


def reset_all_fields():
    """Reset all student fields and return to initial state."""
    st.session_state.student_name = ""
    st.session_state.branch = rules.BRANCH_OPTIONS[0]
    st.session_state.year = rules.YEAR_OPTIONS[0]
    st.session_state.semester = rules.SEMESTER_OPTIONS[0]
    st.session_state.marks_entry_mode = "Subject-Wise Academic Marks"
    st.session_state.mid_marks = 20.0
    st.session_state.semester_marks = 45.0
    st.session_state.sgpa = 7.5
    st.session_state.cgpa = 7.2
    st.session_state.attendance = 75.0
    st.session_state.study_performance = "Good"
    st.session_state.difficulty = "No major difficulty"
    st.session_state.analyzed = False
    st.session_state.num_subjects = 5


# ------------------------------------------------------------------------------
# 3. MAIN HEADER
# ------------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1>🎓 B.Tech Student Performance Advisor</h1>
        <p>“Explainable Rule-Based AI Engine for Academic Performance Diagnostics & Career Roadmaps”</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------------------
# 4. CLEAN INPUT FORM
# ------------------------------------------------------------------------------

# Section 1: Student Profile
with st.container(border=True):
    st.markdown('<div class="section-title">👨‍🎓 Student Profile</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.5, 1.5])

    with c1:
        student_name = st.text_input(
            "Student Name *",
            value=st.session_state.student_name,
            placeholder="Enter Student Name",
            help="Enter the student's full name"
        )
    with c2:
        branch_idx = rules.BRANCH_OPTIONS.index(st.session_state.branch) if st.session_state.branch in rules.BRANCH_OPTIONS else 0
        branch = st.selectbox(
            "B.Tech Branch *",
            options=rules.BRANCH_OPTIONS,
            index=branch_idx
        )

    c3, c4 = st.columns(2)
    with c3:
        year_idx = rules.YEAR_OPTIONS.index(st.session_state.year) if st.session_state.year in rules.YEAR_OPTIONS else 0
        year = st.selectbox("Current Year *", options=rules.YEAR_OPTIONS, index=year_idx)
    with c4:
        sem_idx = rules.SEMESTER_OPTIONS.index(st.session_state.semester) if st.session_state.semester in rules.SEMESTER_OPTIONS else 0
        semester = st.selectbox("Current Semester *", options=rules.SEMESTER_OPTIONS, index=sem_idx)

# Check if student is in 1st Year 1st Semester
is_first_year_first_sem = ("1st" in year and "1st" in semester)

# Section 2: Academic Examination Scores (With Choice between Subject-Wise and Overall)
with st.container(border=True):
    st.markdown('<div class="section-title">📚 Academic Examination Scores</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 0.92rem; margin-top: -0.4rem; margin-bottom: 0.75rem;'>Choose your preferred marks entry method:</p>", unsafe_allow_html=True)

    col_btn_subj, col_btn_overall = st.columns(2)
    is_subject_wise = (st.session_state.marks_entry_mode == "Subject-Wise Academic Marks")
    is_overall = (st.session_state.marks_entry_mode == "Overall Academic Marks")

    with col_btn_subj:
        if st.button(
            "✓ 📚 Subject-Wise Academic Marks" if is_subject_wise else "📚 Subject-Wise Academic Marks",
            type="primary" if is_subject_wise else "secondary",
            use_container_width=True,
            key="btn_mode_subject_wise"
        ):
            if st.session_state.marks_entry_mode != "Subject-Wise Academic Marks":
                st.session_state.marks_entry_mode = "Subject-Wise Academic Marks"
                st.rerun()

    with col_btn_overall:
        if st.button(
            "✓ 📊 Overall Academic Marks" if is_overall else "📊 Overall Academic Marks",
            type="primary" if is_overall else "secondary",
            use_container_width=True,
            key="btn_mode_overall_marks"
        ):
            if st.session_state.marks_entry_mode != "Overall Academic Marks":
                st.session_state.marks_entry_mode = "Overall Academic Marks"
                st.rerun()

    selected_mode = st.session_state.marks_entry_mode

    if is_subject_wise:
        st.markdown(
            """
            <div style="background: #EFF6FF; border: 1.5px solid #BFDBFE; border-radius: 8px; padding: 0.55rem 0.95rem; margin-top: 0.4rem; margin-bottom: 1.1rem; display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.88rem; color: #1E3A8A; font-weight: 600;">
                    ✓ Active Mode: <b>Subject-Wise Academic Marks</b> (Enter individual subject Mid marks)
                </span>
                <span style="font-size: 0.76rem; background: #DBEAFE; color: #1D4ED8; font-weight: 800; padding: 2px 10px; border-radius: 12px; letter-spacing: 0.03em;">SUBJECT-WISE</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background: #EFF6FF; border: 1.5px solid #BFDBFE; border-radius: 8px; padding: 0.55rem 0.95rem; margin-top: 0.4rem; margin-bottom: 1.1rem; display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.88rem; color: #1E3A8A; font-weight: 600;">
                    ✓ Active Mode: <b>Overall Academic Marks</b> (Enter SGPA & CGPA scores)
                </span>
                <span style="font-size: 0.76rem; background: #DBEAFE; color: #1D4ED8; font-weight: 800; padding: 2px 10px; border-radius: 12px; letter-spacing: 0.03em;">OVERALL</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    sgpa = 0.0
    cgpa = 0.0

    # --------------------------------------------------------------------------
    # MODE 1: SUBJECT-WISE ACADEMIC MARKS
    # --------------------------------------------------------------------------
    if selected_mode == "Subject-Wise Academic Marks":
        col_sub_cnt, col_sub_info = st.columns([1, 2.5])
        with col_sub_cnt:
            num_subjects = st.selectbox(
                "Number of Subjects *",
                options=[3, 4, 5, 6, 7],
                index=[3, 4, 5, 6, 7].index(st.session_state.num_subjects) if st.session_state.num_subjects in [3, 4, 5, 6, 7] else 2,
                help="Select how many theory subjects you have in the current semester"
            )
            st.session_state.num_subjects = num_subjects

        with col_sub_info:
            st.info("ℹ️ Enter each subject's **Mid Marks (0 – 30)**. The system will automatically calculate your average internal score and evaluate your performance.")

        default_sub_list = rules.get_default_subjects(branch, year)

        # Subject Input Grid (Mid Marks Only - Semester Marks Removed)
        subject_scores = []
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        for i in range(num_subjects):
            default_sub_name = default_sub_list[i] if i < len(default_sub_list) else f"Subject {i+1}"
            c_sname, c_smid = st.columns([2.5, 1.5])
            with c_sname:
                sub_name = st.text_input(
                    f"Subject {i+1} Name",
                    value=default_sub_name,
                    key=f"subj_name_{i}",
                    placeholder=f"e.g. Subject {i+1}"
                )
            with c_smid:
                sub_mid = st.number_input(
                    f"Mid Marks (0 – 30) *",
                    min_value=0.0,
                    max_value=30.0,
                    value=20.0,
                    step=0.5,
                    key=f"subj_mid_{i}",
                    help="Internal continuous assessment score (Maximum 30)"
                )
            subject_scores.append({
                "name": sub_name.strip() if sub_name.strip() else f"Subject {i+1}",
                "mid": sub_mid,
                "sem": 0.0,
                "total": sub_mid
            })

        # Automatic Calculations from Subject Mid Marks
        all_mids = [s["mid"] for s in subject_scores]
        calc_avg_mid = round(sum(all_mids) / len(all_mids), 2) if all_mids else 0.0
        calc_avg_sem = 0.0
        calc_total = calc_avg_mid
        calc_pct = round((calc_avg_mid / 30.0) * 100.0, 2)
        tot_class = rules.classify_performance(calc_pct)

        st.markdown(
            f"""
            <div style="background: #F8FAFC; border: 1.5px solid #CBD5E1; border-radius: 12px; padding: 1.1rem 1.4rem; margin-top: 1rem; margin-bottom: 0.5rem;">
                <div style="font-size: 0.82rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 0.4rem;">
                    📊 Automatically Calculated Internal Averages ({num_subjects} Subjects)
                </div>
                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem;">
                    <div>
                        <span style="font-size: 0.8rem; color: #64748B;">Average Mid Score:</span>
                        <div style="font-size: 1.6rem; font-weight: 800; color: #1E3A8A;">{calc_avg_mid} <span style="font-size: 0.95rem; color: #64748B;">/ 30</span></div>
                    </div>
                    <div>
                        <span style="font-size: 0.8rem; color: #64748B;">Internal Equivalent:</span>
                        <div style="font-size: 1.6rem; font-weight: 800; color: #2563EB;">{calc_pct}%</div>
                    </div>
                    <div>
                        <span style="font-size: 0.8rem; color: #64748B;">Academic Standing:</span>
                        <div style="font-size: 1.3rem; font-weight: 800; color: {tot_class['color']};">{tot_class['badge']}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------------------------
    # MODE 2: OVERALL ACADEMIC MARKS (SGPA & CGPA)
    # --------------------------------------------------------------------------
    else:
        subject_scores = []

        col_sgpa, col_cgpa, col_tot = st.columns([1.1, 1.1, 1.2])

        with col_sgpa:
            sgpa = st.number_input(
                "Current Semester SGPA (0.00 – 10.00) *",
                min_value=0.0,
                max_value=10.0,
                value=float(st.session_state.sgpa),
                step=0.05,
                format="%.2f",
                help="Current Semester Grade Point Average on a 10.0 scale"
            )


        with col_cgpa:
            cgpa = st.number_input(
                "Cumulative CGPA (0.00 – 10.00) *",
                min_value=0.0,
                max_value=10.0,
                value=float(st.session_state.cgpa),
                step=0.05,
                format="%.2f",
                help="Overall Cumulative Grade Point Average across all semesters"
            )

        calc_avg_mid = 0.0
        calc_avg_sem = 0.0
        calc_total = cgpa
        calc_pct = round(cgpa * 10.0, 1)
        tot_class = rules.classify_performance(calc_pct)

        # Trajectory indicator badge
        if sgpa >= cgpa + 0.3:
            trend_badge = f"📈 Upward Trend (+{sgpa - cgpa:.2f})"
            trend_color = "#16A34A"
        elif sgpa <= cgpa - 0.5:
            trend_badge = f"⚠️ Semester Dip ({sgpa - cgpa:.2f})"
            trend_color = "#DC2626"
        else:
            trend_badge = "⚖️ Steady Trajectory"
            trend_color = "#2563EB"

        with col_tot:
            st.markdown(
                f"""
                <div style="background: {tot_class['bg_color']}; border: 1.5px solid {tot_class['color']}; border-radius: 10px; padding: 0.95rem 1.1rem; text-align: center; margin-top: 0.2rem;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: {tot_class['color']}; text-transform: uppercase;">Overall Cumulative Standing</div>
                    <div style="font-size: 1.85rem; font-weight: 800; color: {tot_class['color']}; margin: 0.15rem 0;">{cgpa:.2f} <span style="font-size: 1.0rem; color: #64748B;">/ 10.0</span></div>
                    <div style="font-size: 0.82rem; font-weight: 700; color: #1E293B;">{tot_class['badge']} ({calc_pct}%)</div>
                    <div style="font-size: 0.74rem; font-weight: 700; color: {trend_color}; margin-top: 0.25rem;">{trend_badge}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# Section 3: Attendance & Study Performance
with st.container(border=True):
    st.markdown('<div class="section-title">🕐 Attendance & Daily Study Habits</div>', unsafe_allow_html=True)
    col_att, col_std = st.columns([1.2, 1.2])

    with col_att:
        attendance = st.number_input(
            "Attendance Percentage (0 – 100%) *",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.attendance),
            step=1.0,
            help="Classroom & laboratory attendance percentage"
        )
        att_c_quick = rules.classify_attendance(attendance)
        st.caption(f"Status: **{att_c_quick['status']} Attendance** ({attendance:.1f}%)")

    with col_std:
        std_idx = rules.PERFORMANCE_LEVELS.index(st.session_state.study_performance) if st.session_state.study_performance in rules.PERFORMANCE_LEVELS else 1
        study_performance = st.selectbox(
            "Daily Study Habits *",
            options=rules.PERFORMANCE_LEVELS,
            index=std_idx,
            help="Regularity of daily self-study and conceptual revision"
        )
        st.caption(f"Selected routine: **{study_performance}**")

# Default difficulty (challenge option removed from form as requested)
difficulty = "No major difficulty"

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 5. ACTION BUTTON & VALIDATION
# ------------------------------------------------------------------------------
analyze_clicked = st.button("🔍 Analyze My Performance & Generate Full Guidance", type="primary", use_container_width=True)

if analyze_clicked:
    st.session_state.student_name = student_name
    st.session_state.branch = branch
    st.session_state.year = year
    st.session_state.semester = semester
    st.session_state.mid_marks = calc_avg_mid
    st.session_state.semester_marks = calc_avg_sem
    st.session_state.sgpa = sgpa if selected_mode == "Overall Academic Marks" else 0.0
    st.session_state.cgpa = cgpa if selected_mode == "Overall Academic Marks" else 0.0
    st.session_state.attendance = attendance
    st.session_state.study_performance = study_performance
    st.session_state.difficulty = difficulty
    st.session_state.analyzed = True

# Validation checks
validation_errors = []
if st.session_state.analyzed:
    if not student_name or not student_name.strip():
        validation_errors.append("Student Name cannot be empty.")
    if selected_mode == "Subject-Wise Academic Marks":
        if calc_avg_mid < 0 or calc_avg_mid > 30:
            validation_errors.append("Mid Marks must be between 0 and 30.")
    else:
        if sgpa < 0.0 or sgpa > 10.0:
            validation_errors.append("Current Semester SGPA must be between 0.0 and 10.0.")
        if cgpa < 0.0 or cgpa > 10.0:
            validation_errors.append("Cumulative CGPA must be between 0.0 and 10.0.")
    if attendance < 0 or attendance > 100:
        validation_errors.append("Attendance must be between 0 and 100%.")

if validation_errors:
    for err in validation_errors:
        st.error(f"❌ {err}")
    st.stop()


# ------------------------------------------------------------------------------
# 6. INFERENCE EXECUTION & COMPREHENSIVE RESULTS PRESENTATION
# ------------------------------------------------------------------------------
if st.session_state.analyzed and not validation_errors:
    results = rules.analyze_performance(
        student_name=student_name.strip(),
        branch=branch,
        year=year,
        semester=semester,
        mid_marks=calc_avg_mid if selected_mode == "Subject-Wise Academic Marks" else 0.0,
        semester_marks=calc_avg_sem if selected_mode == "Subject-Wise Academic Marks" else 0.0,
        attendance=attendance,
        study_performance=study_performance,
        difficulty=difficulty,
        subject_scores=subject_scores if selected_mode == "Subject-Wise Academic Marks" else None,
        sgpa=sgpa if selected_mode == "Overall Academic Marks" else 0.0,
        cgpa=cgpa if selected_mode == "Overall Academic Marks" else 0.0
    )

    st.markdown("---")

    # 1. PERFORMANCE DASHBOARD
    st.markdown('<div class="section-title">📊 Comprehensive Performance Dashboard</div>', unsafe_allow_html=True)

    # Student Summary Banner
    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1.25rem;">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; align-items: center;">
                <div>
                    <span style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Student Name</span>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #0F172A;">{results['student_info']['name']}</div>
                </div>
                <div>
                    <span style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Department & Branch</span>
                    <div style="font-size: 1.1rem; font-weight: 800; color: #1E3A8A;">{results['student_info']['branch']}</div>
                </div>
                <div>
                    <span style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Academic Progression</span>
                    <div style="font-size: 1.1rem; font-weight: 800; color: #2563EB;">{results['student_info']['year']} • {results['student_info']['semester']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Core Metric Cards
    is_cgpa_mode = results['metrics'].get('is_cgpa_mode', False)
    if is_cgpa_mode:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">🎓 Semester SGPA</div>
                    <div class="metric-value">{results['metrics']['sgpa']:.2f} <span style="font-size: 1rem; color: #64748B;">/ 10.0</span></div>
                    <div class="metric-sub">Current Semester GPA</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m2:
            st.markdown(
                f"""
                <div class="metric-card" style="border: 2px solid #BFDBFE; background: #F8FAFC;">
                    <div class="metric-label">🏆 Cumulative CGPA</div>
                    <div class="metric-value" style="color: #1D4ED8;">{results['metrics']['cgpa']:.2f} <span style="font-size: 1rem; color: #64748B;">/ 10.0</span></div>
                    <div class="metric-sub">Degree Cumulative GPA</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">📊 Equivalent Score</div>
                    <div class="metric-value" style="color: #2563EB;">{results['metrics']['scaled_percentage']}%</div>
                    <div class="metric-sub">AICTE / University Scale</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m4:
            att_c = results['attendance_category']
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">🕐 Attendance</div>
                    <div class="metric-value" style="color: {att_c['color']};">{results['metrics']['attendance']}%</div>
                    <div class="metric-sub">{att_c['status']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    elif is_first_year_first_sem or (st.session_state.marks_entry_mode == "Subject-Wise Academic Marks"):
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            mid_sub_text = f"{len(subject_scores)} Subjects Avg" if subject_scores else "Internal Mid Exam"
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">📘 Mid Exam</div>
                    <div class="metric-value">{results['metrics']['mid_marks']} <span style="font-size: 1rem; color: #64748B;">/ 30</span></div>
                    <div class="metric-sub">{mid_sub_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m2:
            sem_sub = "1st Semester in Progress" if is_first_year_first_sem else "End-Term Not Evaluated"
            st.markdown(
                f"""
                <div class="metric-card" style="background: #F8FAFC;">
                    <div class="metric-label">🎓 Semester Exam</div>
                    <div class="metric-value" style="font-size: 1.05rem; color: #64748B; padding-top: 0.4rem;">Mid Assessment Only</div>
                    <div class="metric-sub">{sem_sub}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m3:
            st.markdown(
                f"""
                <div class="metric-card" style="border: 2px solid #BFDBFE; background: #F8FAFC;">
                    <div class="metric-label">📊 Internal Standing</div>
                    <div class="metric-value" style="color: #1D4ED8;">{results['metrics']['mid_marks']} <span style="font-size: 1rem; color: #64748B;">/ 30</span></div>
                    <div class="metric-sub">{results['metrics']['scaled_percentage']}% Scaled Score</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m4:
            att_c = results['attendance_category']
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">🕐 Attendance</div>
                    <div class="metric-value" style="color: {att_c['color']};">{results['metrics']['attendance']}%</div>
                    <div class="metric-sub">{att_c['status']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        mid_sub_text = f"{len(subject_scores)} Subjects Avg" if subject_scores else "Weight: 30%"
        sem_sub_text = f"{len(subject_scores)} Subjects Avg" if subject_scores else "Weight: 70%"

        with col_m1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">📘 Mid Exam</div>
                    <div class="metric-value">{results['metrics']['mid_marks']} <span style="font-size: 1rem; color: #64748B;">/ 30</span></div>
                    <div class="metric-sub">{mid_sub_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">🎓 Semester Exam</div>
                    <div class="metric-value">{results['metrics']['semester_marks']} <span style="font-size: 1rem; color: #64748B;">/ 70</span></div>
                    <div class="metric-sub">{sem_sub_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m3:
            st.markdown(
                f"""
                <div class="metric-card" style="border: 2px solid #BFDBFE; background: #F8FAFC;">
                    <div class="metric-label">📊 Overall Score</div>
                    <div class="metric-value" style="color: #1D4ED8;">{results['metrics']['total_marks']} <span style="font-size: 1rem; color: #64748B;">/ 100</span></div>
                    <div class="metric-sub">Mid + End Semester</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m4:
            att_c = results['attendance_category']
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">🕐 Attendance</div>
                    <div class="metric-value" style="color: {att_c['color']};">{results['metrics']['attendance']}%</div>
                    <div class="metric-sub">{att_c['status']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Academic Classification Banner
    perf = results['performance_category']
    st.markdown(
        f"""
        <div class="category-banner" style="background-color: {perf['bg_color']}; border: 1.5px solid {perf['color']}; margin-top: 1rem;">
            <div>
                <span style="font-size: 0.82rem; text-transform: uppercase; font-weight: 700; color: {perf['color']};">Standing Classification</span>
                <div style="font-size: 1.6rem; font-weight: 800; color: {perf['color']}; margin: 0.15rem 0;">{perf['badge']}</div>
                <div style="font-size: 0.95rem; color: #1E293B; font-weight: 500;">{perf['summary']}</div>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 2.3rem;">{perf['badge'].split()[0]}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Attendance Warning Notice (if < 75%)
    if results['metrics']['attendance'] < 75:
        st.warning(
            f"⚠️ **ATTENDANCE ACTION REQUIRED:** Your current attendance is **{results['metrics']['attendance']}%**, which is below the university 75% eligibility threshold. Attend all remaining classes continuously to avoid condonation fees or examination hall-ticket detention.",
            icon="🚨"
        )

    # 2. SUBJECT-WISE BREAKDOWN TABLE (Only if Subject-Wise mode was used)
    if results.get('subject_scores'):
        st.markdown('<div class="section-title" style="margin-top: 2rem;">📋 Subject-Wise Score Breakdown</div>', unsafe_allow_html=True)
        for s in results['subject_scores']:
            status_color = "#16A34A" if s['mid'] >= 25 else ("#2563EB" if s['mid'] >= 20 else ("#D97706" if s['mid'] >= 15 else "#DC2626"))
            status_text = "🌟 Distinction" if s['mid'] >= 25 else ("👍 Good" if s['mid'] >= 20 else ("📈 Average" if s['mid'] >= 15 else "⚠️ Needs Improvement"))
            st.markdown(
                f"""
                <div class="subject-row">
                    <div style="font-weight: 700; color: #1E293B; font-size: 0.95rem;">📘 {s['name']}</div>
                    <div style="display: flex; gap: 1.5rem; align-items: center;">
                        <div style="font-weight: 700; color: #1E3A8A; font-size: 0.95rem;">Mid Marks: {s['mid']} / 30</div>
                        <span style="font-size: 0.82rem; font-weight: 700; color: {status_color}; background: #F1F5F9; padding: 0.2rem 0.6rem; border-radius: 6px;">{status_text}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # 3. SCORE TARGET & IMPROVEMENT PATHWAY
    st.markdown('<div class="section-title" style="margin-top: 2rem;">🎯 Score Target & Improvement Pathway</div>', unsafe_allow_html=True)
    target = results['target_analysis']
    gap_label = f"Target Score Gap: +{target['marks_needed']} Marks to reach next grade level" if target['marks_needed'] > 0 else "Milestone Reached! Maintain consistent performance"
    st.markdown(
        f"""
        <div class="target-box">
            <div class="target-title">🎯 Next Milestone: {target['target_name']}</div>
            <div style="font-weight: 700; font-size: 1.05rem; color: #15803D; margin-bottom: 0.4rem;">
                {gap_label}
            </div>
            <div class="target-body">
                {target['action_pathway']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4. AI ACADEMIC ADVICE (SHORT FORM & CRISP)
    st.markdown('<div class="section-title" style="margin-top: 2rem;">🤖 AI Academic Recommendations (Expert Engine)</div>', unsafe_allow_html=True)

    if results['ai_advice_list']:
        for idx, item in enumerate(results['ai_advice_list'], 1):
            if ":" in item:
                adv_title, adv_content = item.split(":", 1)
            else:
                adv_title, adv_content = f"Tip #{idx}", item

            border_color = "#2563EB"
            if any(w in adv_title for w in ["Critical", "Detention", "Recovery", "Needs Improvement", "Urgent"]):
                border_color = "#DC2626"
            elif any(w in adv_title for w in ["Distinction", "Advantage", "Excellence", "Mastery", "Strong"]):
                border_color = "#16A34A"
            elif any(w in adv_title for w in ["Warning", "Condonation", "Imbalance", "Risk", "Weak", "Average", "Low"]):
                border_color = "#D97706"

            st.markdown(
                f"""
                <div class="advice-card" style="border-left-color: {border_color}; padding: 0.65rem 1rem; margin-bottom: 0.45rem;">
                    <div style="font-size: 0.92rem; line-height: 1.45;">
                        <strong style="color: #0F172A;">{adv_title.strip()}:</strong> <span style="color: #334155;">{adv_content.strip()}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("Your performance across all metrics is balanced! Continue your current study plan.")

    # 5. RECOMMENDED STUDY PLAN
    st.markdown('<div class="section-title" style="margin-top: 2rem;">📅 Recommended Daily Study Plan</div>', unsafe_allow_html=True)
    plan = results['study_plan']
    st.markdown(
        f"""
        <div class="card" style="background: #FFFFFF; border-left: 5px solid #2563EB;">
            <div style="margin-bottom: 0.7rem;">
                <h3 style="margin: 0; font-size: 1.15rem; color: #1E3A8A; font-weight: 800;">{plan['title']}</h3>
            </div>
            <p style="color: #475569; font-size: 0.93rem; margin: 0 0 0.85rem 0; line-height: 1.5;"><strong>Core Strategy:</strong> {plan['strategy']}</p>
            <div class="plan-grid">
                <div class="plan-box">
                    <h4>⏰ Daily Study Commitment</h4>
                    <p>{plan['daily_study']}</p>
                </div>
                <div class="plan-box">
                    <h4>🔄 Daily Revision Block</h4>
                    <p>{plan['revision']}</p>
                </div>
                <div class="plan-box">
                    <h4>📝 Practice Problem Quota</h4>
                    <p>{plan['practice_questions']}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 6. B.TECH CAREER GUIDANCE & SKILLS ROADMAP
    st.markdown(
        f'<div class="section-title" style="margin-top: 2rem;">🚀 B.Tech Career Preparation & Skill Guidance ({results["student_info"]["year"]})</div>',
        unsafe_allow_html=True
    )
    career = results['career_guidance']
    st.markdown(
        f"""
        <div class="card" style="background: #F8FAFC; border: 1.5px solid #CBD5E1;">
            <div style="font-size: 1.1rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0.35rem;">{career['year_title']}</div>
            <div style="font-style: italic; color: #2563EB; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.85rem;">"{career['action_quote']}"</div>
            <ul style="margin: 0; padding-left: 1.3rem; color: #334155; font-size: 0.92rem; line-height: 1.6;">
                {''.join(f'<li style="margin-bottom: 0.4rem;">{focus}</li>' for focus in career['focus_areas'])}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 7. TAILORED BRANCH & YEAR SUGGESTION TABS
    st.markdown(
        f'<div style="font-weight: 800; color: #1E293B; font-size: 1.05rem; margin-top: 1.2rem; margin-bottom: 0.6rem;">Specialized Action Tabs for <strong>{results["student_info"]["branch"]}</strong> ({results["student_info"]["year"]}):</div>',
        unsafe_allow_html=True
    )
    tab_acad, tab_tech, tab_prac = st.tabs([
        "📚 Academic Improvement",
        "💻 Technical Skills Roadmap",
        "🧪 Practical & Lab Skills"
    ])

    with tab_acad:
        st.markdown(f"#### 📚 Academic Improvement Strategies for **{results['student_info']['branch']}** ({results['student_info']['year']})")
        for sug in results['academic_suggestions']:
            title, desc = sug.split(":", 1) if ":" in sug else ("Tip", sug)
            st.markdown(f"- **{title.strip()}:** {desc.strip()}")

    with tab_tech:
        st.markdown(f"#### 💻 Technical Skills Roadmap for **{results['student_info']['branch']}** ({results['student_info']['year']})")
        for sug in results['tech_suggestions']:
            title, desc = sug.split(":", 1) if ":" in sug else ("Skill", sug)
            st.markdown(f"- **{title.strip()}:** {desc.strip()}")

    with tab_prac:
        st.markdown(f"#### 🧪 Practical & Laboratory Skills for **{results['student_info']['branch']}** ({results['student_info']['year']})")
        for sug in results['practical_suggestions']:
            title, desc = sug.split(":", 1) if ":" in sug else ("Practical", sug)
            st.markdown(f"- **{title.strip()}:** {desc.strip()}")

    # 8. EXPLAINABLE AI (XAI) AUDIT TRAIL ACCORDION
    with st.expander("🔍 Explainable AI (XAI) Rule Audit Trail – Why were these recommendations triggered?", expanded=False):
        st.markdown("This transparent audit trail shows exactly which IF–THEN inference rules fired based on your input parameters:")
        for rule in results['rules_applied']:
            st.markdown(
                f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 0.6rem;">
                    <div style="font-weight: 800; color: #1E3A8A; font-size: 0.92rem;">{rule['rule_name']} ({rule['rule_id']})</div>
                    <div style="font-size: 0.82rem; color: #475569; margin: 0.2rem 0;"><strong>Condition:</strong> <code>{rule['condition']}</code> | <strong>Your Value:</strong> <code>{rule['student_value']}</code></div>
                    <div style="font-size: 0.86rem; color: #1E293B;"><strong>Action:</strong> {rule['recommendation']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ------------------------------------------------------------------------------
# 7. RESET ALL OPTION (AT THE VERY BOTTOM)
# ------------------------------------------------------------------------------
st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
st.markdown("---")

col_r1, col_r2, col_r3 = st.columns([1, 1.5, 1])
with col_r2:
    if st.button("🔄 Reset All Inputs", type="secondary", use_container_width=True, help="Clear all inputs and reset the advisor"):
        reset_all_fields()
        st.rerun()

# ------------------------------------------------------------------------------
# 8. MINIMAL FOOTER
# ------------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer-note">
        🎓 <strong>B.Tech Student Performance Advisor</strong> • Explainable Rule-Based AI Engine
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# 9. VERCEL SERVERLESS RUNTIME ENTRYPOINTS
# ==============================================================================
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    """Vercel BaseHTTPRequestHandler entrypoint."""
    def do_GET(self):
        clean_path = self.path.split("?")[0].lstrip("/")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target_path = os.path.join(base_dir, clean_path) if clean_path else os.path.join(base_dir, "index.html")

        if not os.path.isfile(target_path):
            target_path = os.path.join(base_dir, "index.html")

        content_type = "text/html; charset=utf-8"
        if target_path.endswith(".py"):
            content_type = "text/plain; charset=utf-8"
        elif target_path.endswith(".css"):
            content_type = "text/css"
        elif target_path.endswith(".js"):
            content_type = "application/javascript"
        elif target_path.endswith(".json"):
            content_type = "application/json"

        try:
            with open(target_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception:
            self.send_response(404)
            self.end_headers()


def app(environ, start_response):
    """Vercel WSGI entrypoint."""
    path_info = environ.get("PATH_INFO", "/").lstrip("/")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(base_dir, path_info) if path_info else os.path.join(base_dir, "index.html")

    if not os.path.isfile(target_path):
        target_path = os.path.join(base_dir, "index.html")

    content_type = "text/html; charset=utf-8"
    if target_path.endswith(".py"):
        content_type = "text/plain; charset=utf-8"
    elif target_path.endswith(".css"):
        content_type = "text/css"
    elif target_path.endswith(".js"):
        content_type = "application/javascript"
    elif target_path.endswith(".json"):
        content_type = "application/json"

    try:
        with open(target_path, "rb") as f:
            content = f.read()
        start_response("200 OK", [
            ("Content-Type", content_type),
            ("Content-Length", str(len(content)))
        ])
        return [content]
    except Exception:
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Not Found"]


application = app

