"""Step 6: Save results as CSV files and a readable text report."""
from pathlib import Path

import pandas as pd


def save_reports(df: pd.DataFrame, out_dir, job_title: str = "Job") -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    full = out / "ranking_report.csv"
    df.to_csv(full, index=False)
    df[df.decision == "Shortlisted"].to_csv(out / "shortlisted.csv", index=False)
    df[df.decision == "Rejected"].to_csv(out / "rejected.csv", index=False)

    lines = [f"RESUME SCREENING REPORT - {job_title}", "=" * 60,
             f"Candidates screened : {len(df)}",
             f"Shortlisted         : {(df.decision == 'Shortlisted').sum()}",
             f"Manual review       : {df.decision.str.startswith('Maybe').sum()}",
             f"Rejected            : {(df.decision == 'Rejected').sum()}", ""]
    for _, r in df.iterrows():
        lines += [f"#{r['rank']}  {r['candidate']}  |  score {r['score']}  |  {r['decision']}",
                  f"    matched required : {r['matched_required'] or '-'}",
                  f"    MISSING required : {r['missing_required']}",
                  f"    preferred found  : {r['matched_preferred']}",
                  f"    experience       : {r['years_experience']} yrs | education: {r['education']}", ""]
    txt = out / "summary_report.txt"
    txt.write_text("\n".join(lines), encoding="utf-8")
    return {"csv": full, "txt": txt}


def save_chart(df: pd.DataFrame, path) -> None:
    """Bar chart of scores, coloured by decision - good README screenshot."""
    import matplotlib
    matplotlib.use("Agg")  # no window needed
    import matplotlib.pyplot as plt

    colors = {"Shortlisted": "#2e7d32", "Rejected": "#c62828"}
    d = df.iloc[::-1]
    plt.figure(figsize=(9, 5))
    plt.barh(d["candidate"], d["score"], color=[colors.get(x, "#f9a825") for x in d["decision"]])
    plt.xlabel("Match score (0-100)")
    plt.title("Resume ranking (green = shortlisted, amber = review, red = rejected)")
    plt.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=150)
    plt.close()
