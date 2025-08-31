# 🚀 SkiDev ATS Resume Checker (Premium)

An ATS-style resume screening tool for Data Analyst / FinTech Analyst roles.  
It scores across:
- Tools & Technical Skills
- Projects & Use Cases
- Domain Alignment
- Experience
- Proof of Work (GitHub / Tableau / Portfolio)
- Business Impact Language (KPIs, ROI, decision-making)

## How to run (terminal)
```bash
pip install -r requirements.txt
python ats_checker.py
```

## Web App (Streamlit)
Deploy on Streamlit Cloud and share your link. Main app file: `streamlit_app.py`.

## What it does
- Upload a PDF resume
- (Optional) Paste a Job Description (JD)
- Get ATS score + matched keywords + detailed feedback

## Notes
- Default JD targets a **premium Data Analyst** role if you skip JD input.
- No confidential data is stored by this open-source script.
