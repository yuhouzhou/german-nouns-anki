"""
Integration tests for Anki package (.apkg) generation and card structure.
"""

import sys
import zipfile
import sqlite3
import tempfile
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from src.generator import create_noun_subdecks, export_package, load_nouns_from_json, create_notes_for_noun
from src.models import FULL_SCREEN_CSS, create_gender_model, create_plural_model


def test_single_noun_sample_generation():
    """
    Verifies that 1 noun produces 2 subdecks and 2 distinct cards (Gender & Plural).
    """
    sample_file = PROJECT_ROOT / "data" / "sample.json"
    nouns = load_nouns_from_json(str(sample_file))
    assert len(nouns) == 1, "Sample data should have 1 noun for Iteration 1"

    decks = create_noun_subdecks("Test German Noun Deck", nouns)
    assert len(decks) == 2, "Should create 2 subdecks (Gender & Plural)"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        apkg_path = Path(tmpdir) / "test_sample.apkg"
        export_package(decks, str(apkg_path))
        assert apkg_path.exists(), "APKG file should be created"

        # Unpack .apkg (zip file)
        with zipfile.ZipFile(apkg_path, "r") as zf:
            namelist = zf.namelist()
            assert "collection.anki2" in namelist or "collection.anki21" in namelist

            db_name = "collection.anki2" if "collection.anki2" in namelist else "collection.anki21"
            zf.extract(db_name, tmpdir)
            db_path = Path(tmpdir) / db_name

            # Inspect SQLite database
            conn = sqlite3.connect(str(db_path))
            cur = conn.cursor()

            # Check notes table (2 notes: 1 Gender note, 1 Plural note)
            cur.execute("SELECT count(*) FROM notes")
            note_count = cur.fetchone()[0]
            assert note_count == 2, f"Expected 2 notes, got {note_count}"

            # Check cards table (must be exactly 2 cards: 1 for Gender subdeck, 1 for Plural subdeck)
            cur.execute("SELECT count(*) FROM cards")
            card_count = cur.fetchone()[0]
            assert card_count == 2, f"Expected 2 cards, got {card_count}"

            conn.close()


def test_color_coding_css():
    """
    Verifies that the CSS styling includes color coding for der (blue), die (red), das (green).
    """
    assert ".der" in FULL_SCREEN_CSS
    assert "#0284c7" in FULL_SCREEN_CSS
    assert ".die" in FULL_SCREEN_CSS
    assert "#dc2626" in FULL_SCREEN_CSS
    assert ".das" in FULL_SCREEN_CSS
    assert "#16a34a" in FULL_SCREEN_CSS


def test_master_bundle_generation():
    """
    Verifies that create_hierarchical_cefr_decks properly builds subdecks across levels.
    """
    from src.generator import create_hierarchical_cefr_decks

    test_data = {
        "A1": [{"noun": "Hund", "article": "der", "plural": "Hunde", "meaning": "dog", "level": "A1"}],
        "A2": [{"noun": "Katze", "article": "die", "plural": "Katzen", "meaning": "cat", "level": "A2"}]
    }

    decks = create_hierarchical_cefr_decks("Test Master", test_data)
    assert len(decks) == 4, f"Expected 4 subdecks (2 levels * 2), got {len(decks)}"

    with tempfile.TemporaryDirectory() as tmpdir:
        apkg_path = Path(tmpdir) / "test_master.apkg"
        export_package(decks, str(apkg_path))
        assert apkg_path.exists()

        with zipfile.ZipFile(apkg_path, "r") as zf:
            db_name = "collection.anki2" if "collection.anki2" in zf.namelist() else "collection.anki21"
            zf.extract(db_name, tmpdir)
            conn = sqlite3.connect(str(Path(tmpdir) / db_name))
            cur = conn.cursor()

            cur.execute("SELECT count(*) FROM notes")
            assert cur.fetchone()[0] == 4

            cur.execute("SELECT count(*) FROM cards")
            assert cur.fetchone()[0] == 4

            conn.close()


