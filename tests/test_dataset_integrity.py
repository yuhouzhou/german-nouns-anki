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
                assert item[key], f"Empty value for '{key}' in {filename} at index {idx}: {item}"

            noun = item["noun"].strip()
            article = item["article"].strip().lower()
            plural = item["plural"].strip()
            level = item["level"].strip().upper()

            # Validate article
            assert article in {"der", "die", "das"}, f"Invalid article '{article}' for '{noun}' in {filename}"

            # Validate level
            assert level in {"A1", "A2", "B1", "B2", "C1"}, f"Invalid level '{level}' for '{noun}' in {filename}"

            # Check uniqueness within single-level files
            if filename != "nouns_a1_to_c1.json":
                assert noun not in seen_nouns, f"Duplicate noun '{noun}' in {filename}"
                seen_nouns.add(noun)

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
            assert len(highlighted_p) > 0

    print("✅ All CEFR datasets passed integrity and linguistic rule validation!")


if __name__ == "__main__":
    test_datasets_integrity()
