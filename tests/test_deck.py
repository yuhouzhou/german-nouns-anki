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

from src.generator import create_noun_subdecks, export_package, load_nouns_from_json
from src.models import FULL_SCREEN_CSS


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


if __name__ == "__main__":
    test_single_noun_sample_generation()
    test_master_bundle_generation()
    test_color_coding_css()
    print("✅ All deck generation & APKG validation tests passed!")
