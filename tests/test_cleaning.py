"""Unit tests for USFM text cleaning, built from real cases of the corpus."""

from bible_rag.ingestion import clean_text


def test_removes_strong_numbers():
    raw = r'\w Dieu|strong="H00430"\w* \w créa|strong="H01254"\w*'
    assert clean_text(raw) == ("Dieu créa", [])


def test_word_marker_glued_to_word():
    raw = r'\wQue|strong="H01697"\w* \w la|strong="H01961"\w*'
    assert clean_text(raw)[0] == "Que la"


def test_adjacent_words_are_separated():
    raw = r'\w couvraient|strong="H03680"\w*\w l|strong="H06440"\w*’\w abîme|strong="H08415"\w*'
    assert clean_text(raw)[0] == "couvraient l’abîme"


def test_space_added_after_punctuation():
    raw = r'devant Absalon,\w son|strong="H06440"\w* \w fils|strong="H01121"\w*'
    assert clean_text(raw)[0] == "devant Absalon, son fils"


def test_footnote_is_extracted():
    raw = r"Du temps de Salmanasar,\f + \fr 1:2 \ft 2. \fq Au temps de Salmanasar\ft  : exil.\f* roi d’Assyrie"
    text, notes = clean_text(raw)
    assert text == "Du temps de Salmanasar, roi d’Assyrie"
    assert notes == ["2. Au temps de Salmanasar : exil."]


def test_cross_reference_is_removed():
    raw = r'\w de|strong="G5207"\w* \x a \xo 1.1 \xt Lu 1:31.\x*\w David|strong="G1138"\w*'
    assert clean_text(raw)[0] == "de David"


def test_character_style_keeps_text():
    raw = r"le \nd Seigneur\nd* dit"
    assert clean_text(raw)[0] == "le Seigneur dit"