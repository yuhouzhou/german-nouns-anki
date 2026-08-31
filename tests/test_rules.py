"""
Unit tests for German Gender and Plural Rule Engine.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from src.rules import get_gender_rule, get_plural_rule


def test_feminine_suffixes():
    # -keit
    r = get_gender_rule("Möglichkeit", "die")
    assert r["article"] == "die"
    assert "Suffix -keit" in r["rule_name"]
    assert "100%" in r["confidence"]

    # -heit
    r = get_gender_rule("Freiheit", "die")
    assert "Suffix -heit" in r["rule_name"]

    # -ung
    r = get_gender_rule("Wohnung", "die")
    assert "Suffix -ung" in r["rule_name"]

    # -schaft
    r = get_gender_rule("Freundschaft", "die")
    assert "Suffix -schaft" in r["rule_name"]

    # -tät
    r = get_gender_rule("Universität", "die")
    assert "Suffix -tät" in r["rule_name"]

    # -ion
    r = get_gender_rule("Station", "die")
    assert "Suffix -ion" in r["rule_name"]

    # -in
    r = get_gender_rule("Lehrerin", "die")
    assert "Suffix -in" in r["rule_name"]


def test_masculine_suffixes_and_semantics():
    # -ismus
    r = get_gender_rule("Optimismus", "der")
    assert r["article"] == "der"
    assert "Suffix -ismus" in r["rule_name"]

    # -ling
    r = get_gender_rule("Schmetterling", "der")
    assert "Suffix -ling" in r["rule_name"]

    # -ist
    r = get_gender_rule("Polizist", "der")
    assert "Suffix -ist" in r["rule_name"]

    # -er (agent)
    r = get_gender_rule("Lehrer", "der")
    assert "Suffix -er" in r["rule_name"]

    # Seasons
    r = get_gender_rule("Sommer", "der")
    assert "Seasons" in r["rule_name"]

    # Days
    r = get_gender_rule("Montag", "der")
    assert "Days of the Week" in r["rule_name"]

    # Weather
    r = get_gender_rule("Regen", "der")
    assert "Precipitation & Weather" in r["rule_name"]


def test_neuter_suffixes_and_prefixes():
    # -chen
    r = get_gender_rule("Mädchen", "das")
    assert r["article"] == "das"
    assert "Diminutive Suffix -chen" in r["rule_name"]

    # -lein
    r = get_gender_rule("Fräulein", "das")
    assert "Diminutive Suffix -lein" in r["rule_name"]

    # -ment
    r = get_gender_rule("Dokument", "das")
    assert "Suffix -ment" in r["rule_name"]

    # -um
    r = get_gender_rule("Museum", "das")
    assert "Suffix -um" in r["rule_name"]

    # Collective Ge-...
    r = get_gender_rule("Gebäude", "das")
    assert "Prefix Ge-..." in r["rule_name"]


def test_plural_rules():
    # Diminutive
    p = get_plural_rule("Mädchen", "das", "Mädchen")
    assert "Diminutives" in p["rule_name"]
    assert "No ending change" in p["summary"]

    # Feminine -in -> -innen
    p = get_plural_rule("Lehrerin", "die", "Lehrerinnen")
    assert "-innen" in p["rule_name"]

    # S-plural
    p = get_plural_rule("Auto", "das", "Autos")
    assert "S-Plural" in p["rule_name"]

    # Feminine suffix -> -en
    p = get_plural_rule("Wohnung", "die", "Wohnungen")
    assert "Feminine Suffixes" in p["rule_name"]

    # Masculine -er -> no change
    p = get_plural_rule("Lehrer", "der", "Lehrer")
    assert "without Ending" in p["rule_name"]

    # Masculine monosyllabic +e
    p = get_plural_rule("Hund", "der", "Hunde")
    assert "Standard (+e)" in p["rule_name"]


def test_conflicting_rules():
    # die Gemeinde (Ge- prefix vs die ending in -e)
    r = get_gender_rule("Gemeinde", "die")
    assert r["article"] == "die"
    assert "Gemeinde" in r["rule_name"]
    assert "unlike neuter collective" in r["detail"]

    # die Gemeinschaft (Ge- prefix vs 100% feminine -schaft suffix)
    r = get_gender_rule("Gemeinschaft", "die")
    assert r["article"] == "die"
    assert "Suffix -schaft" in r["rule_name"]

    # das Mädchen (Female entity vs 100% neuter -chen diminutive suffix)
    r = get_gender_rule("Mädchen", "das")
    assert r["article"] == "das"
    assert "Diminutive Suffix -chen" in r["rule_name"]

def test_highlighted_plural():
    from src.rules import get_highlighted_plural
    assert get_highlighted_plural("Hund", "Hunde") == 'Hund<span class="plural-highlight">e</span>'
    assert get_highlighted_plural("Möglichkeit", "Möglichkeiten") == 'Möglichkeit<span class="plural-highlight">en</span>'
    assert get_highlighted_plural("Buch", "Bücher") == 'B<span class="plural-highlight">ü</span>ch<span class="plural-highlight">er</span>'
    assert get_highlighted_plural("Baum", "Bäume") == 'B<span class="plural-highlight">ä</span>um<span class="plural-highlight">e</span>'
    assert get_highlighted_plural("Mädchen", "Mädchen") == 'Mädchen'
    assert get_highlighted_plural("Apfel", "Äpfel") == '<span class="plural-highlight">Ä</span>pfel'


if __name__ == "__main__":
    test_feminine_suffixes()
    test_masculine_suffixes_and_semantics()
    test_neuter_suffixes_and_prefixes()
    test_plural_rules()
    test_conflicting_rules()
    test_highlighted_plural()
    print("✅ All rule engine unit tests passed!")
