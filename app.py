# app.py (Dark theme toggle + optional Lottie support + attractive UI)
import streamlit as st
from parser import parse_file
from scorer import batch_score, generate_candidate_summary
import os
import pandas as pd
import math
import html
import json

# ---------- Try optional Lottie support ----------
_lottie_available = False
try:
    from streamlit_lottie import st_lottie  # type: ignore
    _lottie_available = True
except Exception:
    _lottie_available = False

LOTTIE_FUNNY = os.path.join("assets", "funny_ai.json")
LOTTIE_GLOSSY = os.path.join("assets", "ai_glossy.json")
LOTTIE_JOB = os.path.join("assets", "job_colorful.json")

# ---------- Page config ----------
st.set_page_config(
    page_title="Resume Screening Agent",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme handling ----------
# default theme
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Top row: theme toggle control
col_left, col_right = st.columns([8, 2])
with col_right:
    if st.button("Toggle theme"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# ---------- Dynamic CSS based on theme ----------
def get_css(theme: str):
    if theme == "dark":
        return """
        <style>
        .stApp { background: linear-gradient(180deg,#0f1724 0%, #071028 100%); color: #e6eef8; font-family: 'Segoe UI', Roboto, Arial; }
        .header-anim { background: linear-gradient(90deg,#0b63d4,#1e3a8a,#7c3aed); color: #fff; padding: 18px; border-radius:10px; box-shadow: 0 8px 30px rgba(0,0,0,0.6); }
        .card { background: #071428; border-radius:12px; padding:14px; box-shadow: 0 6px 18px rgba(0,0,0,0.6); color: #e6eef8; }
        .smallmuted { color:#9aa7bf; font-size:13px; }
        .jd-box { background: #082033; padding:12px; border-radius:8px; color:#dbeafe; }
        .brand { color: #9be7ff; font-weight:700; }
        .badge.green { background:#059669; }
        .badge.orange { background:#f97316; }
        .badge.red { background:#ef4444; }
        .header-anim { background-size: 300% 300%; animation: gradientShift 8s ease infinite; }
        @keyframes gradientShift { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
        </style>
        """
    else:
        # light theme (previous)
        return """
        <style>
        .stApp { background: linear-gradient(180deg, #f7fbff 0%, #ffffff 100%); font-family: 'Segoe UI', Roboto, Arial; color: #0b1220; }
        .header-anim { background: linear-gradient(90deg, #0b63d4, #6ec1ff, #9be7ff); color: white; padding: 18px; border-radius: 10px; box-shadow: 0 8px 30px rgba(11,99,212,0.12); }
        .card { background: #ffffff; border-radius: 12px; padding: 14px; box-shadow: 0 6px 18px rgba(20,40,80,0.06); margin-bottom: 12px; color: #0b1220; }
        .smallmuted { color: #6b7280; font-size:13px; }
        .jd-box { background: #f3f6fb; padding: 12px; border-radius: 8px; }
        .brand { color: #0b63d4; font-weight: 700; }
        .badge.green { background: #16a34a; }
        .badge.orange { background: #f97316; }
        .badge.red { background: #ef4444; }
        </style>
        """

st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# ---------- Helper functions ----------
def badge_html(score: float) -> str:
    try:
        s = float(score)
    except:
        s = 0.0
    if s >= 75:
        cls = "green"
        label = "High match"
    elif s >= 50:
        cls = "orange"
        label = "Medium match"
    else:
        cls = "red"
        label = "Low match"
    return f"<span class='badge {cls}' style='color:white; padding:6px 10px; border-radius:999px; font-weight:600; font-size:13px'>{label}</span>"

def render_logo_or_svg():
    logo_path = "assets/logo.svg"
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "r", encoding="utf-8") as f:
                svg = f.read()
            st.markdown(svg, unsafe_allow_html=True)
        except Exception:
            pass
    else:
        svg = '<svg width="120" height="120" viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg"><rect width="160" height="160" rx="20" fill="#0b63d4"/><text x="80" y="95" fill="#fff" text-anchor="middle" font-size="36" font-family="Segoe UI, Roboto">AI</text></svg>'
        st.markdown(svg, unsafe_allow_html=True)

def load_lottie(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

# ---------- Sidebar ----------
with st.sidebar:
    render_logo_or_svg()
    st.markdown("<h3 class='brand'>Resume Screening Agent</h3>", unsafe_allow_html=True)
    st.markdown("<div class='smallmuted'>Upload JD & resumes — AI ranks candidates by job fit</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Options")
    st.markdown("- Toggle theme using the top-right button")
    if _lottie_available:
        st.markdown("- Lottie support available")
        if os.path.exists(LOTTIE_FUNNY):
            st.success("funny_ai.json found (assets/funny_ai.json)")
        else:
            st.info("Add assets/funny_ai.json to enable header animation")
        if os.path.exists(LOTTIE_GLOSSY):
            st.success("ai_glossy.json found (assets/ai_glossy.json)")
        else:
            st.info("Add assets/ai_glossy.json to enable glossy animation")
        if os.path.exists(LOTTIE_JOB):
            st.success("job_colorful.json found (assets/job_colorful.json)")
        else:
            st.info("Add assets/job_colorful.json to enable job animation")
    else:
        st.markdown("- Lottie: not installed (optional)")
        st.markdown("  Install: pip install streamlit-lottie")
    st.markdown("---")
    st.caption("Made with ❤️ by Bharat !")

# ---------- Animated header (keeps theme friendly) ----------
st.markdown("<div class='header-anim'><h1 style='margin:6px 0 2px 0'>Resume Screening Agent</h1><div style='font-size:14px; opacity:0.95'>Upload a Job Description and multiple resumes. AI ranks & summarizes candidates.</div></div>", unsafe_allow_html=True)
st.write("")

# If Lottie available and file present, show it
if _lottie_available and os.path.exists(LOTTIE_FUNNY):
    ljson = load_lottie(LOTTIE_FUNNY)
    if ljson:
        try:
            st_lottie(ljson, height=220, key="funny_top")
        except Exception:
            pass

# ---------- Upload Section ----------
upload_col1, upload_col2 = st.columns([2, 3])

with upload_col1:
    jd_file = st.file_uploader("📄 Upload Job Description (TXT / PDF / DOCX)", type=["txt", "pdf", "docx"])
    st.write("")
    resume_files = st.file_uploader("📎 Upload Resumes (Multiple)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    st.write("")
    score_btn = st.button("🔎 Score Resumes", use_container_width=True)

with upload_col2:
    st.markdown("#### Job Description Preview")
    if jd_file:
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        jd_path = os.path.join(temp_dir, jd_file.name)

        with open(jd_path, "wb") as f:
            f.write(jd_file.getbuffer())

        jd_text = parse_file(jd_path)
        if len(jd_text.strip()) == 0:
            st.warning("JD parsed as empty — scanned PDF? use a text JD for best results.")
        st.markdown(f"<div class='jd-box'>{html.escape(jd_text[:2000]).replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
    else:
        st.info("Upload a JD to preview here.")

# ---------- Scoring ----------
if score_btn:
    if not jd_file or not resume_files:
        st.error("Upload JD + at least 1 resume")
    else:
        jd_path = os.path.join("temp_uploads", jd_file.name)
        jd_text = parse_file(jd_path)

        resumes = {}
        for rf in resume_files:
            rp = os.path.join("temp_uploads", rf.name)
            with open(rp, "wb") as f:
                f.write(rf.getbuffer())
            resumes[rf.name] = parse_file(rp)

        with st.spinner("Scoring resumes..."):
            results = batch_score(resumes, jd_text)

        # Metrics summary
        num = len(results)
        top_score = results[0]["score"] if num > 0 else 0
        avg_score = math.floor(sum([r["score"] for r in results]) / (num or 1))

        mcol1, mcol2, mcol3 = st.columns([1, 1, 1])
        mcol1.metric("Total Resumes", num)
        mcol2.metric("Top Score", int(top_score))
        mcol3.metric("Average Score", int(avg_score))

        st.markdown("### Ranked Candidates")

        for r in results:
            score = r["score"]
            text = r["text"] or ""
            name = r["filename"]

            badge = badge_html(score)

            st.markdown("<div class='card'>", unsafe_allow_html=True)

            c1, c2 = st.columns([8, 2])
            c1.markdown(f"**{html.escape(name)}** {badge}", unsafe_allow_html=True)
            c1.markdown(f"<div class='smallmuted'>Score: <strong>{score}</strong></div>", unsafe_allow_html=True)
            c1.write(text[:300] + ("..." if len(text) > 300 else ""))

            progress = min(max(score / 100, 0.0), 1.0)
            c2.progress(progress)
            c2.metric("Match", f"{int(progress * 100)}%")

            cols = st.columns([1, 1, 6])

            if cols[0].button(f"📝 Summary {name}", key=f"sum_{name}"):
                with st.spinner("Generating AI summary..."):
                    summary = generate_candidate_summary(jd_text, text)
                st.json(summary)

            cols[1].download_button(
                "⬇️ Download",
                data=text,
                file_name=f"{name}.txt",
                mime="text/plain"
            )

            with cols[2]:
                with st.expander("Show full resume text"):
                    st.text_area("Resume text", value=text, height=200)

            st.markdown("</div>", unsafe_allow_html=True)

        # after the loop (aligned with the `if score_btn` block)
        df = pd.DataFrame([{"filename": r["filename"], "score": r["score"]} for r in results])
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "results.csv", "text/csv")

        st.success("Done! Resumes ranked successfully.")
