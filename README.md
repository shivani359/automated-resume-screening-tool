# Automated Resume Screening Tool

A Python tool that reads resumes (PDF, DOCX, TXT), compares them with a job description, and produces a **ranked, explainable** shortlist: score, matched skills, **missing must-have skills**, and a Shortlist / Maybe / Reject decision.

> Built as a Python course project using **100% synthetic resumes**. No real personal data or company ATS access is used.

![Ranking chart](images/ranking_chart.png)

## What problem does it solve?
A single job post can get hundreds of resumes. Recruiters spend seconds on each, so good candidates get missed. This tool does the first-pass sort automatically and shows *why* each candidate scored the way they did, so a human can make the final call.

## Features
- Text extraction from PDF (`pdfplumber`), DOCX (`python-docx`) and TXT
- Cleaning (links, emails, phones, stop words) that keeps `c++` / `c#`
- Skill extraction from an editable skills database with aliases (`postgres` -> `sql`)
- Job description parsing into **required** vs **preferred** skills + minimum years
- Hybrid score: skill coverage + TF-IDF cosine similarity + experience
- Must-have gap flags, CSV + text reports, chart, optional Streamlit dashboard

## Workflow
```
resume upload -> text extraction -> cleaning -> skill extraction
      -> job description matching -> score -> shortlist/reject -> report
```

## Quick start
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python generate_samples.py      # creates synthetic resumes in resumes/
python main.py                  # runs the pipeline -> outputs/
streamlit run app.py            # optional dashboard
```

## Folder structure
| Folder / file | Purpose |
|---|---|
| `resumes/` | Input resumes (synthetic samples included) |
| `data/` | `job_description.txt` and `skills.csv` (skills database) |
| `src/` | `extractor.py`, `cleaner.py`, `skills.py`, `scorer.py`, `report.py` |
| `outputs/` | Generated CSV and text reports |
| `images/` | Charts and screenshots for this README |
| `docs/` | Step-by-step guide, interview prep |
| `main.py` / `app.py` | Command-line and Streamlit entry points |

## How the score works (0-100)
| Part | Weight | Meaning |
|---|---|---|
| Required-skill coverage | 50% | Share of must-have skills found |
| TF-IDF cosine similarity | 25% | Overall wording overlap with the JD |
| Preferred-skill coverage | 10% | Nice-to-have skills found |
| Experience | 15% | Years found vs years requested |

**Shortlisted** = score >= 60 **and** at least 60% of required skills present. **Maybe** = score >= 45. Otherwise **Rejected**. Weights and thresholds are constants at the top of `src/scorer.py`.

## Sample result
| Rank | Candidate | Score | Decision | Missing required |
|---|---|---|---|---|
| 1 | aarav_sharma.pdf | 90.0 | Shortlisted | - |
| 2 | ananya_rao.txt | 78.3 | Shortlisted | - |
| 3 | diya_patel.docx | 75.2 | Shortlisted | - |
| 4 | sara_khan.docx | 63.6 | Shortlisted | pandas |
| 5 | meera_nair.pdf | 62.5 | Shortlisted | rest api |
| 6 | rohan_verma.txt | 34.4 | Rejected | pandas, rest api, sql |
| 7 | kabir_singh.docx | 26.8 | Rejected | git, pandas, python, rest api |
| 8 | vikram_joshi.pdf | 1.4 | Rejected | everything |

## Limitations (be honest about these)
- Keyword matching can miss skills written in unusual ways; the alias list helps but isn't complete
- Scanned (image-only) PDFs return no text; OCR (e.g. Tesseract) would be needed
- "Years of experience" is a simple regex, not a date-range calculator
- **Fairness:** automated screening can encode bias. This tool never uses names, gender, age or photos, and it is designed to *assist* a human reviewer, not replace one

## Future improvements
- Semantic matching with sentence embeddings (handles synonyms)
- FastAPI backend + Next.js recruiter dashboard (the advanced version)
- Experience from date ranges, OCR for scanned PDFs, unit tests with pytest

## License
MIT
