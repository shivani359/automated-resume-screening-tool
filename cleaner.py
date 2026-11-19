"""Step 2: Clean raw text so that matching is fair."""
import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def basic_clean(text: str) -> str:
    """Light cleaning used for skill matching.
    Keeps symbols like + and # so 'c++' and 'c#' survive."""
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)   # links
    text = re.sub(r"\S+@\S+", " ", text)                 # emails
    text = re.sub(r"\+?\d[\d\s\-()]{8,}\d", " ", text)   # phone numbers
    text = re.sub(r"[^a-z0-9+#.\-/\s]", " ", text)       # odd symbols
    return re.sub(r"\s+", " ", text).strip()


def clean_for_tfidf(text: str) -> str:
    """Heavier cleaning for TF-IDF: also drop stop words (the, and, is...)."""
    text = basic_clean(text)
    words = re.findall(r"[a-z0-9+#]+(?:[.\-/][a-z0-9+#]+)*", text)
    return " ".join(w for w in words if w not in ENGLISH_STOP_WORDS and len(w) > 1)
