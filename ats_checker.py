import re
import fitz  # PyMuPDF
import os

DEFAULT_JD = """
We are hiring a Data Analyst. Key skills include SQL, Python, Excel, Power BI/Tableau,
Statistics, Machine Learning basics, data visualization, and strong analytical thinking.
Preferred domains: FinTech, Banking, E-commerce, Healthcare.
Candidates should demonstrate experience/projects involving KPIs, metrics, dashboards,
decision-making, and proof-of-work (GitHub/Tableau/Kaggle/Portfolio).
"""

CONFIG = {
    "weights": {
        "tools": 25,
        "projects": 25,
        "domain": 15,
        "experience": 15,
        "proof": 15,
        "impact": 5,
    },
    "keywords": {
        "tools": ["sql", "python", "excel", "power bi", "tableau", "pandas", "numpy",
                  "matplotlib", "seaborn", "r", "statistics", "ml", "machine learning"],
        "projects": ["dashboard", "etl", "visualization", "analysis", "forecasting",
                     "classification", "regression", "business problem", "prediction"],
        "domain": ["fintech", "banking", "payment", "risk", "credit", "fraud",
                   "e-commerce", "retail", "healthcare", "telecom"],
        "proof": ["github", "tableau public", "portfolio", "kaggle", "medium"],
        "impact": ["kpi", "roi", "metrics", "decision-making", "improved", "optimized",
                   "reduced", "increased", "growth", "retention", "forecast accuracy"],
    }
}

def extract_text_from_pdf(pdf_path):
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + " "
    return text.lower()

def match_keywords(corpus, text):
    return [kw for kw in corpus if kw in text]

def narrow_to_jd(jd_text, corpus):
    jd_text = (jd_text or "").lower()
    jd_terms = [kw for kw in corpus if kw in jd_text]
    return jd_terms if jd_terms else corpus

def analyze_resume(resume_text, jd_text=DEFAULT_JD):
    score = 0.0
    results, feedback = {}, {}

    tools_pool = narrow_to_jd(jd_text, CONFIG["keywords"]["tools"])
    projects_pool = narrow_to_jd(jd_text, CONFIG["keywords"]["projects"])
    domain_pool = narrow_to_jd(jd_text, CONFIG["keywords"]["domain"])

    matched_tools = match_keywords(tools_pool, resume_text)
    results["tools_matched"] = matched_tools
    score += (len(matched_tools) / len(tools_pool)) * CONFIG["weights"]["tools"] if tools_pool else 0
    if len(matched_tools) < max(1, len(tools_pool)//3):
        feedback["tools"] = "❌ Strengthen tools: SQL, Python, Excel, Power BI/Tableau, Statistics."

    matched_projects = match_keywords(projects_pool, resume_text)
    results["projects_matched"] = matched_projects
    score += (len(matched_projects) / len(projects_pool)) * CONFIG["weights"]["projects"] if projects_pool else 0
    if not matched_projects:
        feedback["projects"] = "❌ Add projects with dashboards, forecasting/prediction, or business problem framing."

    matched_domain = match_keywords(domain_pool, resume_text)
    results["domain_matched"] = matched_domain
    score += (len(matched_domain) / len(domain_pool)) * CONFIG["weights"]["domain"] if domain_pool else 0
    if not matched_domain:
        feedback["domain"] = "❌ Add domain context (FinTech/E-commerce/Healthcare) in projects or summary."

    exp_match = re.search(r'(\d+)\+?\s*years?', resume_text)
    exp_years = int(exp_match.group(1)) if exp_match else 0
    results["experience_years"] = exp_years
    if exp_years >= 2:
        score += CONFIG["weights"]["experience"]
    elif exp_years >= 1:
        score += CONFIG["weights"]["experience"] * 0.6
    else:
        feedback["experience"] = "ℹ️ Fresher detected — compensate with high-impact, domain-tagged projects."

    matched_proof = match_keywords(CONFIG["keywords"]["proof"], resume_text)
    results["proof_of_work"] = matched_proof
    if matched_proof:
        score += CONFIG["weights"]["proof"]
    else:
        feedback["proof"] = "❌ Add proof-of-work links (GitHub, Tableau Public, Kaggle, Portfolio)."

    matched_impact = match_keywords(CONFIG["keywords"]["impact"], resume_text)
    results["impact_terms"] = matched_impact
    if matched_impact:
        score += CONFIG["weights"]["impact"]
    else:
        feedback["impact"] = "❌ Use business impact language (KPIs, ROI, decision-making, improved accuracy)."

    return round(score, 2), results, feedback

if __name__ == "__main__":
    try:
        resume_path = input("📂 Enter the path of your resume PDF: ").strip().strip('"').strip("'")
        jd_text = input("📑 Paste JD here (or type 'skip' to use default Data Analyst role): ").strip()
        if jd_text.lower() in ("", "skip"):
            print("\n⚙️ Using default premium Data Analyst JD...")
            jd_text = DEFAULT_JD

        resume_text = extract_text_from_pdf(resume_path)
        score, results, feedback = analyze_resume(resume_text, jd_text)

        print("\n===== PREMIUM ATS SCREENING REPORT =====")
        print(f"Role: {'Custom JD' if jd_text != DEFAULT_JD else 'Data Analyst (Default Premium)'}")
        print(f"Final ATS Score: {score}/100\n")

        print("✅ Matched:")
        for k, v in results.items():
            print(f" - {k}: {v if v else 'None'}")

        print("\n⚠️ Detailed Feedback:")
        if feedback:
            for v in feedback.values():
                print(f" - {v}")
        else:
            print(" - Solid profile. Keep proof-of-work & KPIs visible.")

        print("\n🚀 Verdict:")
        if score >= 80:
            print("✅ Strong Fit — Likely to pass premium analyst screening.")
        elif score >= 60:
            print("⚠️ Borderline — Improve projects/domain alignment.")
        else:
            print("❌ Not a Fit — Upskill tools, projects, and business framing.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
