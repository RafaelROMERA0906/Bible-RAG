"""Download and parse a French Bible translation from eBible.org (USFM format)."""

import shutil
import urllib.request
import zipfile
from pathlib import Path

# Sainte Bible néo-Crampon Libre, © 2022 Fraternité de Tibériade, CC BY-SA 4.0
TRANSLATION_ID = "francl"
USFM_URL = f"https://ebible.org/Scriptures/{TRANSLATION_ID}_usfm.zip"
USER_AGENT = "bible-rag/0.1 (+https://github.com/RafaelROMERA0906/Bible-RAG)"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
ZIP_PATH = RAW_DIR / f"{TRANSLATION_ID}_usfm.zip"
USFM_DIR = RAW_DIR / f"{TRANSLATION_ID}_usfm"


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