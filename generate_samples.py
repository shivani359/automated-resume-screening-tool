"""Creates 8 SYNTHETIC resumes (fake people, fake data) in TXT, DOCX and PDF.
No real personal data is used anywhere in this project."""
from pathlib import Path

from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUT = Path("resumes")
OUT.mkdir(exist_ok=True)

RESUMES = {
 "aarav_sharma": ("pdf", """Aarav Sharma
Python Developer | aarav@example.com
Summary: Python developer with 4 years of experience building data pipelines and REST APIs.
Skills: Python, SQL, Pandas, NumPy, Git, REST API, Flask, Docker, AWS, scikit-learn
Experience:
Data Engineer, Acme Analytics (2021-2025) - 4 years
- Built ETL pipelines with Python and Pandas processing 2M rows daily
- Designed REST APIs in Flask; deployed with Docker on AWS
Education: B.Tech in Computer Science"""),
 "diya_patel": ("docx", """Diya Patel
Backend Developer
Skills: Python, PostgreSQL, Pandas, GitHub, RESTful services, FastAPI, Machine Learning
Experience: 3 years of experience in backend development and automation scripts.
Built SQL reporting dashboards and automated Excel reports with Python.
Education: Bachelor of Science in Computer Science"""),
 "rohan_verma": ("txt", """Rohan Verma
Junior Python Developer
Skills: Python, Git, Flask, HTML, CSS
Experience: 1 year of experience. Built a small Flask blog and a to-do app.
Education: B.Tech in Information Technology"""),
 "meera_nair": ("pdf", """Meera Nair
Data Analyst
Skills: SQL, Excel, Power BI, Tableau, Python, Pandas, Data Analysis
Experience: 3 years as a data analyst creating dashboards and KPI reports.
Used Python and Pandas for cleaning data; Git for version control.
Education: Master of Science in Statistics"""),
 "kabir_singh": ("docx", """Kabir Singh
Java Developer
Skills: Java, Spring, MySQL, Javascript, React, Kubernetes
Experience: 6 years of experience in enterprise Java applications and microservices.
Education: B.E. Computer Engineering"""),
 "ananya_rao": ("txt", """Ananya Rao
Machine Learning Engineer
Skills: Python, Pandas, NumPy, scikit-learn, TensorFlow, SQL, Git, Docker, NLP
Experience: 2 years of experience training NLP models and exposing them through REST API endpoints.
Education: M.Tech in Artificial Intelligence"""),
 "vikram_joshi": ("pdf", """Vikram Joshi
Fresher | Marketing graduate
Skills: Communication, Excel, Social media
Experience: Internship in digital marketing (6 months).
Education: Bachelor of Commerce"""),
 "sara_khan": ("docx", """Sara Khan
Automation Engineer
Skills: Python, Selenium, SQL, Git, Linux, Docker, web scraping, API development
Experience: 5 years of experience writing Python automation and test frameworks.
Education: B.Tech in Computer Science"""),
}


def write_pdf(path, text):
    c = canvas.Canvas(str(path), pagesize=A4)
    y = 800
    for line in text.splitlines():
        c.drawString(50, y, line[:100])
        y -= 18
    c.save()


for name, (fmt, text) in RESUMES.items():
    path = OUT / f"{name}.{fmt}"
    if fmt == "txt":
        path.write_text(text, encoding="utf-8")
    elif fmt == "docx":
        doc = Document()
        for line in text.splitlines():
            doc.add_paragraph(line)
        doc.save(path)
    else:
        write_pdf(path, text)
print(f"Created {len(RESUMES)} synthetic resumes in {OUT}/")
