import streamlit as st
import fitz  # PyMuPDF
import re

# =========================
# CONFIGURATION
# =========================
CONFIG = {
    "role": "Data Analyst (Premium)",
    "weights": {
        "tools": 25,
        "projects": 25,
        "experience": 20,
        "domain": 15,
        "proof": 15,
    },
    "keywords": {
        "tools": ["sql", "python", "excel", "power bi", "tableau", "r", "pandas", "numpy", "matplotlib"],
        "projects": ["analysis", "dashboard", "etl", "visualization", "business problem"],
        "domain": ["fintech", "banking", "credit", "risk", "payment", "regulatory"],
        "proof": ["github", "kaggle", "tableau", "portfolio", "linkedin"],
        "impact": ["kpi", "metrics", "roi", "improved", "growth", "decision-making"],
    }
}

# =========================
# UTILS
# =========================
def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF"""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text.lower()


def match_keywords(keywords, text):
    return [kw for kw in keywords if kw in text]


def analyze_resume(resume_text, jd_text=""):
    score = 0
    feedback = {}
    results = {}

    # Tools
    matched_tools = match_keywords(CONFIG["keywords"]["tools"], resume_text)
    results["tools"] = matched_tools
    score += (len(matched_tools) / len(CONFIG["keywords"]["tools"])) * CONFIG["weights"]["tools"]

    # Projects
    matched_projects = match_keywords(CONFIG["keywords"]["projects"], resume_text)
    results["projects"] = matched_projects
    score += (len(matched_projects) / len(CONFIG["keywords"]["projects"])) * CONFIG["weights"]["projects"]

    # Experience
    exp_match = re.search(r'(\d+)\+?\s*year', resume_text)
    experience = int(exp_match.group(1)) if exp_match else 0
    results["experience_years"] = experience
    if experience >= 2:
        score += CONFIG["weights"]["experience"]
    elif experience >= 1:
        score += CONFIG["weights"]["experience"] * 0.5
        feedback["experience"] = "⚠️ Add more relevant BA/DA experience."
    else:
        feedback["experience"] = "ℹ️ Fresher profile: highlight academic/relevant projects."

    # Domain
    matched_domain = match_keywords(CONFIG["keywords"]["domain"], resume_text + jd_text)
    results["domain"] = matched_domain
    if matched_domain:
        score += (len(matched_domain) / len(CONFIG["keywords"]["domain"])) * CONFIG["weights"]["domain"]
    else:
        feedback["domain"] = "❌ Add FinTech/Banking keywords if relevant."

    # Proof of Work
    matched_proof = match_keywords(CONFIG["keywords"]["proof"], resume_text)
    results["proof"] = matched_proof
    if matched_proof:
        score += CONFIG["weights"]["proof"]
    else:
        feedback["proof"] = "❌ Add GitHub/Kaggle/Tableau/Portfolio links."

    # Business Impact
    matched_impact = match_keywords(CONFIG["keywords"]["impact"], resume_text)
    results["impact"] = matched_impact

    return round(score, 2), results, feedback

# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="SkiDev ATS Resume Checker", page_icon="🚀", layout="wide")

st.title("🚀 SkiDev ATS Resume Checker")
st.write("Upload your resume PDF + optional JD to get ATS Score & Feedback.")

resume_file = st.file_uploader("📂 Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("📑 Paste Job Description (optional)", "")

if resume_file:
    with st.spinner("Analyzing resume..."):
        try:
            resume_text = extract_text_from_pdf(resume_file)
            score, results, feedback = analyze_resume(resume_text, jd_text)

            st.subheader("📊 ATS Screening Report")
            st.metric("Final ATS Score", f"{score}/100")

            st.write("### ✅ Matched Keywords")
            for k, v in results.items():
                st.write(f"- **{k}**: {v if v else 'None'}")

            st.write("### ⚠️ Feedback")
            if feedback:
                for v in feedback.values():
                    st.write(f"- {v}")
            else:
                st.success("Your resume looks strong! ✅")

        except Exception as e:
            st.error(f"Error processing resume: {e}")