def test_singular_only_and_plural_only_deck_generation():
    """
    Verifies Option 1:
    - Gender deck has clean notes (no plural clutter on gender card).
    - Plural deck generates dedicated cards showing '— (kein Plural)' for Singulariatantum (das Ausland)
      and 'die Eltern (nur Plural)' for Pluraliatantum.
    """
    test_nouns = [
        {"noun": "Ausland", "article": "das", "plural": "", "meaning": "abroad", "level": "A1", "singular_only": True},
        {"noun": "Eltern", "article": "die", "plural": "", "meaning": "parents", "level": "A1", "plural_only": True},
        {"noun": "Hund", "article": "der", "plural": "Hunde", "meaning": "dog", "level": "A1"}
    ]

    decks = create_noun_subdecks("Special Noun Test Deck", test_nouns)
    assert len(decks) == 2, "Should create 2 subdecks"
    gender_deck, plural_deck = decks[0], decks[1]

    # Gender deck should have 3 notes (Ausland, Eltern, Hund)
    assert len(gender_deck.notes) == 3
    # Plural deck should have 3 notes (Ausland, Eltern, Hund)
    assert len(plural_deck.notes) == 3

    with tempfile.TemporaryDirectory() as tmpdir:
        apkg_path = Path(tmpdir) / "test_special.apkg"
        export_package(decks, str(apkg_path))
        assert apkg_path.exists()

        with zipfile.ZipFile(apkg_path, "r") as zf:
            db_name = "collection.anki2" if "collection.anki2" in zf.namelist() else "collection.anki21"
            zf.extract(db_name, tmpdir)
            conn = sqlite3.connect(str(Path(tmpdir) / db_name))
            cur = conn.cursor()

            # Total notes = 6 (3 gender + 3 plural)
            cur.execute("SELECT count(*) FROM notes")
            assert cur.fetchone()[0] == 6

            # Total cards = 6
            cur.execute("SELECT count(*) FROM cards")
            assert cur.fetchone()[0] == 6

            # Check notes content
            cur.execute("SELECT flds FROM notes")
            rows = cur.fetchall()
            
            gender_notes = {r[0].split("\x1f")[0]: r[0].split("\x1f") for r in rows if len(r[0].split("\x1f")) == 9}
            plural_notes = {r[0].split("\x1f")[0]: r[0].split("\x1f") for r in rows if len(r[0].split("\x1f")) == 10}

            # Gender cards must be clean (no plural notes injected)
            assert gender_notes["Ausland"][8] == ""
            assert gender_notes["Eltern"][8] == ""
            assert gender_notes["Hund"][8] == ""

            # Plural cards must show exact forms & rules
            assert "— (kein Plural)" in plural_notes["Ausland"][3]
            assert "Singulariatantum" in plural_notes["Ausland"][6]

            assert "(nur Plural)" in plural_notes["Eltern"][3]
            assert "Pluraliatantum" in plural_notes["Eltern"][6]

            assert "Hund<span class=\"plural-highlight\">e</span>" in plural_notes["Hund"][3]

            conn.close()


def test_homonyms_nominalized_adjectives_and_double_plurals_deck():
    """Verifies that homonyms, nominalized adjectives, and double plurals produce accurate notes and cards."""
    gender_model = create_gender_model()
    plural_model = create_plural_model()

    # 1. Nominalized Adjectives: Erwachsene
    erw_data = {
        "noun": "Erwachsene",
        "article": "der/die",
        "plural": "Erwachsenen",
        "meaning": "adult",
        "level": "A1",
        "nominalized_adj": True
    }
    g_note, p_note = create_notes_for_noun(erw_data, gender_model, plural_model)
    # Gender Note
    assert g_note.fields[1] == "der / die"
    assert "Substantiviertes Adjektiv" in g_note.fields[5]
    assert "ein Erwachsener" in g_note.fields[6]
    assert "eine Erwachsene" in g_note.fields[6]
    assert g_note.fields[8] == ""  # Zero plural info on gender card!
    # Plural Note
    assert "Erwachsen" in p_note.fields[3] and "<span class=\"plural-highlight\">n</span>" in p_note.fields[3]
    assert "ohne Artikel / nach Zahlen:" in p_note.fields[3]
    assert "viele Erwachsene" in p_note.fields[3]
    assert "Substantiviertes Adjektiv" in p_note.fields[6]
    assert "Adjektiv-Deklination" in p_note.fields[7]

    # 2. Homonyms: das Band vs der Band vs die Band
    band_das = {"noun": "Band", "article": "das", "plural": "Bänder", "meaning": "ribbon", "level": "A2", "is_homonym": True}
    band_der = {"noun": "Band", "article": "der", "plural": "Bände", "meaning": "volume", "level": "B1", "is_homonym": True}
    band_die = {"noun": "Band", "article": "die", "plural": "Bands", "meaning": "music group", "level": "A1", "is_homonym": True}

    g_das, p_das = create_notes_for_noun(band_das, gender_model, plural_model)
    g_der, p_der = create_notes_for_noun(band_der, gender_model, plural_model)
    g_die, p_die = create_notes_for_noun(band_die, gender_model, plural_model)

    assert g_das.guid != g_der.guid != g_die.guid
    assert "Homonym-Verwechslungsgefahr" in g_das.fields[8]
    assert "Homonym-Verwechslungsgefahr" in g_der.fields[8]

    # 3. Double Plurals: das Wort
    wort_data = {"noun": "Wort", "article": "das", "plural": "Wörter", "meaning": "word", "level": "A1", "double_plural": True}
    _, p_wort = create_notes_for_noun(wort_data, gender_model, plural_model)
    assert "W<span class=\"plural-highlight\">ö</span>rt<span class=\"plural-highlight\">er</span>" in p_wort.fields[3]
    assert "Wort<span class=\"plural-highlight\">e</span>" in p_wort.fields[3]
    assert "Doppelplural" in p_wort.fields[6]
    assert "Einzelne Vokabeln" in p_wort.fields[7]


if __name__ == "__main__":
    test_single_noun_sample_generation()
    test_master_bundle_generation()
    test_color_coding_css()
    test_singular_only_and_plural_only_deck_generation()
    test_homonyms_nominalized_adjectives_and_double_plurals_deck()
    print("✅ All deck generation & APKG validation tests passed!")
