import streamlit as st
import subprocess
import sys
import re
import textwrap
from pathlib import Path

from auth import (
    register_user,
    login_user,
    add_search,
    get_history
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearchOps",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "research"


# ============================================================
# HELPER
# ============================================================

def render_html(html):
    """
    Render actual HTML instead of displaying HTML as code.
    """
    clean_html = textwrap.dedent(html).strip()
    st.html(clean_html)


# ============================================================
# CUSTOM CSS
# ============================================================

render_html("""
<style>

    /* ========================================================
       MAIN PAGE
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                #11152d 0%,
                transparent 35%
            ),
            radial-gradient(
                circle at 90% 20%,
                #071827 0%,
                transparent 35%
            ),
            #070a12;

        color: #f5f7ff;
    }


    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1250px;
    }


    /* ========================================================
       LOGO
       ======================================================== */

    .logo {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 45px;
    }


    .logo-dot {
        color: #7c3aed;
        font-size: 28px;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .badge {
        display: inline-block;
        padding: 8px 15px;

        border: 1px solid rgba(139, 92, 246, 0.35);
        background: rgba(124, 58, 237, 0.10);

        border-radius: 30px;

        color: #c4b5fd;
        font-size: 14px;

        margin-bottom: 18px;
    }


    .hero-title {
        font-size: 58px;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -3px;
        margin-bottom: 18px;
    }


    .gradient-text {
        background: linear-gradient(
            90deg,
            #a78bfa,
            #8b5cf6,
            #6366f1
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-subtitle {
        font-size: 18px;
        line-height: 1.7;
        color: #9ca3b8;
        max-width: 750px;
        margin-bottom: 45px;
    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {
        font-size: 25px;
        font-weight: 750;
        margin-top: 45px;
        margin-bottom: 20px;
    }


    /* ========================================================
       PIPELINE CARDS
       ======================================================== */

    .card {
        background: rgba(17, 24, 39, 0.75);

        border: 1px solid rgba(148, 163, 184, 0.13);
        border-radius: 18px;

        padding: 20px;

        min-height: 165px;

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.15);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }


    .card:hover {
        transform: translateY(-3px);
        border-color: rgba(139, 92, 246, 0.45);
    }


    .agent-icon {
        font-size: 27px;
        margin-bottom: 12px;
    }


    .agent-name {
        font-weight: 700;
        font-size: 16px;
    }


    .agent-description {
        color: #8f99ad;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 7px;
    }


    /* ========================================================
       STAT CARDS
       ======================================================== */

    .stat-card {
        background: rgba(15, 23, 42, 0.90);

        border: 1px solid rgba(148, 163, 184, 0.13);
        border-radius: 16px;

        padding: 20px;

        min-height: 115px;
    }


    .stat-label {
        color: #8d98ad;
        font-size: 13px;
        margin-bottom: 12px;
    }


    .stat-value {
        color: #f8fafc;
        font-size: 28px;
        font-weight: 750;
    }


    /* ========================================================
       TEXTAREA
       ======================================================== */

    textarea {
        background-color: #0d1424 !important;
        color: #f1f5f9 !important;

        border: 1px solid #334155 !important;
        border-radius: 14px !important;
    }


    textarea:focus {
        border-color: #7c3aed !important;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    .stButton > button {
        background: linear-gradient(
            135deg,
            #7c3aed,
            #6366f1
        );

        color: white;

        border: none;
        border-radius: 12px;

        padding: 12px 25px;

        font-size: 15px;
        font-weight: 700;

        min-height: 48px;
    }


    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #8b5cf6,
            #6366f1
        );

        border: none;
        color: white;
    }


    /* ========================================================
       RESULT BOX
       ======================================================== */

    .result-box {
        background: #0b1120;

        border: 1px solid rgba(124, 58, 237, 0.25);
        border-radius: 16px;

        padding: 25px;

        margin-top: 20px;
    }


    .result-box h3 {
        margin-top: 0;
        color: #f8fafc;
    }


    .result-box p {
        color: #94a3b8;
        margin-bottom: 0;
    }


    /* ========================================================
       CLAIM CARDS
       ======================================================== */

    .claim-card {
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.98),
                rgba(11, 17, 32, 0.98)
            );

        border: 1px solid rgba(124, 58, 237, 0.30);

        border-radius: 18px;

        padding: 25px;

        margin: 18px 0;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.18);
    }


    .claim-number {
        color: #a78bfa;

        font-size: 12px;
        font-weight: 800;

        text-transform: uppercase;
        letter-spacing: 1.2px;

        margin-bottom: 10px;
    }


    .claim-text {
        color: #f8fafc;

        font-size: 17px;
        line-height: 1.7;

        margin-bottom: 20px;
    }


    .claim-grid {
        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        gap: 12px;
    }


    .claim-stat {
        background: rgba(2, 6, 23, 0.65);

        border: 1px solid rgba(148, 163, 184, 0.12);

        border-radius: 13px;

        padding: 15px;
    }


    .claim-stat-label {
        color: #64748b;

        font-size: 11px;
        font-weight: 700;

        text-transform: uppercase;
        letter-spacing: 0.8px;

        margin-bottom: 7px;
    }


    .claim-stat-value {
        color: #e2e8f0;

        font-size: 14px;
        line-height: 1.4;

        font-weight: 650;
    }


    .claim-note {
        margin-top: 15px;

        padding: 14px 16px;

        background: rgba(15, 23, 42, 0.75);

        border: 1px solid rgba(148, 163, 184, 0.10);

        border-radius: 12px;

        color: #94a3b8;

        font-size: 13px;
        line-height: 1.6;
    }


    .claim-note strong {
        color: #e2e8f0;
    }


    /* ========================================================
       FINAL REPORT
       ======================================================== */

    .final-report {
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.98),
                rgba(7, 10, 18, 0.98)
            );

        border: 1px solid rgba(124, 58, 237, 0.30);

        border-radius: 20px;

        padding: 30px;

        margin-top: 20px;

        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.20);
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }


    footer {
        visibility: hidden;
    }


    header {
        visibility: hidden;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {

        .hero-title {
            font-size: 42px;
        }

        .claim-grid {
            grid-template-columns: 1fr;
        }

    }

</style>
""")


# ============================================================
# NAVIGATION BAR
# ============================================================

nav_left, nav_research, nav_history, nav_profile, nav_logout = st.columns(
    [4, 1.2, 1.2, 1.2, 1]
)


with nav_left:

    render_html("""
    <div class="logo" style="margin-bottom:0;">
        <span class="logo-dot">◉</span> RESEARCHOPS
    </div>
    """)


with nav_research:

    research_nav = st.button(
        "Research",
        use_container_width=True,
        key="research_nav"
    )


with nav_history:

    history_nav = st.button(
        "History",
        use_container_width=True,
        key="history_nav"
    )


with nav_profile:

    profile_nav = st.button(
        "Profile",
        use_container_width=True,
        key="profile_nav"
    )


with nav_logout:

    logout_nav = st.button(
        "Logout",
        use_container_width=True,
        key="logout_nav"
    )


# ============================================================
# NAVIGATION ACTIONS
# ============================================================

if research_nav:

    st.session_state.current_page = "research"

    st.rerun()


if history_nav:

    st.session_state.current_page = "history"

    st.rerun()


if profile_nav:

    st.session_state.current_page = "profile"

    st.rerun()


if logout_nav:

    st.session_state.show_logout_confirm = True

    st.rerun()

# ============================================================
# LOGOUT CONFIRMATION
# ============================================================

if st.session_state.show_logout_confirm:

    st.warning(
        "Are you sure you want to logout?"
    )

    confirm_col, cancel_col = st.columns(2)

    with confirm_col:

        if st.button(
            "Yes, Logout",
            use_container_width=True,
            key="confirm_logout"
        ):

            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.current_page = "research"
            st.session_state.show_logout_confirm = False

            st.rerun()

    with cancel_col:

        if st.button(
            "Cancel",
            use_container_width=True,
            key="cancel_logout"
        ):

            st.session_state.show_logout_confirm = False

            st.rerun()

# ============================================================
# LOGIN / REGISTER PAGE
# ============================================================

if not st.session_state.logged_in:

    render_html("""
    <div style="
        max-width:500px;
        margin:70px auto 30px auto;
        text-align:center;
    ">

        <h1 style="
            color:#f8fafc;
            font-size:32px;
            margin-bottom:10px;
        ">
            Welcome back
        </h1>

        <p style="
            color:#9ca3b8;
            font-size:15px;
        ">
            Sign in to access your research workspace.
        </p>

    </div>
    """)


    login_tab, register_tab = st.tabs(
        ["Login", "Create Account"]
    )


    # ========================================================
    # LOGIN
    # ========================================================

    with login_tab:

        login_username = st.text_input(
            "Username",
            key="login_username"
        )


        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        if st.button(
            "Login",
            use_container_width=True,
            key="login_button"
        ):

            username = login_username.strip()


            if not username or not login_password:

                st.error(
                    "Please enter your username and password."
                )

            else:

                success, message = login_user(
                    username,
                    login_password
                )


                if success:

                    st.session_state.logged_in = True

                    st.session_state.username = username

                    st.session_state.current_page = "research"

                    st.rerun()


                else:

                    st.error(message)


    # ========================================================
    # CREATE ACCOUNT
    # ========================================================

    with register_tab:

        register_username = st.text_input(
            "Choose a username",
            key="register_username"
        )


        register_password = st.text_input(
            "Choose a password",
            type="password",
            key="register_password"
        )


        register_confirm = st.text_input(
            "Confirm password",
            type="password",
            key="register_confirm"
        )


        if st.button(
            "Create Account",
            use_container_width=True,
            key="register_button"
        ):

            username = register_username.strip()


            if not username:

                st.error(
                    "Please enter a username."
                )


            elif not register_password:

                st.error(
                    "Please enter a password."
                )


            elif register_password != register_confirm:

                st.error(
                    "Passwords do not match."
                )


            else:

                success, message = register_user(
                    username,
                    register_password
                )


                if success:

                    st.success(message)

                    st.info(
                        "Your account is ready. "
                        "Go to the Login tab."
                    )


                else:

                    st.error(message)


    st.stop()


# ============================================================
# HISTORY PAGE
# ============================================================

if st.session_state.current_page == "history":

    render_html("""
    <div class="section-title">
        Research History
    </div>

    <p style="
        color:#9ca3b8;
        margin-bottom:30px;
    ">
        Your previous research missions.
    </p>
    """)


    user_history = get_history(
        st.session_state.username
    )


    if not user_history:

        st.info(
            "No research history yet. "
            "Start your first research mission."
        )


    else:

        for index, item in enumerate(
            reversed(user_history),
            start=1
        ):

            saved_question = item.get(
                "question",
                "Untitled research"
            )


            saved_report = item.get(
                "report",
                ""
            )


            render_html(f"""
            <div class="claim-card">

                <div class="claim-number">
                    Research {index}
                </div>

                <div class="claim-text">
                    {saved_question}
                </div>

            </div>
            """)


            if saved_report:

                with st.expander(
                    "View Final Report"
                ):

                    st.markdown(
                        saved_report,
                        unsafe_allow_html=False
                    )


                    st.download_button(
                        "Download Report",
                        data=saved_report,
                        file_name=f"research_report_{index}.md",
                        mime="text/markdown",
                        key=f"download_history_{index}"
                    )


    st.stop()


# ============================================================
# PROFILE PAGE
# ============================================================

if st.session_state.current_page == "profile":

    render_html("""
    <div class="section-title">
        Profile
    </div>

    <p style="
        color:#9ca3b8;
        margin-bottom:30px;
    ">
        Your ResearchOps account information.
    </p>
    """)


    user_history = get_history(
        st.session_state.username
    )


    render_html(f"""
    <div class="final-report">

        <div class="claim-number">
            ACCOUNT
        </div>

        <div style="
            color:#f8fafc;
            font-size:24px;
            font-weight:700;
            margin-bottom:20px;
        ">
            {st.session_state.username}
        </div>

        <div class="claim-grid">

            <div class="claim-stat">

                <div class="claim-stat-label">
                    Username
                </div>

                <div class="claim-stat-value">
                    {st.session_state.username}
                </div>

            </div>


            <div class="claim-stat">

                <div class="claim-stat-label">
                    Research Missions
                </div>

                <div class="claim-stat-value">
                    {len(user_history)}
                </div>

            </div>


            <div class="claim-stat">

                <div class="claim-stat-label">
                    Account Status
                </div>

                <div class="claim-stat-value">
                    Active
                </div>

            </div>

        </div>

    </div>
    """)


    st.stop()


# ============================================================
# HERO SECTION
# ============================================================

render_html("""
<div class="badge">
    ✦ Autonomous Research Agent
</div>

<div class="hero-title">
    Turn questions into<br>
    <span class="gradient-text">
        verified intelligence.
    </span>
</div>

<div class="hero-subtitle">
    ResearchOps autonomously searches the web,
    extracts evidence, verifies claims,
    analyzes findings, and generates a
    structured research report.
</div>
""")


# ============================================================
# RESEARCH INPUT
# ============================================================

render_html("""
<div class="section-title">
    Start a research mission
</div>
""")


question = st.text_area(
    label="Research question",
    placeholder="Example: Analyze the electric vehicle market in India",
    height=130,
    label_visibility="collapsed"
)


start = st.button(
    "✦  Start Research",
    use_container_width=False,
    key="start_research"
)


# ============================================================
# PIPELINE
# ============================================================

render_html("""
<div class="section-title">
    Research pipeline
</div>
""")


pipeline_cols = st.columns(6)


agents = [
    (
        "🧠",
        "Planner",
        "Breaks the question into research tasks."
    ),
    (
        "🔎",
        "Researcher",
        "Searches the web for relevant sources."
    ),
    (
        "📄",
        "Extractor",
        "Extracts useful evidence from sources."
    ),
    (
        "🛡️",
        "Verifier",
        "Checks claims against evidence."
    ),
    (
        "📊",
        "Analyst",
        "Analyzes verified findings."
    ),
    (
        "📝",
        "Reporter",
        "Builds the final research report."
    )
]


for col, (icon, name, description) in zip(
    pipeline_cols,
    agents
):

    with col:

        render_html(f"""
        <div class="card">

            <div class="agent-icon">
                {icon}
            </div>

            <div class="agent-name">
                {name}
            </div>

            <div class="agent-description">
                {description}
            </div>

        </div>
        """)


# ============================================================
# RESEARCH INTELLIGENCE
# ============================================================

render_html("""
<div class="section-title">
    Research intelligence
</div>
""")


stat1, stat2, stat3, stat4 = st.columns(4)


with stat1:

    render_html("""
    <div class="stat-card">

        <div class="stat-label">
            Sources
        </div>

        <div class="stat-value">
            —
        </div>

    </div>
    """)


with stat2:

    render_html("""
    <div class="stat-card">

        <div class="stat-label">
            Evidence
        </div>

        <div class="stat-value">
            —
        </div>

    </div>
    """)


with stat3:

    render_html("""
    <div class="stat-card">

        <div class="stat-label">
            Confidence
        </div>

        <div class="stat-value">
            —
        </div>

    </div>
    """)


with stat4:

    render_html("""
    <div class="stat-card">

        <div class="stat-label">
            Status
        </div>

        <div class="stat-value">
            Ready
        </div>

    </div>
    """)


# ============================================================
# RUN COMPLETE RESEARCH PIPELINE
# ============================================================

if start:

    if not question.strip():

        st.warning(
            "Please enter a research question first."
        )

    else:

        render_html("""
        <div class="section-title">
            Mission progress
        </div>
        """)


        progress = st.progress(0)

        status = st.empty()


        status.info(
            "🚀 Starting ResearchOps..."
        )


        progress.progress(10)


        try:

            # ====================================================
            # PROJECT DIRECTORY
            # ====================================================

            project_dir = Path(
                __file__
            ).resolve().parent


            # ====================================================
            # FIND REPORTER.PY
            # ====================================================

            reporter_path = project_dir / "reporter.py"


            if not reporter_path.exists():

                raise FileNotFoundError(
                    "reporter.py was not found "
                    "in the ResearchOps folder."
                )


            status.info(
                "🧠 Running complete ResearchOps pipeline..."
            )


            progress.progress(15)


            # ====================================================
            # RUN REPORTER.PY
            # ====================================================

            process = subprocess.Popen(
                [
                    sys.executable,
                    str(reporter_path)
                ],

                stdin=subprocess.PIPE,

                stdout=subprocess.PIPE,

                stderr=subprocess.STDOUT,

                text=True,

                encoding="utf-8",

                errors="replace",

                cwd=str(project_dir)
            )


            # ====================================================
            # SEND RESEARCH QUESTION
            # ====================================================

            try:

                stdout, _ = process.communicate(
                    input=question.strip(),
                    timeout=300
                )


            except subprocess.TimeoutExpired:

                process.kill()

                stdout, _ = process.communicate()


                st.error(
                    "Research timed out. "
                    "The AI service may be temporarily unavailable."
                )


                with st.expander(
                    "Pipeline output"
                ):

                    st.text(stdout)


                st.stop()


            progress.progress(100)


            # ====================================================
            # FULL PIPELINE OUTPUT
            # ====================================================

            full_output = stdout or ""


            st.subheader(
                "RAW PIPELINE OUTPUT"
            )


            st.text_area(
                "Raw output from reporter.py",
                full_output,
                height=600
            )


            # ====================================================
            # PIPELINE STATUS
            # ====================================================

            if process.returncode == 0:

                status.success(
                    "✓ Complete ResearchOps pipeline "
                    "finished successfully."
                )


                render_html("""
                <div class="result-box">

                    <h3>
                        Research completed
                    </h3>

                    <p>
                        Your question passed through
                        Researcher, Extractor, Verifier,
                        Analyst, and Reporter.
                    </p>

                </div>
                """)


            else:

                status.warning(
                    "Research pipeline completed with warnings."
                )


            # ====================================================
            # EXTRACT SOURCE COUNT
            # ====================================================

            source_match = re.search(
                r"Found\s+(\d+)\s+sources",
                full_output,
                re.IGNORECASE
            )


            source_count = (
                source_match.group(1)
                if source_match
                else "—"
            )


            # ====================================================
            # EXTRACT CONFIDENCE
            # ====================================================

            confidence_matches = re.findall(
                r"CONFIDENCE:\s*([^\n]+)",
                full_output,
                re.IGNORECASE
            )


            if confidence_matches:

                confidence_values = [
                    value.strip()
                    for value in confidence_matches
                ]


                if all(
                    value.lower() == "high"
                    for value in confidence_values
                ):

                    overall_confidence = "High"


                elif any(
                    value.lower() == "low"
                    for value in confidence_values
                ):

                    overall_confidence = "Mixed"


                else:

                    overall_confidence = "Medium"


            else:

                overall_confidence = "—"


            # ====================================================
            # DISPLAY RESEARCH INTELLIGENCE
            # ====================================================

            render_html(f"""
            <div style="
                display:grid;
                grid-template-columns:
                    repeat(4, minmax(0, 1fr));
                gap:15px;
                margin-top:20px;
            ">

                <div class="stat-card">

                    <div class="stat-label">
                        Sources
                    </div>

                    <div class="stat-value">
                        {source_count}
                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-label">
                        Evidence
                    </div>

                    <div class="stat-value">
                        Extracted
                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-label">
                        Confidence
                    </div>

                    <div class="stat-value">
                        {overall_confidence}
                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-label">
                        Status
                    </div>

                    <div class="stat-value">
                        Complete
                    </div>

                </div>

            </div>
            """)


            # ====================================================
            # VERIFICATION REPORT / CLAIMS
            # ====================================================

            render_html("""
            <div class="section-title">
                Verification results
            </div>
            """)


            claim_pattern = re.compile(
                r"CLAIM\s*(\d+)\s*:\s*(.*?)"
                r"(?=\n\s*(?:---+\s*)?"
                r"CLAIM\s*\d+\s*:|"
                r"\n\s*RESEARCHOPS\s*—\s*FINAL REPORT|"
                r"\n\s*FULL\s+RESEARCH\s+PIPELINE\s+COMPLETE|"
                r"$)",
                re.IGNORECASE | re.DOTALL
            )


            claims = claim_pattern.findall(
                full_output
            )


            # ====================================================
            # DISPLAY CLAIMS
            # ====================================================

            if claims:

                for claim_number, claim_block in claims:

                    claim_block = claim_block.strip()


                    # --------------------------------------------
                    # CLAIM TEXT
                    # --------------------------------------------

                    claim_match = re.search(
                        r"^(.*?)(?=\n\s*SOURCE SUPPORT:)",
                        claim_block,
                        re.IGNORECASE | re.DOTALL
                    )


                    claim_text = (
                        claim_match.group(1).strip()
                        if claim_match
                        else claim_block
                    )


                    # --------------------------------------------
                    # SOURCE SUPPORT
                    # --------------------------------------------

                    support_match = re.search(
                        r"SOURCE SUPPORT:\s*(.*?)(?="
                        r"\n\s*SOURCE QUALITY:)",
                        claim_block,
                        re.IGNORECASE | re.DOTALL
                    )


                    support = (
                        support_match.group(1).strip()
                        if support_match
                        else "Not available"
                    )


                    # --------------------------------------------
                    # SOURCE QUALITY
                    # --------------------------------------------

                    quality_match = re.search(
                        r"SOURCE QUALITY:\s*(.*?)(?="
                        r"\n\s*CONFLICT:)",
                        claim_block,
                        re.IGNORECASE | re.DOTALL
                    )


                    quality = (
                        quality_match.group(1).strip()
                        if quality_match
                        else "Not available"
                    )


                    # --------------------------------------------
                    # CONFLICT
                    # --------------------------------------------

                    conflict_match = re.search(
                        r"CONFLICT:\s*(.*?)(?="
                        r"\n\s*CONFIDENCE:)",
                        claim_block,
                        re.IGNORECASE | re.DOTALL
                    )


                    conflict = (
                        conflict_match.group(1).strip()
                        if conflict_match
                        else "None identified"
                    )


                    # --------------------------------------------
                    # CONFIDENCE
                    # --------------------------------------------

                    confidence_match = re.search(
                        r"CONFIDENCE:\s*(.*?)(?="
                        r"\n\s*NEEDS MORE RESEARCH:)",
                        claim_block,
                        re.IGNORECASE | re.DOTALL
                    )


                    confidence = (
                        confidence_match.group(1).strip()
                        if confidence_match
                        else "Not available"
                    )


                    # --------------------------------------------
                    # MORE RESEARCH
                    # --------------------------------------------

                    research_match = re.search(
                        r"NEEDS MORE RESEARCH:\s*(.*)$",
                        claim_block,
                        re.IGNORECASE | re.DOTALL
                    )


                    more_research = (
                        research_match.group(1).strip()
                        if research_match
                        else "Not specified"
                    )


                    # --------------------------------------------
                    # DISPLAY CLAIM CARD
                    # --------------------------------------------

                    render_html(f"""
                    <div class="claim-card">

                        <div class="claim-number">
                            Claim {claim_number}
                        </div>


                        <div class="claim-text">
                            {claim_text}
                        </div>


                        <div class="claim-grid">

                            <div class="claim-stat">

                                <div class="claim-stat-label">
                                    Source Support
                                </div>

                                <div class="claim-stat-value">
                                    {support}
                                </div>

                            </div>


                            <div class="claim-stat">

                                <div class="claim-stat-label">
                                    Source Quality
                                </div>

                                <div class="claim-stat-value">
                                    {quality}
                                </div>

                            </div>


                            <div class="claim-stat">

                                <div class="claim-stat-label">
                                    Confidence
                                </div>

                                <div class="claim-stat-value">
                                    {confidence}
                                </div>

                            </div>

                        </div>


                        <div class="claim-note">

                            <strong>
                                Conflict:
                            </strong>

                            {conflict}

                            <br><br>

                            <strong>
                                Needs More Research:
                            </strong>

                            {more_research}

                        </div>

                    </div>
                    """)


            else:

                st.info(
                    "No structured verification claims "
                    "were detected."
                )


            # ====================================================
            # EXTRACT FINAL REPORT
            # ====================================================

            final_report = ""


            report_match = re.search(
                r"RESEARCHOPS.*?RESEARCH\s+REPORT\s*(.*?)"
                r"(?:FULL\s+RESEARCH\s+PIPELINE\s+COMPLETE|"
                r"={10,}\s*RESEARCH|$)",
                full_output,
                re.IGNORECASE | re.DOTALL
            )


            if report_match:

                final_report = (
                    report_match.group(1).strip()
                )


            # ====================================================
            # FALLBACK REPORT EXTRACTION
            # ====================================================

            if not final_report:

                report_match = re.search(
                    r"RESEARCH\s+REPORT\s*(.*)",
                    full_output,
                    re.IGNORECASE | re.DOTALL
                )


                if report_match:

                    final_report = (
                        report_match.group(1).strip()
                    )


            # ====================================================
            # CLEAN TERMINAL MARKERS
            # ====================================================

            if final_report:

                final_report = re.sub(
                    r"FULL\s+RESEARCH\s+PIPELINE\s+COMPLETE.*",
                    "",
                    final_report,
                    flags=re.IGNORECASE | re.DOTALL
                ).strip()


                final_report = re.sub(
                    r"={10,}\s*RESEARCH.*$",
                    "",
                    final_report,
                    flags=re.IGNORECASE | re.DOTALL
                ).strip()


            # ====================================================
            # DISPLAY FINAL REPORT
            # ====================================================

            render_html("""
            <div class="section-title">
                Final research report
            </div>
            """)


            if final_report:

                # =================================================
                # SAVE TO LOGGED-IN USER'S HISTORY
                # =================================================

                add_search(
                    st.session_state.username,
                    question.strip(),
                    final_report
                )


                # =================================================
                # DISPLAY REPORT
                # =================================================

                render_html("""
                <div class="final-report">
                """)


                st.markdown(
                    final_report,
                    unsafe_allow_html=False
                )


                render_html("""
                </div>
                """)


                # =================================================
                # DOWNLOAD CURRENT REPORT
                # =================================================

                st.download_button(
                    "⬇ Download Final Report",
                    data=final_report,
                    file_name="research_report.md",
                    mime="text/markdown",
                    key="download_current_report"
                )


            else:

                st.warning(
                    "The pipeline completed, but the final "
                    "report could not be extracted."
                )


        # ========================================================
        # ERROR HANDLING
        # ========================================================

        except FileNotFoundError as e:

            st.error(
                str(e)
            )


        except Exception as e:

            st.error(
                f"Something went wrong: {str(e)}"
            )


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div style="
    text-align:center;
    margin-top:70px;
    padding-top:25px;
    border-top:1px solid rgba(148,163,184,0.1);
    color:#64748b;
    font-size:13px;
">
    RESEARCHOPS · Autonomous Research Intelligence
</div>
""")