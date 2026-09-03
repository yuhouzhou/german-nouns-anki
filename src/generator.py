"""
Deck Generator Engine for German Noun Anki Decks.
Generates full-screen subdecks for Gender and Plural with 2-tier concise + detailed rule hints,
supporting individual CEFR levels and multi-level hierarchical deck trees.
"""

import os
import json
import hashlib
from typing import List, Dict, Any, Tuple
import genanki

from src.models import create_gender_model, create_plural_model
from src.rules import (
    get_gender_rule, get_plural_rule, get_highlighted_plural,
    HOMONYM_GROUPS, CURATED_DOUBLE_PLURALS, NOMINALIZED_ADJ
)


def get_deterministic_id(key: str) -> int:
    """Generates a stable integer ID from a string key."""
    return int(hashlib.md5(key.encode("utf-8")).hexdigest()[:8], 16)


def create_notes_for_noun(
    noun_data: Dict[str, Any],
    gender_model: genanki.Model,
    plural_model: genanki.Model
) -> Tuple[genanki.Note, genanki.Note]:
    """
    Creates 2 separate notes for a German noun:
    1. A Gender Note for the Gender deck (strictly der/die/das + gender rule).
    2. A Plural Note for the Plural deck (morphological highlighting or '— (kein Plural)' for Singulariatantum).
    """
    noun = noun_data["noun"].strip()
    article = noun_data["article"].strip().lower()
    plural = noun_data.get("plural", "").strip()
    meaning = noun_data.get("meaning", "").strip()
    level = noun_data.get("level", "A1").strip().upper()
    notes = noun_data.get("notes", "").strip()
    
    is_pl_only = noun_data.get("plural_only", False)
    is_sg_only = not is_pl_only and (
        noun_data.get("singular_only", False) or not plural or plural.lower() in ("-", "kein plural", "ohne plural", "nur singular")
    )
    is_nom_adj = noun_data.get("nominalized_adj") or article in ("der/die", "der / die") or noun.lower() in NOMINALIZED_ADJ
    is_double_pl = noun_data.get("double_plural") or (noun in CURATED_DOUBLE_PLURALS and article == CURATED_DOUBLE_PLURALS[noun]["article"])

    # 1. Resolve Gender Rule
    if "gender_rule_summary" in noun_data and noun_data["gender_rule_summary"]:
        gender_rule_summary = noun_data["gender_rule_summary"]
        gender_rule_detail = noun_data.get("gender_rule_detail", "")
        gender_examples = noun_data.get("gender_rule_examples", "")
    elif "gender_rule" in noun_data and noun_data["gender_rule"]:
        gender_rule_summary = noun_data["gender_rule"]
        gender_rule_detail = ""
        gender_examples = noun_data.get("gender_rule_examples", "")
    else:
        rule_info = get_gender_rule(noun, article, meaning=meaning)
        gender_rule_summary = rule_info.get("summary", "")
        gender_rule_detail = rule_info.get("detail", "")
        gender_examples = rule_info.get("examples", "")
        
    tags = [f"level::{level}", f"gender::{article}", "german-noun"]
    if is_sg_only:
        tags.append("singulariatantum")
    if is_pl_only:
        tags.append("pluraliatantum")
    if is_nom_adj:
        tags.append("nominalized_adj")
    if is_double_pl:
        tags.append("double_plural")
    if noun in HOMONYM_GROUPS or noun_data.get("is_homonym"):
        tags.append("homonym")
        if not notes and noun in HOMONYM_GROUPS:
            notes = HOMONYM_GROUPS[noun]["note"]

    if "tags" in noun_data:
        tags.extend(noun_data["tags"])

    # Format article display string (e.g. 'der / die' with spacing for dual gender)
    article_display = "der / die" if is_nom_adj else article

    # 1. Gender Note (Kept 100% clean - no plural notes injected)
    gender_guid = genanki.guid_for(f"german_gender_{noun}_{article}_{level}")
    gender_note = genanki.Note(
        model=gender_model,
        fields=[
            noun,
            article_display,
            plural,
            meaning,
            level,
            gender_rule_summary,
            gender_rule_detail,
            gender_examples,
            notes
        ],
        tags=tags,
        guid=gender_guid
    )

    # 2. Plural Note (Format display & rule for Plural deck)
    if is_sg_only:
        plural_highlighted = '<style>.plural-article-neutral { display: none !important; }</style><span style="color: #64748b; font-style: italic; font-weight: 700;">— (kein Plural)</span>'
        p_rule_info = get_plural_rule(noun, article, "")
    elif is_pl_only:
        plural_highlighted = f'{noun} <span style="font-size: 16px; color: #64748b; font-style: italic; font-weight: normal;">(nur Plural)</span>'
        p_rule_info = get_plural_rule(noun, article, "", is_pl_only=True)
    elif is_nom_adj:
        p_rule_info = get_plural_rule(noun, article, plural)
        plural_highlighted = (
            f'{noun}<span class="plural-highlight">n</span>'
            f'<div style="font-size: 20px; font-weight: 500; color: #64748b; margin-top: 8px;">'
            f'<i>(ohne Artikel / nach Zahlen:</i> <span style="color: #0284c7; font-weight: 600;">viele {noun}</span><i>)</i>'
            f'</div>'
        )
    elif is_double_pl:
        dp = CURATED_DOUBLE_PLURALS[noun]
        pl1, pl2 = dp["plurals"]
        hl1 = get_highlighted_plural(noun, pl1)
        hl2 = get_highlighted_plural(noun, pl2)
        plural_highlighted = (
            f'<style>.plural-article-neutral {{ display: none !important; }}</style>'
            f'<span class="plural-article-neutral">die</span> <span class="noun">{hl1}</span> '
            f'<span style="font-size: 24px; color: #94a3b8; font-weight: normal; margin: 0 6px;">/</span> '
            f'<span class="plural-article-neutral">die</span> <span class="noun">{hl2}</span>'
        )
        p_rule_info = get_plural_rule(noun, article, plural)
    else:
        hl = noun_data.get("plural_highlighted") or get_highlighted_plural(noun, plural)
        plural_highlighted = hl
        if "plural_rule_summary" in noun_data and noun_data["plural_rule_summary"]:
            p_rule_info = {
                "summary": noun_data["plural_rule_summary"],
                "detail": noun_data.get("plural_rule_detail", ""),
                "examples": noun_data.get("plural_rule_examples", "")
            }
        else:
            p_rule_info = get_plural_rule(noun, article, plural)

    plural_rule_summary = p_rule_info.get("summary", "")
    plural_rule_detail = p_rule_info.get("detail", "")
    plural_examples = p_rule_info.get("examples", "")

    plural_guid = genanki.guid_for(f"german_plural_{noun}_{article}_{level}")
    plural_note = genanki.Note(
        model=plural_model,
        fields=[
            noun,
            article_display,
            plural,
            plural_highlighted,
            meaning,
            level,
            plural_rule_summary,
            plural_rule_detail,
            plural_examples,
            notes
        ],
        tags=tags,
        guid=plural_guid
    )

    return gender_note, plural_note


