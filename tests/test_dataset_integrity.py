"""
Dataset Integrity & Quality Assurance Tests.
Validates all CEFR noun datasets (A1, A2, B1, B2, C1) for completeness and correctness.
"""

import sys
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from src.rules import get_gender_rule, get_plural_rule, get_highlighted_plural

DATA_DIR = PROJECT_ROOT / "data"


def test_datasets_integrity():
    level_files = [
        "nouns_a1.json",
        "nouns_a2.json",
        "nouns_b1.json",
        "nouns_b2.json",
        "nouns_c1.json",
        "nouns_a1_to_c1.json"
    ]

    for filename in level_files:
        file_path = DATA_DIR / filename
        assert file_path.exists(), f"Missing dataset file: {file_path}"

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, list), f"Expected list in {filename}, got {type(data)}"
        assert len(data) > 0, f"Dataset {filename} is empty"

        seen_nouns = set()

        for idx, item in enumerate(data):
            # Check required keys
            for key in ["noun", "article", "plural", "meaning", "level"]:
                assert key in item, f"Missing key '{key}' in {filename} at index {idx}: {item}"
                if key != "plural" or (not item.get("singular_only") and not item.get("plural_only")):
                    assert item[key], f"Empty value for '{key}' in {filename} at index {idx}: {item}"

            noun = item["noun"].strip()
            article = item["article"].strip().lower()
            plural = item["plural"].strip()
            level = item["level"].strip().upper()

            # Validate article (including der/die for nominalized adjectives)
            assert article in {"der", "die", "das", "der/die"}, f"Invalid article '{article}' for '{noun}' in {filename}"

            # Validate level
            assert level in {"A1", "A2", "B1", "B2", "C1"}, f"Invalid level '{level}' for '{noun}' in {filename}"

            # Check uniqueness of (noun, article) within single-level files
            if filename != "nouns_a1_to_c1.json":
                entry_key = (noun.lower(), article.lower())
                assert entry_key not in seen_nouns, f"Duplicate entry '{noun}' with article '{article}' in {filename}"
                seen_nouns.add(entry_key)

            # Test rule execution
            g_rule = get_gender_rule(noun, article, meaning=item.get("meaning", ""))
            assert isinstance(g_rule, dict)
            assert "summary" in g_rule
            assert "detail" in g_rule

            p_rule = get_plural_rule(noun, article, plural)
            assert isinstance(p_rule, dict)
            assert "summary" in p_rule
            assert "detail" in p_rule

            # Test highlighted plural generation
            highlighted_p = get_highlighted_plural(noun, plural)
            assert isinstance(highlighted_p, str)
            if plural:
                assert len(highlighted_p) > 0


def test_special_noun_classes():
    """Verifies that Singulariatantum and Pluraliatantum are correctly represented in datasets."""
    with open(DATA_DIR / "nouns_a1.json", "r", encoding="utf-8") as f:
        a1_nouns = {n["noun"]: n for n in json.load(f)}

    # 1. Singular-Only: das Ausland, die Milch, die Butter
    assert "Ausland" in a1_nouns
    assert a1_nouns["Ausland"]["article"] == "das"
    assert a1_nouns["Ausland"]["plural"] == ""
    assert a1_nouns["Ausland"].get("singular_only") is True

    assert "Milch" in a1_nouns
    assert a1_nouns["Milch"]["article"] == "die"
    assert a1_nouns["Milch"]["plural"] == ""
    assert a1_nouns["Milch"].get("singular_only") is True

    # 2. Plural-Only: die Eltern, die Leute, die Geschwister
    assert "Eltern" in a1_nouns
    assert a1_nouns["Eltern"]["article"] == "die"
    assert a1_nouns["Eltern"]["plural"] == ""
    assert a1_nouns["Eltern"].get("plural_only") is True

    assert "Leute" in a1_nouns
    assert a1_nouns["Leute"]["article"] == "die"
    assert a1_nouns["Leute"]["plural"] == ""
    assert a1_nouns["Leute"].get("plural_only") is True

    assert "Geschwister" in a1_nouns
    assert a1_nouns["Geschwister"]["article"] == "die"
    assert a1_nouns["Geschwister"]["plural"] == ""
    assert a1_nouns["Geschwister"].get("plural_only") is True

    # 3. Regular & Null-Plural: der Hund, der Koffer, das Mädchen
    assert a1_nouns["Hund"]["plural"] == "Hunde"
    assert a1_nouns["Koffer"]["plural"] == "Koffer"
    assert a1_nouns["Mädchen"]["plural"] == "Mädchen"

    print("✅ Verified special noun classes (Singulariatantum & Pluraliatantum)!")


def test_homonyms_nominalized_adjectives_and_double_plurals():
    """Verifies homonyms, nominalized adjectives, and double plurals."""
    with open(DATA_DIR / "nouns_a1.json", "r", encoding="utf-8") as f:
        a1_nouns = json.load(f)
    with open(DATA_DIR / "nouns_a2.json", "r", encoding="utf-8") as f:
        a2_nouns = json.load(f)
    with open(DATA_DIR / "nouns_b1.json", "r", encoding="utf-8") as f:
        b1_nouns = json.load(f)

    # 1. Nominalized Adjectives (der/die)
    a1_nom_adjs = {n["noun"]: n for n in a1_nouns if n.get("nominalized_adj")}
    assert "Erwachsene" in a1_nom_adjs
    assert a1_nom_adjs["Erwachsene"]["article"] == "der/die"
    assert a1_nom_adjs["Erwachsene"]["plural"] == "Erwachsenen"

    assert "Jugendliche" in a1_nom_adjs
    assert a1_nom_adjs["Jugendliche"]["article"] == "der/die"
    assert a1_nom_adjs["Jugendliche"]["plural"] == "Jugendlichen"

    assert "Bekannte" in a1_nom_adjs
    assert a1_nom_adjs["Bekannte"]["article"] == "der/die"

    # 2. Homonyms with different gender and meaning
    a1_bands = [n for n in a1_nouns if n["noun"] == "Band"]
    a2_bands = [n for n in a2_nouns if n["noun"] == "Band"]
    b1_bands = [n for n in b1_nouns if n["noun"] == "Band"]

    assert len(a1_bands) == 1 and a1_bands[0]["article"] == "die"  # die Band (music group)
    assert len(a2_bands) == 1 and a2_bands[0]["article"] == "das"  # das Band (ribbon/tape)
    assert len(b1_bands) == 1 and b1_bands[0]["article"] == "der"  # der Band (book volume)

    # Gehalt
    a2_gehalt = [n for n in a2_nouns if n["noun"] == "Gehalt"]
    b1_gehalt = [n for n in b1_nouns if n["noun"] == "Gehalt"]
    assert len(a2_gehalt) == 1 and a2_gehalt[0]["article"] == "das"  # das Gehalt (salary)
    assert len(b1_gehalt) == 1 and b1_gehalt[0]["article"] == "der"  # der Gehalt (content)

    # 3. Double Plurals
    a1_words = {n["noun"]: n for n in a1_nouns if n.get("double_plural")}
    assert "Wort" in a1_words and a1_words["Wort"]["article"] == "das"
    assert "Bank" in a1_words and a1_words["Bank"]["article"] == "die"

    print("✅ Verified homonyms, nominalized adjectives, and double plurals!")


if __name__ == "__main__":
    test_datasets_integrity()
    test_special_noun_classes()
    test_homonyms_nominalized_adjectives_and_double_plurals()
