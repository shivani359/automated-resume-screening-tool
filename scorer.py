"""Steps 4-5: Score every resume against the job description and decide."""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .cleaner import basic_clean, clean_for_tfidf
from .skills import extract_education, extract_skills, extract_years_experience

# --- Tune these and watch the ranking change (great for your README!) -------
WEIGHTS = {"required": 0.50, "tfidf": 0.25, "preferred": 0.10, "experience": 0.15}
SHORTLIST_SCORE = 60      # overall score needed
SHORTLIST_MIN_REQ = 0.60  # share of required skills that must be present
MAYBE_SCORE = 45
# -----------------------------------------------------------------------------


def tfidf_similarity(jd_text: str, resume_texts: list) -> np.ndarray:
    """Cosine similarity (0-1) between the JD and each resume using TF-IDF.
    Unigrams + bigrams so 'machine learning' counts as one idea."""
    docs = [clean_for_tfidf(jd_text)] + [clean_for_tfidf(t) for t in resume_texts]
    matrix = TfidfVectorizer(ngram_range=(1, 2)).fit_transform(docs)
    return cosine_similarity(matrix[0:1], matrix[1:]).flatten()


def decide(score: float, req_cov: float) -> str:
    if score >= SHORTLIST_SCORE and req_cov >= SHORTLIST_MIN_REQ:
        return "Shortlisted"
    if score >= MAYBE_SCORE:
        return "Maybe (manual review)"
    return "Rejected"


def screen(resumes: dict, jd_text: str, required: set, preferred: set,
           min_years: float, skill_db: dict) -> pd.DataFrame:
    """Return a ranked DataFrame - one row per candidate."""
    names = list(resumes)
    sims = tfidf_similarity(jd_text, [resumes[n] for n in names])
    rows = []
    for name, sim in zip(names, sims):
        text = basic_clean(resumes[name])
        have = extract_skills(text, skill_db)
        years = extract_years_experience(text)

        req_hit, req_miss = sorted(required & have), sorted(required - have)
        pref_hit = sorted(preferred & have)
        req_cov = len(req_hit) / len(required) if required else 1.0
        pref_cov = len(pref_hit) / len(preferred) if preferred else 0.0
        exp_ratio = min(years / min_years, 1.0) if min_years else 1.0

        score = 100 * (WEIGHTS["required"] * req_cov + WEIGHTS["tfidf"] * min(sim * 2, 1.0)
                       + WEIGHTS["preferred"] * pref_cov + WEIGHTS["experience"] * exp_ratio)
        # *2 on similarity: raw TF-IDF cosine between a resume and a JD rarely exceeds 0.5

        rows.append({
            "candidate": name,
            "score": round(score, 1),
            "decision": decide(score, req_cov),
            "required_match_%": round(req_cov * 100),
            "matched_required": ", ".join(req_hit),
            "missing_required": ", ".join(req_miss) or "-",
            "matched_preferred": ", ".join(pref_hit) or "-",
            "years_experience": years,
            "education": extract_education(text),
            "tfidf_similarity": round(float(sim), 3),
        })
    df = pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)
    df.insert(0, "rank", df.index + 1)
    return df
