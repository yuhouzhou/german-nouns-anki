#!/usr/bin/env python3
"""
CLI Tool to generate German Noun Gender & Plural Anki Decks (A1 to C1).
Supports building individual level packages and the master CEFR complete bundle.
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from src.generator import (
    create_noun_subdecks,
    create_hierarchical_cefr_decks,
    export_package,
    load_nouns_from_json
)

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"


def build_single_level(level: str):
    """Builds a single CEFR level package (Gender & Plural subdecks)."""
    level = level.lower().strip()
    json_file = DATA_DIR / f"nouns_{level}.json"
    if not json_file.exists():
        print(f"❌ Error: Dataset {json_file} not found!")
        return

    nouns = load_nouns_from_json(str(json_file))
    deck_name = f"German Nouns ({level.upper()})"
    output_file = OUTPUT_DIR / f"german_nouns_{level.upper()}.apkg"

    print(f"📦 Building {level.upper()} ({len(nouns)} nouns -> {len(nouns)*2} cards)...")
    decks = create_noun_subdecks(deck_name, nouns)
    export_package(decks, str(output_file))
    print(f"✅ Exported: {output_file}")
    return output_file


def build_all_levels():
    """Builds all individual level packages AND the master complete bundle."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    levels = ["a1", "a2", "b1", "b2", "c1"]
    level_datasets = {}
    total_nouns = 0

    print("🚀 ===============================================")
    print("🚀 Building German Noun Decks (CEFR A1 to C1)")
    print("🚀 ===============================================\n")

    # 1. Build individual level packages
    for lvl in levels:
        json_file = DATA_DIR / f"nouns_{lvl}.json"
        if json_file.exists():
            nouns = load_nouns_from_json(str(json_file))
            level_datasets[lvl.upper()] = nouns
            total_nouns += len(nouns)
            build_single_level(lvl)

    # 2. Build Master Complete Package
    print(f"\n📦 Building Master Complete Package: German Nouns (A1-C1 Complete)...")
    master_decks = create_hierarchical_cefr_decks(
        "German Nouns (A1-C1 Complete)",
        level_datasets
    )
    master_output = OUTPUT_DIR / "german_nouns_A1_to_C1_complete.apkg"
    export_package(master_decks, str(master_output))
    print(f"🌟 Master Complete Deck Exported: {master_output}")
    print(f"🎉 Total: {total_nouns} nouns -> {total_nouns * 2} cards across 10 subdecks!\n")


def main():
    parser = argparse.ArgumentParser(description="Generate German Noun Anki Decks (Gender & Plural).")
    parser.add_argument("--all", action="store_true", help="Build all level decks (A1 to C1) and master package.")
    parser.add_argument("--level", type=str, choices=["a1", "a2", "b1", "b2", "c1"], help="Build a specific level deck.")
    parser.add_argument("--sample", action="store_true", help="Build the 1-noun sample deck (Iteration 1).")
    parser.add_argument("--showcase", action="store_true", help="Build the rule showcase deck.")
    parser.add_argument("--input", type=str, help="Path to custom input JSON file.")
    parser.add_argument("--output", type=str, help="Path to custom output .apkg file.")
    parser.add_argument("--name", type=str, default="German Nouns::Gender & Plural", help="Custom deck name in Anki.")

    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.all:
        build_all_levels()
        return

    if args.level:
        build_single_level(args.level)
        return

    if args.sample:
        input_file = DATA_DIR / "sample.json"
        output_file = OUTPUT_DIR / "german_nouns_sample_iteration1.apkg"
        deck_name = "German Nouns (Sample)"
        nouns = load_nouns_from_json(str(input_file))
        decks = create_noun_subdecks(deck_name, nouns)
        export_package(decks, str(output_file))
        print(f"✅ Exported sample deck: {output_file}")
        return

    if args.showcase:
        input_file = DATA_DIR / "showcase.json"
        output_file = OUTPUT_DIR / "german_nouns_rule_showcase.apkg"
        deck_name = "German Nouns (Rule Showcase)"
        nouns = load_nouns_from_json(str(input_file))
        decks = create_noun_subdecks(deck_name, nouns)
        export_package(decks, str(output_file))
        print(f"✅ Exported showcase deck: {output_file}")
        return

    if args.input:
        input_file = Path(args.input)
        output_file = Path(args.output) if args.output else OUTPUT_DIR / f"{input_file.stem}.apkg"
        nouns = load_nouns_from_json(str(input_file))
        decks = create_noun_subdecks(args.name, nouns)
        export_package(decks, str(output_file))
        print(f"✅ Exported {len(nouns)} nouns to {output_file}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
