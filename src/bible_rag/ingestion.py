"""Download and parse a French Bible translation from eBible.org (USFM format)."""

import shutil
import urllib.request
import zipfile
from pathlib import Path
import re

# Sainte Bible néo-Crampon Libre, © 2022 Fraternité de Tibériade, CC BY-SA 4.0
TRANSLATION_ID = "francl"
USFM_URL = f"https://ebible.org/Scriptures/{TRANSLATION_ID}_usfm.zip"
USER_AGENT = "bible-rag/0.1 (+https://github.com/RafaelROMERA0906/Bible-RAG)"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
ZIP_PATH = RAW_DIR / f"{TRANSLATION_ID}_usfm.zip"
USFM_DIR = RAW_DIR / f"{TRANSLATION_ID}_usfm"

# --- USFM cleaning ------------------------------------------------------------

# Blocks removed together with their content (non-greedy: stop at the first closing tag)
FOOTNOTE_RE = re.compile(r"\\f\s.*?\\f\*")
CROSS_REF_RE = re.compile(r"\\x\s.*?\\x\*")
QUOTE_REF_RE = re.compile(r"\\rq\s.*?\\rq\*")
ALT_VERSE_RE = re.compile(r"\\va\s.*?\\va\*")
FOOTNOTE_REF_RE = re.compile(r"\\fr\s[^\\]*")

# Word-level markup: \w word|strong="..."\w*  (also \+w, and \w glued to the word)
ADJACENT_WORDS_RE = re.compile(r"(\\\+?w\*)(\\\+?w)")
WORD_RE = re.compile(r"\\\+?w\s?([^|\\]*)(?:\|[^\\]*)?\\\+?w\*")

# Any remaining marker (\nd, \nd*, \+qt, \add*...): removed, text kept
MARKER_RE = re.compile(r"\\\+?[a-z]+\d*(?:\*|\s?)")

# Typography fixes
PUNCT_LETTER_RE = re.compile(r"([,;.!?])(?=[^\W\d_])")
SPACES_RE = re.compile(r"\s+")


def _strip_markers(text: str) -> str:
    """Remove word-level and character-level USFM markers, keep the text."""
    text = ADJACENT_WORDS_RE.sub(r"\1 \2", text)
    text = WORD_RE.sub(r"\1", text)
    text = MARKER_RE.sub("", text)
    text = PUNCT_LETTER_RE.sub(r"\1 ", text)
    return SPACES_RE.sub(" ", text).strip()


def _clean_footnote(note: str) -> str:
    """Turn a raw \\f ... \\f* block into plain text."""
    note = FOOTNOTE_REF_RE.sub("", note)
    note = note.removeprefix("\\f").removesuffix("\\f*").strip().removeprefix("+")
    return _strip_markers(note)


def clean_text(raw: str) -> tuple[str, list[str]]:
    """Clean a USFM text fragment. Return the clean text and its footnotes."""
    footnotes = [_clean_footnote(note) for note in FOOTNOTE_RE.findall(raw)]
    text = FOOTNOTE_RE.sub("", raw)
    text = CROSS_REF_RE.sub("", text)
    text = QUOTE_REF_RE.sub("", text)
    text = ALT_VERSE_RE.sub("", text)
    return _strip_markers(text), footnotes

def download_usfm(force: bool = False) -> Path:
    """Download and extract the USFM archive. Skip if already present."""
    if USFM_DIR.exists() and not force:
        print(f"Data already present in {USFM_DIR}, skipping download.")
        return USFM_DIR

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {USFM_URL} ...")
    request = urllib.request.Request(USFM_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response, open(ZIP_PATH, "wb") as file:
        shutil.copyfileobj(response, file)

    with zipfile.ZipFile(ZIP_PATH) as archive:
        archive.extractall(USFM_DIR)

    n_files = len(list(USFM_DIR.glob("*.usfm")))
    print(f"Extracted {n_files} USFM files to {USFM_DIR}")
    return USFM_DIR


if __name__ == "__main__":
    download_usfm()