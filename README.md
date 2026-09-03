# 🇩🇪 German Nouns Anki Deck Collection (CEFR A1 to C1)

[![Release](https://img.shields.io/github/v/release/yuhouzhou/german-nouns-anki?color=blue&label=Release)](https://github.com/yuhouzhou/german-nouns-anki/releases/latest)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Anki](https://img.shields.io/badge/Anki-Ready-success.svg)](https://apps.ankiweb.net/)

A curated, comprehensive collection of **2,805 German Nouns (5,610 cards)** organized by CEFR level (**A1 to C1**), powered by a 100,000-lemma Wiktionary morphological database, concise 2-tier grammatical rules, automatic morphological plural highlighting, and zero sibling burying.

### 📥 Direct Downloads ([v1.1.0 Release](https://github.com/yuhouzhou/german-nouns-anki/releases/tag/v1.1.0))

| Deck Package | Level | Nouns | Cards | Direct Download |
| :--- | :--- | :--- | :--- | :--- |
| **Complete Bundle** | **A1–C1** | **2,805** | **5,610** | [⬇️ Download .apkg (2.6 MB)](https://github.com/yuhouzhou/german-nouns-anki/releases/download/v1.1.0/german_nouns_A1_to_C1_complete.apkg) |
| **Level A1** | Beginner | 1,110 | 2,220 | [⬇️ Download .apkg (1.0 MB)](https://github.com/yuhouzhou/german-nouns-anki/releases/download/v1.1.0/german_nouns_A1.apkg) |
| **Level A2** | Elementary | 514 | 1,028 | [⬇️ Download .apkg (544 KB)](https://github.com/yuhouzhou/german-nouns-anki/releases/download/v1.1.0/german_nouns_A2.apkg) |
| **Level B1** | Intermediate | 555 | 1,110 | [⬇️ Download .apkg (612 KB)](https://github.com/yuhouzhou/german-nouns-anki/releases/download/v1.1.0/german_nouns_B1.apkg) |
| **Level B2** | Upper-Intermediate | 336 | 672 | [⬇️ Download .apkg (408 KB)](https://github.com/yuhouzhou/german-nouns-anki/releases/download/v1.1.0/german_nouns_B2.apkg) |
| **Level C1** | Advanced | 290 | 580 | [⬇️ Download .apkg (372 KB)](https://github.com/yuhouzhou/german-nouns-anki/releases/download/v1.1.0/german_nouns_C1.apkg) |

---

## 📱 Mobile App Demo (AnkiMobile / AnkiDroid)

| 1. Gender Card (Front) | 1. Gender Card (Back) | 2. Plural Card (Front) | 2. Plural Card (Back) |
| :---: | :---: | :---: | :---: |
| <img src="docs/screenshots/gender_card_front.png" width="220" alt="Gender Front"> | <img src="docs/screenshots/gender_card_back.png" width="220" alt="Gender Back"> | <img src="docs/screenshots/plural_card_front.png" width="220" alt="Plural Front"> | <img src="docs/screenshots/plural_card_back.png" width="220" alt="Plural Back"> |
| *Prompt: Article `der/die/das`* | *Reveal: Full color + Gender Rule* | *Prompt: Recall plural form* | *Reveal: Crimson diff + Plural Rule* |

---

## 🌟 Key Features

### 1. 🗂️ Dual Subdeck Architecture (Zero Sibling Burying)
Anki by default buries sibling cards from the same note on the same day. This collection uses **dual independent subdecks** per level so you can study both cards immediately:
- `German Nouns (A1)::1. Gender` — Prompt: *Which article (der / die / das)?*
- `German Nouns (A1)::2. Plural` — Prompt: *What is the plural form?*

```text
▼ German Nouns (A1-C1 Complete)
    ├── ▼ A1 (Beginner)
    │     ├── 1. Gender
    │     └── 2. Plural
    ├── ▼ A2 (Elementary)
    │     ├── 1. Gender
    │     └── 2. Plural
    ├── ▼ B1 (Intermediate)
    │     ├── 1. Gender
    │     └── 2. Plural
    ├── ▼ B2 (Upper-Intermediate)
    │     ├── 1. Gender
    │     └── 2. Plural
    └── ▼ C1 (Advanced)
          ├── 1. Gender
          └── 2. Plural
```

---

### 2. 👥 Nominalized Adjectives (`der / die`)
Words referring to persons that decline like adjectives (*der/die Erwachsene*, *der/die Jugendliche*, *der/die Bekannte*, *der/die Beamte*, *der/die Verwandte*) are fully modeled:
- **Gender Card**: Displays **`der / die [Noun]`** with split gradient styling and adjective declension breakdown (*Maskulin: ein Erwachsener*, *Feminin: eine Erwachsene*).
- **Plural Card**: Displays the primary definite plural **`die Erwachsenen`** and prominently displays the strong inflection without article: **`(ohne Artikel / nach Zahlen: viele Erwachsene)`**.

---

### 3. 🔀 Curated Homonyms with Different Gender & Meaning
24 pairs and triplets of German nouns that change gender and meaning are fully disambiguated with English descriptions on card fronts and cross-reference comparison boxes on card backs:
- **`Band`**: `das Band` *(ribbon/tape &rarr; die Bänder)* | `der Band` *(book volume &rarr; die Bände)* | `die Band` *(music band &rarr; die Bands)*
- **`Gehalt`**: `das Gehalt` *(salary &rarr; die Gehälter)* | `der Gehalt` *(content/substance &rarr; die Gehalte)*
- **`Leiter`**: `der Leiter` *(leader &rarr; die Leiter)* | `die Leiter` *(ladder &rarr; die Leitern)*
- **`Schild`**: `das Schild` *(signboard &rarr; die Schilder)* | `der Schild` *(shield &rarr; die Schilde)*
- **`Steuer`**: `die Steuer` *(tax &rarr; die Steuern)* | `das Steuer` *(steering wheel &rarr; die Steuer)*

---

### 4. ✨ Curated Double Plurals with Semantic Distinctions
Nouns with two distinct plural forms display both highlighted on the card back alongside clear semantic explanations:
- **`das Wort`**: `die Wörter` *(isolated vocabulary words)* vs `die Worte` *(connected speech, meaningful quotes)*
- **`die Bank`**: `die Bänke` *(sitting benches)* vs `die Banken` *(financial institutions)*
- **`das Band`**: `die Bänder` *(ribbons/tapes)* vs `die Bande` *(bonds of friendship, ties)*
- **`das Tuch`**: `die Tücher` *(cloths, towels)* vs `die Tuche` *(woven fabrics, textiles)*
- **`das Denkmal`**: `die Denkmäler` *(standard)* vs `die Denkmale` *(literary/official)*

---

### 5. 🎨 Full Color-Coded Reveal
On card reveal, both the definite article and the entire noun light up in vibrant color:
- **Masculine (`der`)** &rarr; **Blue** (`#0284c7` / `#38bdf8`)
- **Feminine (`die`)** &rarr; **Red** (`#dc2626` / `#f87171`)
- **Neuter (`das`)** &rarr; **Green** (`#16a34a` / `#4ade80`)
- **Dual Gender (`der/die`)** &rarr; **Split Blue/Red Gradient & Purple** (`#8b5cf6` / `#c084fc`)

---

### 6. ✨ Morphological Plural Highlighting
On plural cards, the article `die` is rendered in **neutral black text**, and all morphological changes (Umlaut shifts and suffix endings) are highlighted in **vibrant underlined crimson**:

| Singular | Plural Card Output | Highlighted Changes |
| :--- | :--- | :--- |
| **der Hund** | <span style="font-size: 18px;">die Hund<span style="color:#e11d48;font-weight:bold;border-bottom:2px solid #e11d48">e</span></span> | Suffix **`-e`** |
| **die Altstadt** | <span style="font-size: 18px;">die Altst<span style="color:#e11d48;font-weight:bold;border-bottom:2px solid #e11d48">ä</span>dt<span style="color:#e11d48;font-weight:bold;border-bottom:2px solid #e11d48">e</span></span> | Umlaut **`ä`** + Suffix **`-e`** |
| **das Buch** | <span style="font-size: 18px;">die B<span style="color:#e11d48;font-weight:bold;border-bottom:2px solid #e11d48">ü</span>ch<span style="color:#e11d48;font-weight:bold;border-bottom:2px solid #e11d48">er</span></span> | Umlaut **`ü`** + Suffix **`-er`** |
| **der Baum** | <span style="font-size: 18px;">die B<span style="color:#e11d48;font-weight:bold;border-bottom:2px solid #e11d48">ä</span>um<span style="color:#e11d48;font-weight:bold;border-bottom:2px solid #e11d48">e</span></span> | Umlaut **`ä`** + Suffix **`-e`** |
| **die Möglichkeit** | <span style="font-size: 18px;">die Möglichkeit<span style="color:#e11d48;font-weight:bold;border-bottom:2px solid #e11d48">en</span></span> | Suffix **`-en`** |
| **das Mädchen** | <span style="font-size: 18px;">die Mädchen</span> | No change (clean) |

---

### 7. 💡 2-Tier Glanceable Rule Engine
- **Headline (< 0.5s glance)**: Bold high-level takeaway (e.g. `Suffix -keit ➔ 100% Feminine (die)`).
- **Context**: Rationale and pattern examples.
- **Clean for Root Words**: Pure root nouns without an applicable rule leave the rule box completely hidden.

---

### 8. 🌙 Native iOS & macOS System Dark Mode
- Automatically reacts whenever your iPhone, iPad, or Mac switches between Light and Dark mode via `@media (prefers-color-scheme: dark)`.
- Full-screen edge-to-edge layout customized for **AnkiMobile (iOS)** and **Anki Desktop**.

---

## 📊 Dataset & CEFR Breakdown

Sourced from **Goethe-Institut**, **Profile Deutsch**, **Hathibelagal Lexicon**, and verified against the **100,064-lemma German Wiktionary Morphological Database**:

| Deck Package | CEFR Focus | Noun Count | Card Count | Dual Subdecks |
| :--- | :--- | :--- | :--- | :--- |
| **`german_nouns_A1.apkg`** | **A1 (Beginner)** | 1,110 nouns | 2,220 cards | `1. Gender`, `2. Plural` |
| **`german_nouns_A2.apkg`** | **A2 (Elementary)** | 514 nouns | 1,028 cards | `1. Gender`, `2. Plural` |
| **`german_nouns_B1.apkg`** | **B1 (Intermediate)** | 555 nouns | 1,110 cards | `1. Gender`, `2. Plural` |
| **`german_nouns_B2.apkg`** | **B2 (Upper-Intermediate)** | 336 nouns | 672 cards | `1. Gender`, `2. Plural` |
| **`german_nouns_C1.apkg`** | **C1 (Advanced)** | 290 nouns | 580 cards | `1. Gender`, `2. Plural` |
| **`german_nouns_A1_to_C1_complete.apkg`** | **Master Complete Bundle** | **2,805 nouns** | **5,610 cards** | **10 subdecks** |

---

## 🚀 Quick Start & Installation

### Option 1: Import Pre-built Decks into Anki
1. Download the `.apkg` file from the [Releases](https://github.com/yuhouzhou/german-nouns-anki/releases) section (or build them locally).
2. Double-click any `.apkg` package to import into **Anki Desktop**, **AnkiMobile (iOS)**, or **AnkiDroid**.

### Option 2: Build Decks from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yuhouzhou/german-nouns-anki.git
   cd german-nouns-anki
   ```

2. Install dependencies:
   ```bash
   pip install genanki
   ```

3. Build all decks:
   ```bash
   # Build all levels (A1 to C1) + master bundle
   python3 src/build_decks.py --all

   # Or build a specific level
   python3 src/build_decks.py --level a1
   ```
   The generated `.apkg` files will be in `output/`.

---

## 🧪 Testing

Run the test suite to verify morphological integrity, deck models, and rule engine accuracy:

```bash
# Run unit & integration tests
python3 tests/test_rules.py
python3 tests/test_deck.py
python3 tests/test_dataset_integrity.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
