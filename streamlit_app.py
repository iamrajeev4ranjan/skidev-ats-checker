import streamlit as st
import fitz  # PyMuPDF
import re

# ============================
# CONFIG
# ============================
CONFIG = {
    "role": "Data Analyst (Premium)",
    "weights": {
        "tools": 25,
        "projects": 25,
        "experience": 20,
        "domain": 15,
        "proof": 15
    },
    "keywords": {
        "tools": ["sql", "python", "excel", "power bi", "tableau", "r", "pandas", "numpy", "matplotlib", "statistics", "ml"],
        "projects": ["analysis", "dashboard", "etl", "automation", "visualization", "business problem"],
        "domain": ["fintech", "banking", "payment", "credit", "risk", "regulatory", "financial modeling"],
        "proof": ["github", "portfolio", "tableau public", "kaggle", "linkedin project"]
    }
}

# ============================
# PDF TEXT EXTRACTION
# ============================
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text.lower()

# ============================
# ATS ANALYSIS
# ============================
def analyze_resume(resume_text, jd_text=""):
    score = 0
    feedback = {}
    results = {}

    # Tools
    matched_tools = [kw for kw in CONFIG["keywords"]["tools"] if kw in resume_text]
    results["tools"] = matched_tools
    if matched_tools:
        score += (len(matched_tools) / len(CONFIG["keywords"]["tools"])) * CONFIG["weights"]["tools"]
    else:
        feedback["tools"] = "❌ Add technical tools (SQL, Python, Power BI, Tableau, etc.)."

    # Projects
    matched_projects = [kw for kw in CONFIG["keywords"]["projects"] if kw in resume_text]
    results["projects"] = matched_projects
    if matched_projects:
        score += (len(matched_projects) / len(CONFIG["keywords"]["projects"])) * CONFIG["weights"]["projects"]
    else:
        feedback["projects"] = "❌ Highlight relevant projects (dashboards, automation, business problem solving)."

    # Experience
    exp_match = re.search(r'(\d+)\+?\s*year', resume_text)
    experience = int(exp_match.group(1)) if exp_match else 0
    results["experience_years"] = experience
    if experience >= 2:
        score += CONFIG["weights"]["experience"]
    elif experience >= 1:
        score += CONFIG["weights"]["experience"] * 0.5
        feedback["experience"] = "⚠️ Add more relevant BA/Data Analyst experience."
    else:
        feedback["experience"] = "ℹ️ Fresher: Compensate with strong academic/relevant projects."

    # Domain Knowledge
    matched_domain = [kw for kw in CONFIG["keywords"]["domain"] if kw in resume_text]
    results["domain"] = matched_domain
    if matched_domain:
        score += (len(matched_domain) / len(CONFIG["keywords"]["domain"])) * CONFIG["weights"]["domain"]
    else:
        feedback["domain"] = "❌ Add FinTech/Banking knowledge."

    # Proof of Work
    matched_proof = [kw for kw in CONFIG["keywords"]["proof"] if kw in resume_text]
    results["proof"] = matched_proof
    if matched_proof:
        score += CONFIG["weights"]["proof"]
    else:
        feedback["proof"] = "❌ Add proof of work (GitHub, Kaggle, Tableau, Portfolio)."

    return round(score, 2), results, feedback

# ============================
# STREAMLIT APP
# ============================
st.set_page_config(page_title="SkiDev ATS Resume Checker", page_icon="📄", layout="wide")

st.title("🚀 SkiDev ATS Resume Checker (Premium)")
st.write("Upload your resume PDF and (optionally) paste a Job Description (JD) for analysis.")

uploaded_file = st.file_uploader("📂 Upload Resume (PDF only)", type=["pdf"])
jd_input = st.text_area("📑 Paste JD (or leave blank to use default Data Analyst role)")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    jd_text = jd_input if jd_input.strip().lower() != "" else ""

    score, results, feedback = analyze_resume(resume_text, jd_text)

    st.subheader("📊 ATS Screening Report")
    st.metric("Final ATS Score", f"{score}/100")

    with st.expander("✅ Matched Keywords"):
        st.write(results)

    with st.expander("⚠️ Detailed Feedback"):
        for k, v in feedback.items():
            st.write(f"- {v}")

    if score >= 70:
        st.success("✅ Strong Fit! Your resume is highly competitive.")
    elif score >= 50:
        st.warning("⚠️ Borderline – Improve tools/projects/impact keywords.")
    else:
        st.error("❌ Not a Fit – Needs major improvements.")
