# Beginner Guide: Automated Resume Screening Tool

## 1. Project explanation
**Simple:** Imagine 200 resumes for one job. This program reads them all, checks which ones have the skills the job needs, gives each a score, and sorts them - like a very fast first-round filter.

**Technical:** A pipeline that extracts text from documents, normalises it, extracts structured features (skills, years, education) with regex and a skills dictionary, vectorises text with TF-IDF, measures cosine similarity to the job description, combines features into a weighted score, applies decision rules, and writes reports.

**How real ATS systems work:** They parse resumes into fields, match keywords/skills against the job post, apply knock-out rules ("must have X"), and rank. This project mimics that core idea in a transparent way.

**Why it matters:** Saves recruiter time, applies the same criteria to everyone, and gives a consistent first pass. The risk is bias and missed candidates, which is why humans stay in the loop.

## 2. Tech stack options
| Option | Stack | Difficulty | Output |
|---|---|---|---|
| A - Easy | Python, regex keyword count, pandas, TXT only | Beginner | CSV ranking |
| **B - Intermediate (this repo)** | A + pdfplumber, python-docx, TF-IDF, cosine similarity, skills DB, Streamlit | Beginner+ | Ranked CSV, report, chart, dashboard |
| C - Advanced | B + spaCy/sentence-transformers, FastAPI, Next.js dashboard, Docker, pytest | Hard | Web API + recruiter UI with explanations |

**Best for students: Option B.** It is complete and explainable without hiding things behind a heavy framework. Build B first, then grow it toward C.

## 3. Architecture
```
 INPUT                    PROCESSING                              OUTPUT
 -----                    ----------                              ------
 resumes/ (PDF,DOCX,TXT)-> extractor.py  -> raw text
 job_description.txt  ---> skills.py     -> required / preferred / years
 skills.csv  ------------> cleaner.py    -> clean text
                           skills.py     -> skills, years, education per resume
                           scorer.py     -> TF-IDF cosine + weighted score
                           scorer.py     -> decision rules
                           report.py     -> ranking_report.csv, shortlisted.csv,
                                            rejected.csv, summary_report.txt, chart
```

## 4. Implementation plan (11 phases)
| Phase | What to do | Why | Expected output | Common beginner mistake |
|---|---|---|---|---|
| 1 Setup | Install Python 3.10+, create venv, `pip install -r requirements.txt` | Isolated, reproducible environment | `pip list` shows libraries | Forgetting to activate the venv |
| 2 Folders | Create the structure in the README | Clean, GitHub-ready layout | Empty folders + `src/__init__.py` | Putting everything in one file |
| 3 Sample resumes | Run `generate_samples.py` | Need data without real people | 8 files in `resumes/` | Using real resumes of friends (privacy!) |
| 4 Job description | Write `data/job_description.txt` with `Required Skills:` / `Preferred Skills:` | Defines what "good" means | One text file | Writing vague requirements |
| 5 Extraction | `src/extractor.py` | Computers can't score a PDF directly | Raw text per file | Scanned PDFs return empty text |
| 6 Cleaning | `src/cleaner.py` | Noise lowers match quality | Lower-case, no links/emails | Removing `+`/`#` and breaking `c++` |
| 7 Skill matching | `src/skills.py` + `skills.csv` | Turns text into structured facts | Skill set per resume | `java` matching inside `javascript` (use word boundaries) |
| 8 Scoring | `src/scorer.py` | Combine evidence into one number | Score 0-100 | Magic weights you can't explain |
| 9 Ranking | Sort + decision rules | Actionable shortlist | Ranked DataFrame | Hard-coding thresholds with no reasoning |
| 10 Reports | `src/report.py` | Humans need readable output | CSVs, text report, chart | Not showing *why* a candidate was rejected |
| 11 GitHub | See below | Proof of work | Public repo | Committing real data or `venv/` |

## 5. Installation
**Windows**
```
python --version
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
**Mac / Linux**
```
python3 --version
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 6. Run it
```
python generate_samples.py
python main.py
streamlit run app.py
```
Take screenshots of the Streamlit page and the terminal output; save them in `images/`.

## 7. GitHub upload steps
```
git init
git add .
git commit -m "Initial commit: resume screening pipeline"
git branch -M main
git remote add origin https://github.com/<your-username>/Automated-Resume-Screening-Tool.git
git push -u origin main
```
Then: add a repo description + topics (`python`, `nlp`, `tf-idf`, `hr-tech`), pin the repo, and add a 2-line LinkedIn post linking it. Make several meaningful commits over time rather than one big upload.

## 8. Interview preparation
1. **Explain the project in 30 seconds.** "It reads resumes, extracts skills, compares them to a job description using skill coverage and TF-IDF cosine similarity, and outputs a ranked, explainable shortlist."
2. **What is TF-IDF?** Weights words by how frequent they are in a document but rare across documents, so distinctive terms matter more than common ones.
3. **What is cosine similarity?** The angle between two vectors; 1 means same direction (very similar), 0 means unrelated.
4. **Why not only TF-IDF?** It ignores must-have rules and can't tell a skill from a passing mention; combining it with explicit skill coverage gives explainable results.
5. **Why `*2` on similarity?** Resume-vs-JD cosine values are naturally low (rarely above 0.5), so I rescale to use the full range. (Be ready to say this is a heuristic.)
6. **How would you handle synonyms?** Alias list now; sentence embeddings later.
7. **How would you test it?** Unit tests for each extractor/regex, plus labelled sample resumes checked against expected decisions.
8. **What are the risks?** Bias, keyword stuffing, missed candidates. Mitigations: ignore personal attributes, keep a "Maybe" band, human final decision.
9. **How would you scale it?** FastAPI service, queue for batch parsing, database for results, caching, Docker.
10. **What would you improve next?** Embeddings, OCR, date-based experience, pytest + CI, web dashboard.
