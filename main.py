"""Run the whole pipeline from the command line:

    python main.py
    python main.py --resumes resumes --jd data/job_description.txt
"""
import argparse
from pathlib import Path

from src.extractor import load_resumes
from src.report import save_chart, save_reports
from src.scorer import screen
from src.skills import load_skill_db, parse_job_description


def main():
    ap = argparse.ArgumentParser(description="Automated Resume Screening Tool")
    ap.add_argument("--resumes", default="resumes")
    ap.add_argument("--jd", default="data/job_description.txt")
    ap.add_argument("--skills", default="data/skills.csv")
    ap.add_argument("--out", default="outputs")
    args = ap.parse_args()

    skill_db = load_skill_db(args.skills)
    jd_text = Path(args.jd).read_text(encoding="utf-8")
    required, preferred, years = parse_job_description(jd_text, skill_db)
    print(f"Required : {sorted(required)}\nPreferred: {sorted(preferred)}\nMin years: {years}\n")

    resumes = load_resumes(args.resumes)
    if not resumes:
        raise SystemExit("No resumes found. Run `python generate_samples.py` first.")

    df = screen(resumes, jd_text, required, preferred, years, skill_db)
    paths = save_reports(df, args.out, job_title=jd_text.splitlines()[0])
    save_chart(df, "images/ranking_chart.png")
    print(df[["rank", "candidate", "score", "decision", "missing_required"]].to_string(index=False))
    print(f"\nSaved: {paths['csv']} and {paths['txt']}")


if __name__ == "__main__":
    main()
