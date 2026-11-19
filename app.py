"""Optional dashboard:  streamlit run app.py"""
import tempfile
from pathlib import Path

import streamlit as st

from src.extractor import load_resumes
from src.scorer import screen
from src.skills import load_skill_db, parse_job_description

st.set_page_config(page_title="Resume Screening Tool", layout="wide")
st.title("Automated Resume Screening Tool")

skill_db = load_skill_db("data/skills.csv")
default_jd = Path("data/job_description.txt").read_text(encoding="utf-8")

jd_text = st.text_area("Job description (use 'Required Skills:' and 'Preferred Skills:' lines)",
                       default_jd, height=250)
files = st.file_uploader("Upload resumes (PDF / DOCX / TXT)", accept_multiple_files=True,
                         type=["pdf", "docx", "txt"])
use_samples = st.checkbox("Use the sample resumes in /resumes", value=not files)

if st.button("Screen candidates"):
    required, preferred, years = parse_job_description(jd_text, skill_db)
    st.write(f"**Required:** {sorted(required)}  \n**Preferred:** {sorted(preferred)}  \n**Min years:** {years}")
    with tempfile.TemporaryDirectory() as tmp:
        if files:
            for f in files:
                (Path(tmp) / f.name).write_bytes(f.getvalue())
            resumes = load_resumes(tmp)
        elif use_samples:
            resumes = load_resumes("resumes")
        else:
            resumes = {}
    if not resumes:
        st.warning("No readable resumes found.")
    else:
        df = screen(resumes, jd_text, required, preferred, years, skill_db)
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df.set_index("candidate")["score"])
        st.download_button("Download CSV", df.to_csv(index=False), "ranking_report.csv")