def create_noun_subdecks(
    base_deck_name: str,
    nouns: List[Dict[str, Any]]
) -> List[genanki.Deck]:
    """
    Creates two subdecks:
    - [base_deck_name]::1. Gender
    - [base_deck_name]::2. Plural
    """
    gender_model = create_gender_model()
    plural_model = create_plural_model()

    gender_deck_name = f"{base_deck_name}::1. Gender"
    plural_deck_name = f"{base_deck_name}::2. Plural"

    gender_deck = genanki.Deck(get_deterministic_id(gender_deck_name), gender_deck_name)
    plural_deck = genanki.Deck(get_deterministic_id(plural_deck_name), plural_deck_name)

    for item in nouns:
        g_note, p_note = create_notes_for_noun(item, gender_model, plural_model)
        if g_note is not None:
            gender_deck.add_note(g_note)
        if p_note is not None:
            plural_deck.add_note(p_note)

    return [gender_deck, plural_deck]


def create_hierarchical_cefr_decks(
    master_deck_name: str,
    level_datasets: Dict[str, List[Dict[str, Any]]]
) -> List[genanki.Deck]:
    """
    Creates a full nested hierarchical deck tree:
    [master_deck_name]::[LevelName]::1. Gender
    [master_deck_name]::[LevelName]::2. Plural
    """
    gender_model = create_gender_model()
    plural_model = create_plural_model()

    all_decks = []

    level_labels = {
        "A1": "A1 (Beginner)",
        "A2": "A2 (Elementary)",
        "B1": "B1 (Intermediate)",
        "B2": "B2 (Upper-Intermediate)",
        "C1": "C1 (Advanced)"
    }

    for level_key, nouns in level_datasets.items():
        label = level_labels.get(level_key.upper(), level_key)
        level_base_name = f"{master_deck_name}::{label}"
        
        gender_deck_name = f"{level_base_name}::1. Gender"
        plural_deck_name = f"{level_base_name}::2. Plural"

        g_deck = genanki.Deck(get_deterministic_id(gender_deck_name), gender_deck_name)
        p_deck = genanki.Deck(get_deterministic_id(plural_deck_name), plural_deck_name)

        for item in nouns:
            g_note, p_note = create_notes_for_noun(item, gender_model, plural_model)
            if g_note is not None:
                g_deck.add_note(g_note)
            if p_note is not None:
                p_deck.add_note(p_note)

        all_decks.extend([g_deck, p_deck])

    return all_decks


def export_package(decks: List[genanki.Deck], output_path: str) -> str:
    """
    Saves a list of genanki Decks to an .apkg file package.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    package = genanki.Package(decks)
    package.write_to_file(output_path)
    return output_path


def load_nouns_from_json(json_path: str) -> List[Dict[str, Any]]:
    """Loads a list of noun objects from a JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "nouns" in data:
        return data["nouns"]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError(f"Unexpected data format in {json_path}")
