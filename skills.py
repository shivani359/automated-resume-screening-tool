"""Step 3: Find skills, experience and education in text."""
import re
from pathlib import Path

import pandas as pd


def load_skill_db(path) -> dict:
    """Return {canonical_skill: [all spellings]} from data/skills.csv."""
    df = pd.read_csv(path).fillna("")
    db = {}
    for _, row in df.iterrows():
        names = [row["skill"].strip().lower()]
        names += [a.strip().lower() for a in str(row["aliases"]).split("|") if a.strip()]
        db[row["skill"].strip().lower()] = names
    return db


def _pattern(term: str) -> re.Pattern:
    # lookarounds stop 'java' matching inside 'javascript', and 'sql' inside 'mysql'
    return re.compile(r"(?<![a-z0-9+#])" + re.escape(term) + r"(?![a-z0-9+#])")


def extract_skills(text: str, skill_db: dict) -> set:
    """Return the set of canonical skills found in (already lower-cased) text."""
    found = set()
    for skill, names in skill_db.items():
        if any(_pattern(n).search(text) for n in names):
            found.add(skill)
    return found


def extract_years_experience(text: str) -> float:
    """Largest 'N years' / 'N+ years' mention. Simple but effective for a demo."""
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)", text)
    return max((float(m) for m in matches), default=0.0)


def extract_education(text: str) -> str:
    levels = [("phd", r"\bph\.?d\b|doctorate"), ("masters", r"\bmaster'?s?\b|\bm\.?sc\b|\bm\.?tech\b|\bmba\b"),
              ("bachelors", r"\bbachelor'?s?\b|\bb\.?sc\b|\bb\.?tech\b|\bb\.?e\b|\bb\.?ca\b")]
    for name, pat in levels:
        if re.search(pat, text):
            return name
    return "not found"


def parse_job_description(jd_text: str, skill_db: dict):
    """Split JD skills into required vs preferred using the section labels.
    Fallback: if no labels exist, every skill in the JD is treated as required."""
    low = jd_text.lower()
    req_part = re.search(r"required skills?:(.*?)(?:\n\s*\n|preferred skills?:|$)", low, re.S)
    pref_part = re.search(r"(?:preferred|nice[- ]to[- ]have) skills?:(.*?)(?:\n\s*\n|$)", low, re.S)
    required = extract_skills(req_part.group(1), skill_db) if req_part else set()
    preferred = extract_skills(pref_part.group(1), skill_db) if pref_part else set()
    if not required and not preferred:
        required = extract_skills(low, skill_db)
    preferred -= required
    years = extract_years_experience(low)
    return required, preferred, years
