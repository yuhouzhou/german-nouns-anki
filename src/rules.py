"""
German Gender and Plural Rule Engine
Exhaustive linguistic rule detection for German noun genders (der/die/das) and plural forms.
Provides 2-tier rule explanations:
1. Concise glanceable takeaway summary (instant comprehension).
2. Deeper linguistic explanation and pattern examples.
"""

from typing import Dict, Optional, Any

# ==========================================
# 1. SEMANTIC DICTIONARIES / WORD LISTS
# ==========================================

DAYS_OF_WEEK = {
    "montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonnabend", "sonntag"
}

MONTHS = {
    "januar", "februar", "märz", "maerz", "april", "mai", "juni", "juli",
    "august", "september", "oktober", "november", "dezember"
}

SEASONS = {"frühling", "fruehling", "sommer", "herbst", "winter"}

TIMES_OF_DAY = {
    "morgen", "vormittag", "mittag", "nachmittag", "abend", "spätnachmittag"
}  # Note: 'nacht' is feminine exception

WEATHER_PRECIPITATION = {
    "regen", "schnee", "hagel", "graupel", "nebel", "wind", "sturm", "orkan",
    "taifun", "tornado", "zyklon", "monsun", "föhn", "foehn", "tau", "frost",
    "donner", "blitz", "hurrikan", "reiff", "schauer"
}  # Exceptions: das Eis, das Wetter, die Brise, die Hitze, die Kälte

COMPASS_DIRECTIONS = {
    "norden", "süden", "sueden", "osten", "westen", "nordosten", "nordwesten",
    "südosten", "suedosten", "südwesten", "suedwesten"
}

ALCOHOLIC_DRINKS = {
    "wein", "rotwein", "weißwein", "weisswein", "sekt", "champagner", "wodka",
    "vodka", "schnaps", "gin", "likör", "likoer", "rum", "whisky", "whiskey",
    "cognac", "brandy", "tequila", "ouzo", "grappa", "cocktail", "aperitif",
    "glühwein", "gluehwein"
}  # Exception: das Bier

NON_ALC_BEVERAGES = {
    "kaffee", "tee", "saft", "apfelsaft", "orangensaft", "kakao", "espresso", "cappuccino"
}  # Exceptions: die Milch, das Wasser

MINERALS_GEMS = {
    "diamant", "rubin", "smaragd", "saphir", "quarz", "granit", "marmor",
    "gneis", "basalt", "kristall", "amethyst", "topas", "opal"
}

CAR_TRAIN_BRANDS = {
    "bmw", "mercedes", "audi", "volkswagen", "vw", "porsche", "opel", "ford",
    "ferrari", "fiat", "toyota", "tesla", "ice", "intercity", "eurocity", "regionalexpress"
}

CURRENCIES = {
    "euro", "dollar", "franken", "cent", "rubel", "yen", "dinar", "shekel",
    "peso", "zloty", "dirham", "renminbi", "yuan"
}  # Exceptions: die Krone, die Mark, das Pfund

TREES_SHRUBS = {
    "eiche", "birke", "tanne", "fichte", "buche", "palme", "linde", "kiefer",
    "erle", "esche", "ulme", "weide", "zypresse", "zeder", "akazie", "kastanie",
    "hasel", "magnolie", "platane", "espe", "pappel", "lärche", "laerche"
}  # Exceptions: der Ahorn, der Baum, der Strauch, der Wacholder

FLOWERS = {
    "rose", "tulpe", "nelke", "orchidee", "sonnenblume", "lilie", "daffodil",
    "narzisse", "begonie", "geranie", "iris",
    "kamille", "hortensie", "margerite", "chrysantheme", "dahlie", "aster", "anemone"
}  # Exceptions: der Kaktus, das Veilchen, das Vergissmeinnicht

FRUITS_BERRIES = {
    "banane", "orange", "zitrone", "erdbeere", "himbeere", "kirsche", "birne",
    "pflaume", "aprikose", "mandarine", "melone", "wassermelone", "feige",
    "ananas", "dattel", "brombeere", "heidelbeere", "blaubeere", "stachelbeere",
    "johannisbeere", "traube", "weintraube", "grapefruit", "mango", "papaya",
    "kiwi", "avocado", "limette", "maracuja"
}  # Exceptions: der Apfel, der Pfirsich, der Granatapfel

METALS_ELEMENTS = {
    "gold", "silber", "eisen", "kupfer", "aluminium", "blei", "zink", "platin",
    "uran", "titan", "nickel", "chrom", "magnesium", "kalzium", "zinn",
    "quecksilber", "helium", "neon", "argon", "krypton", "xenon", "radon"
}  # Exceptions: der Stahl, die Bronze, das Messing (neuter fits)

LANGUAGES = {
    "deutsch", "englisch", "französisch", "franzoesisch", "spanisch", "italienisch",
    "russisch", "chinesisch", "japanisch", "arabisch", "portugiesisch", "latein",
    "griechisch", "polnisch", "türkisch", "tuerkisch", "niederländisch"
}

FRACTIONS = {
    "drittel", "viertel", "fünftel", "fuenftel", "sechstel", "siebtel",
    "achtel", "neuntel", "zehntel", "hundertstel", "tausendstel", "prozent"
}  # Exception: die Hälfte

COLORS_AS_NOUNS = {
    "blau", "rot", "grün", "gruen", "gelb", "weiß", "weiss", "schwarz",
    "grau", "braun", "rosa", "orange", "lila", "violett", "türkis", "tuerkis"
}

FEMALE_ENTITIES = {
    "frau", "mutter", "tochter", "schwester", "omi", "oma", "tante", "nichte",
    "kuh", "stute", "henne", "löwin", "loewin", "wölfin", "woelfin", "bäckerin",
    "baeckerin", "katze", "gans", "ente"
}

MALE_ENTITIES = {
    "mann", "junge", "bursche", "knabe", "vater", "sohn", "bruder", "opa",
    "onkel", "neffe", "kater", "stier", "bulle", "hengst", "hahn", "rüde", "ruede",
    "bock", "eber", "widder", "ochse"
}

BABY_ANIMALS_HUMANS = {
    "kind", "baby", "lamm", "kalb", "ferkel", "küken", "kueken", "fohlen",
    "welpe", "kätzchen", "kaetzchen", "hündchen", "huendchen"
}

VERB_STEM_NOUNS = {
    "lauf", "sprung", "flug", "sitz", "zug", "schlaf", "schnitt", "griff",
    "gang", "schuss", "schrei", "blick", "ruf", "druck", "fall", "stoß",
    "stoss", "wurf", "biss", "tritt", "streit", "kauf", "bau", "klang",
    "fang", "start", "schub", "halt", "brand", "wuchs", "stich", "kuss",
    "rausch", "schreck", "sturz", "knall", "drang"
}

# ==========================================
# 2. MORPHOLOGICAL EXCEPTIONS & ROOT LISTS
# ==========================================

# Weak masculine nouns ending in -e
WEAK_MASCULINE_E = {
    "name", "same", "gedanke", "wille", "glaube", "friede", "funke", "buchstabe",
    "schade", "drache", "zeuge", "experte", "kunde", "kollege", "nachbar",
    "junge", "bursche", "knabe", "löwe", "loewe", "affe", "hase", "bulle",
    "ochse", "rabe", "riese", "soziologe", "psychologe", "biologe", "diplomat",
    "mensch", "herr", "prinz", "held", "graf", "fürst", "fuerst", "präsident",
    "praesident", "polizist", "tourist", "architekt", "fotograf"
}

# Neuter nouns ending in -e
NEUTER_E_EXCEPTIONS = {
    "auge", "ende", "erbe", "interesse", "finale"
}

# Feminine exceptions to typical masculine / neuter patterns
FEMININE_EXCEPTIONS = {
    "gemeinde": (
        "Ending <b>-e</b> &rarr; Feminine (<i>die</i>)",
        "Community noun ending in -e; distinct feminine word with <i>Ge-</i> prefix (unlike neuter collectives like <i>das Gebäude</i>)."
    ),
    "geschichte": (
        "Ending <b>-e</b> &rarr; Feminine (<i>die</i>)",
        "Story/history noun ending in -e; notable feminine word starting with <i>Ge-</i>."
    ),
    "gefahr": (
        "Feminine root noun (<i>die Gefahr</i>)",
        "Danger/peril is feminine despite the <i>Ge-</i> prefix."
    ),
    "geduld": (
        "Abstract noun &rarr; Feminine (<i>die Geduld</i>)",
        "Patience is feminine despite the <i>Ge-</i> prefix."
    ),
    "gebühr": (
        "Fee / charge &rarr; Feminine (<i>die Gebühr</i>)",
        "Fee/charge noun is feminine."
    ),
    "gestalt": (
        "Form / shape &rarr; Feminine (<i>die Gestalt</i>)",
        "Form/figure noun is feminine."
    ),
    "geburt": (
        "Derived from <i>gebären</i> + <b>-t</b> &rarr; Feminine (<i>die</i>)",
        "Verb root + -t formation produces a feminine noun."
    ),
    "gewohnheit": (
        "Suffix <b>-heit</b> &rarr; 100% Feminine (<i>die</i>)",
        "The -heit suffix trumps the Ge- prefix."
    ),
    "nacht": (
        "Time exception &rarr; Feminine (<i>die Nacht</i>)",
        "Major exception to the general masculine rule for times of day."
    ),
    "milch": (
        "Beverage exception &rarr; Feminine (<i>die Milch</i>)",
        "Exception to the general masculine rule for common drinks."
    ),
    "butter": (
        "Culinary noun &rarr; Feminine (<i>die Butter</i>)",
        "Common feminine exception to the masculine -er tendency."
    ),
    "mutter": (
        "Natural female gender &rarr; Feminine (<i>die Mutter</i>)",
        "Biological female entity."
    ),
    "schwester": (
        "Natural female gender &rarr; Feminine (<i>die Schwester</i>)",
        "Biological female entity."
    ),
    "tochter": (
        "Natural female gender &rarr; Feminine (<i>die Tochter</i>)",
        "Biological female entity."
    ),
    "macht": (
        "Verb root + <b>-t</b> &rarr; Feminine (<i>die Macht</i>)",
        "Derived from mögen/vermögen + -t."
    ),
    "fahrt": (
        "Verb root + <b>-t</b> &rarr; Feminine (<i>die Fahrt</i>)",
        "Derived from fahren + -t."
    ),
    "schrift": (
        "Verb root + <b>-t</b> &rarr; Feminine (<i>die Schrift</i>)",
        "Derived from schreiben + -t."
    ),
    "tat": (
        "Verb root + <b>-t</b> &rarr; Feminine (<i>die Tat</i>)",
        "Derived from tun + -t."
    )
}

# Masculine exceptions to typical neuter / feminine patterns
MASCULINE_EXCEPTIONS = {
    "gedanke": (
        "Weak masculine noun in <b>-e</b> (<i>der Gedanke</i>)",
        "Belongs to the N-Deklination masculine noun class."
    ),
    "geschmack": (
        "Verb stem derived &rarr; Masculine (<i>der Geschmack</i>)",
        "Derived from <i>schmecken</i> with Ge- prefix."
    ),
    "geruch": (
        "Verb stem derived &rarr; Masculine (<i>der Geruch</i>)",
        "Derived from <i>riechen</i> with Ge- prefix."
    ),
    "gewinn": (
        "Verb stem derived &rarr; Masculine (<i>der Gewinn</i>)",
        "Derived from <i>gewinnen</i>."
    ),
    "apfel": (
        "Fruit exception &rarr; Masculine (<i>der Apfel</i>)",
        "Key masculine exception to the feminine fruit tendency."
    ),
    "käse": (
        "Dairy noun &rarr; Masculine (<i>der Käse</i>)",
        "Dairy product noun ending in -e."
    ),
    "kaese": (
        "Dairy noun &rarr; Masculine (<i>der Käse</i>)",
        "Dairy product noun ending in -e."
    ),
    "bier": (
        "Alcohol exception &rarr; Neuter (<i>das Bier</i>)",
        "The main neuter exception to the masculine alcoholic drinks rule."
    )
}


# ==========================================
# 3. DETAILED GENDER RULES LOGIC
# ==========================================

def get_gender_rule(noun: str, article: str, meaning: str = "", tags: Optional[list] = None) -> Dict[str, Any]:
    """
    Determines the linguistic rule explaining why a German noun has its grammatical gender.
    Returns structured 2-tier summary and detailed explanation.
    """
    article = article.lower().strip()
    clean_noun = noun.strip()
    lower_noun = clean_noun.lower()
    
    # Helper to return a structured rule dict
    def make_rule(category: str, rule_name: str, summary: str, detail: str, confidence: str, examples: str, icon: str = "💡"):
        return {
            "article": article,
            "category": category,
            "rule_name": rule_name,
            "summary": summary,
            "detail": detail,
            "rule_text": f"{summary}<br><span style='font-size: 13.5px; opacity: 0.85;'>{detail}</span>",
            "confidence": confidence,
            "examples": examples,
            "icon": icon
        }

    # ---------------------------------------------------------
    # A. EXPLICIT EXCEPTIONS & CONFLICT CASES
    # ---------------------------------------------------------
    if article == "die" and lower_noun in FEMININE_EXCEPTIONS:
        summary, detail = FEMININE_EXCEPTIONS[lower_noun]
        return make_rule("Specific Pattern", f"Specific Pattern ({clean_noun})", summary, detail, "100%", clean_noun, "💡")

    if article == "der" and lower_noun in MASCULINE_EXCEPTIONS:
        summary, detail = MASCULINE_EXCEPTIONS[lower_noun]
        return make_rule("Specific Pattern", f"Specific Pattern ({clean_noun})", summary, detail, "100%", clean_noun, "💡")

    # ---------------------------------------------------------
    # B. HIGH-CERTAINTY SUFFIX RULES
    # ---------------------------------------------------------
    
    # --- FEMININE SUFFIXES ---
    if article == "die":
        if lower_noun.endswith("heit"):
            return make_rule(
                "Suffix", "Suffix -heit (100% Feminine)",
                "Suffix <b>-heit</b> &rarr; 100% Feminine (<i>die</i>)",
                "Forms abstract nouns from adjectives/nouns denoting state or condition.",
                "100%", "die Freiheit, die Schönheit, die Gesundheit, die Wahrheit, die Einheit", "⭐"
            )
        if lower_noun.endswith("keit"):
            return make_rule(
                "Suffix", "Suffix -keit (100% Feminine)",
                "Suffix <b>-keit</b> &rarr; 100% Feminine (<i>die</i>)",
                "Forms abstract nouns describing qualities, abilities, and states.",
                "100%", "die Möglichkeit, die Einsamkeit, die Fähigkeit, die Dankbarkeit, die Höflichkeit", "⭐"
            )
        if lower_noun.endswith("ung"):
            return make_rule(
                "Suffix", "Suffix -ung (~99% Feminine)",
                "Suffix <b>-ung</b> &rarr; ~99% Feminine (<i>die</i>)",
                "Forms nouns from verbs describing actions, processes, or results.",
                "~99%", "die Zeitung, die Wohnung, die Hoffnung, die Bedeutung, die Übung", "⭐"
            )
        if lower_noun.endswith("schaft"):
            return make_rule(
                "Suffix", "Suffix -schaft (~99% Feminine)",
                "Suffix <b>-schaft</b> &rarr; ~99% Feminine (<i>die</i>)",
                "Denotes collective entities, partnerships, and states of being.",
                "~99%", "die Freundschaft, die Mannschaft, die Gesellschaft, die Wirtschaft, die Landschaft", "⭐"
            )
        if lower_noun.endswith("tät") or lower_noun.endswith("taet"):
            return make_rule(
                "Suffix", "Suffix -tät (100% Feminine)",
                "Suffix <b>-tät</b> &rarr; 100% Feminine (<i>die</i>)",
                "Latin-origin suffix corresponding to English <i>-ty</i>.",
                "100%", "die Universität, die Realität, die Qualität, die Aktivität, die Nationalität", "⭐"
            )
        if lower_noun.endswith("ion") and not lower_noun.endswith("spion") and not lower_noun.endswith("stadion"):
            return make_rule(
                "Suffix", "Suffix -ion (100% Feminine)",
                "Suffix <b>-ion</b> &rarr; 100% Feminine (<i>die</i>)",
                "Foreign loanwords corresponding to English <i>-tion / -sion</i>.",
                "100%", "die Information, die Station, die Tradition, die Nation, die Aktion, die Religion", "⭐"
            )
        if lower_noun.endswith("ik") and not lower_noun.endswith("atlantik") and not lower_noun.endswith("pazifik"):
            return make_rule(
                "Suffix", "Suffix -ik (~95% Feminine)",
                "Suffix <b>-ik</b> &rarr; ~95% Feminine (<i>die</i>)",
                "Denotes academic disciplines, arts, and systems of science.",
                "~95%", "die Musik, die Politik, die Fabrik, die Kritik, die Physik, die Grammatik", "💡"
            )
        if lower_noun.endswith("in") and len(lower_noun) > 3:
            return make_rule(
                "Suffix", "Suffix -in (Female Roles 100%)",
                "Suffix <b>-in</b> &rarr; 100% Feminine (<i>die</i>)",
                "Female profession, role, nationality, and animal titles.",
                "100%", "die Lehrerin, die Ärztin, die Studentin, die Freundin, die Löwin", "⭐"
            )
        if (lower_noun.endswith("ei") or lower_noun.endswith("erei")) and lower_noun not in {"ei", "papagei"}:
            return make_rule(
                "Suffix", "Suffix -ei / -erei (100% Feminine)",
                "Suffix <b>-ei / -erei</b> &rarr; 100% Feminine (<i>die</i>)",
                "Denotes businesses, places of activity, or habits.",
                "100%", "die Bäckerei, die Bücherei, die Datei, die Polizei, die Malerei", "⭐"
            )
        if lower_noun.endswith("anz") or lower_noun.endswith("enz"):
            return make_rule(
                "Suffix", "Suffix -anz / -enz (100% Feminine)",
                "Suffix <b>-anz / -enz</b> &rarr; 100% Feminine (<i>die</i>)",
                "Abstract concepts of Latin origin.",
                "100%", "die Distanz, die Toleranz, die Existenz, die Konferenz, die Intelligenz", "⭐"
            )
        if lower_noun.endswith("ie") and lower_noun != "genie":
            return make_rule(
                "Suffix", "Suffix -ie (100% Feminine)",
                "Stressed ending <b>-ie</b> &rarr; 100% Feminine (<i>die</i>)",
                "Fields of study, sciences, and abstract qualities.",
                "100%", "die Energie, die Familie, die Biologie, die Theorie, die Industrie", "⭐"
            )
        if lower_noun.endswith("ur") and lower_noun not in {"abitur", "futur", "purpur"}:
            return make_rule(
                "Suffix", "Suffix -ur (~95% Feminine)",
                "Suffix <b>-ur</b> &rarr; ~95% Feminine (<i>die</i>)",
                "Denotes structures, procedures, or states of being.",
                "~95%", "die Natur, die Kultur, die Figur, die Struktur, die Temperatur, die Reparatur", "💡"
            )
        if lower_noun.endswith("ade") or lower_noun.endswith("age"):
            return make_rule(
                "Suffix", "Suffix -ade / -age (100% Feminine)",
                "Suffix <b>-ade / -age</b> &rarr; 100% Feminine (<i>die</i>)",
                "French-derived loanwords.",
                "100%", "die Schokolade, die Limonade, die Garage, die Passage, die Reportage", "⭐"
            )
        if lower_noun.endswith("ette"):
            return make_rule(
                "Suffix", "Suffix -ette (100% Feminine)",
                "Suffix <b>-ette</b> &rarr; 100% Feminine (<i>die</i>)",
                "French diminutive or item suffix.",
                "100%", "die Zigarette, die Marionette, die Diskette, die Kassette, die Toilette", "⭐"
            )
        if lower_noun.endswith("itis"):
            return make_rule(
                "Suffix", "Medical Suffix -itis (100% Feminine)",
                "Medical suffix <b>-itis</b> &rarr; 100% Feminine (<i>die</i>)",
                "Terms for inflammatory medical conditions.",
                "100%", "die Bronchitis, die Gastritis, die Arthritis, die Hepatitis", "⭐"
            )
        if lower_noun.endswith("thek") or lower_noun.endswith("theke"):
            return make_rule(
                "Suffix", "Suffix -thek (100% Feminine)",
                "Ending <b>-thek</b> &rarr; 100% Feminine (<i>die</i>)",
                "Collections, institutions, and establishments.",
                "100%", "die Bibliothek, die Diskothek, die Apotheke, die Pinakothek", "⭐"
            )

    # --- MASCULINE SUFFIXES ---
    if article == "der":
        if lower_noun.endswith("ismus"):
            return make_rule(
                "Suffix", "Suffix -ismus (100% Masculine)",
                "Suffix <b>-ismus</b> &rarr; 100% Masculine (<i>der</i>)",
                "Doctrines, movements, belief systems, and ideologies.",
                "100%", "der Optimismus, der Realismus, der Tourismus, der Kapitalismus", "⭐"
            )
        if lower_noun.endswith("ling") and lower_noun != "messing":
            return make_rule(
                "Suffix", "Suffix -ling (~99% Masculine)",
                "Suffix <b>-ling</b> &rarr; ~99% Masculine (<i>der</i>)",
                "Denotes persons, living things, or distinctive characteristics.",
                "~99%", "der Schmetterling, der Frühling, der Lehrling, der Zwilling, der Flüchtling", "⭐"
            )
        if lower_noun.endswith("ist"):
            return make_rule(
                "Suffix", "Suffix -ist (100% Masculine)",
                "Suffix <b>-ist</b> &rarr; 100% Masculine (<i>der</i>)",
                "Agent nouns, professions, and adherents of movements.",
                "100%", "der Polizist, der Tourist, der Optimist, der Pianist, der Artist", "⭐"
            )
        if lower_noun.endswith("or") and len(lower_noun) > 3 and lower_noun not in {"labor", "tor", "moor", "chor"}:
            return make_rule(
                "Suffix", "Suffix -or (~95% Masculine)",
                "Suffix <b>-or</b> &rarr; ~95% Masculine (<i>der</i>)",
                "Latin-origin agents, actors, and machinery.",
                "~95%", "der Motor, der Reaktor, der Autor, der Doktor, der Professor", "💡"
            )
        if (lower_noun.endswith("ant") or lower_noun.endswith("ent")) and len(lower_noun) > 4 and lower_noun not in {"restaurant", "patent", "talent", "element", "moment", "argument", "dokument", "parlament"}:
            return make_rule(
                "Suffix", "Suffix -ant / -ent (~90% Masculine)",
                "Suffix <b>-ant / -ent</b> &rarr; ~90% Masculine (<i>der</i>)",
                "Active persons, agents, or participants.",
                "~90%", "der Elefant, der Demonstrant, der Student, der Patient, der Präsident", "💡"
            )
        if lower_noun.endswith("eur") or lower_noun.endswith("ör") or lower_noun.endswith("oer"):
            return make_rule(
                "Suffix", "Suffix -eur / -ör (100% Masculine)",
                "Suffix <b>-eur / -ör</b> &rarr; 100% Masculine (<i>der</i>)",
                "French loanwords for professions, roles, and objects.",
                "100%", "der Friseur, der Ingenieur, der Likör, der Regisseur", "⭐"
            )
        if lower_noun.endswith("oge"):
            return make_rule(
                "Suffix", "Suffix -oge (100% Masculine)",
                "Ending <b>-oge</b> &rarr; 100% Masculine (<i>der</i>)",
                "Specialists and scientists (weak masculine N-declension).",
                "100%", "der Biologe, der Psychologe, der Geologe, der Soziologe", "⭐"
            )
        if lower_noun.endswith("är") or lower_noun.endswith("aer"):
            return make_rule(
                "Suffix", "Suffix -är (100% Masculine)",
                "Ending <b>-är</b> &rarr; 100% Masculine (<i>der</i>)",
                "Occupations, titles, and social roles.",
                "100%", "der Millionär, der Sekretär, der Funktionär", "⭐"
            )
        if lower_noun.endswith("ich") or (lower_noun.endswith("ig") and len(lower_noun) > 3):
            return make_rule(
                "Suffix", "Suffix -ich / -ig (~90% Masculine)",
                "Suffix <b>-ich / -ig</b> &rarr; ~90% Masculine (<i>der</i>)",
                "German native nouns ending in -ich or -ig.",
                "~90%", "der Teppich, der Bottich, der Käfig, der König, der Honig, der Essig", "💡"
            )
        if lower_noun.endswith("us") and len(lower_noun) > 3:
            return make_rule(
                "Suffix", "Suffix -us (~90% Masculine)",
                "Ending <b>-us</b> &rarr; ~90% Masculine (<i>der</i>)",
                "Latin-origin nouns ending in -us.",
                "~90%", "der Rhythmus, der Status, der Zyklus, der Fokus, der Optimismus", "💡"
            )

    # --- NEUTER SUFFIXES & PREFIXES ---
    if article == "das":
        if lower_noun.endswith("chen"):
            return make_rule(
                "Suffix", "Diminutive Suffix -chen (100% Neuter)",
                "Diminutive <b>-chen</b> &rarr; 100% Neuter (<i>das</i>)",
                "Overrules biological gender without exception.",
                "100%", "das Mädchen, das Brötchen, das Häuschen, das Tierchen, das Stückchen", "⭐"
            )
        if lower_noun.endswith("lein"):
            return make_rule(
                "Suffix", "Diminutive Suffix -lein (100% Neuter)",
                "Diminutive <b>-lein</b> &rarr; 100% Neuter (<i>das</i>)",
                "Overrules biological gender without exception.",
                "100%", "das Fräulein, das Büchlein, das Kindelein, das Männlein", "⭐"
            )
        if lower_noun.endswith("ment") and lower_noun not in {"zement", "moment"}:
            return make_rule(
                "Suffix", "Suffix -ment (~95% Neuter)",
                "Suffix <b>-ment</b> &rarr; ~95% Neuter (<i>das</i>)",
                "Latin/French loanwords for objects, documents, and institutions.",
                "~95%", "das Dokument, das Instrument, das Experiment, das Element, das Parlament", "💡"
            )
        if lower_noun.endswith("tum") and lower_noun not in {"reichtum", "irrtum"}:
            return make_rule(
                "Suffix", "Suffix -tum (~90% Neuter)",
                "Suffix <b>-tum</b> &rarr; ~90% Neuter (<i>das</i>)",
                "Denotes states, conditions, or collectives.",
                "~90%", "das Eigentum, das Christentum, das Wachstum, das Datum, das Altertum", "💡"
            )
        if lower_noun.endswith("um") and len(lower_noun) > 3 and lower_noun not in {"raum", "traum", "baum", "schaum"}:
            return make_rule(
                "Suffix", "Suffix -um (100% Neuter)",
                "Latin ending <b>-um</b> &rarr; 100% Neuter (<i>das</i>)",
                "Classical Latin loan nouns are always neuter.",
                "100%", "das Zentrum, das Museum, das Datum, das Album, das Studium, das Universum", "⭐"
            )
        if (lower_noun.endswith("ma") or lower_noun.endswith("em")) and len(lower_noun) > 3:
            return make_rule(
                "Suffix", "Greek Root -ma / -em (100% Neuter)",
                "Greek ending <b>-ma / -em</b> &rarr; 100% Neuter (<i>das</i>)",
                "Academic, abstract, and scientific Greek loanwords.",
                "100%", "das Thema, das Drama, das Problem, das Klima, das Schema, das System", "⭐"
            )
        if lower_noun.endswith("o") and len(lower_noun) > 2 and lower_noun not in {"euro", "avocado"}:
            return make_rule(
                "Suffix", "Ending -o (~90% Neuter)",
                "Foreign ending <b>-o</b> &rarr; ~90% Neuter (<i>das</i>)",
                "Modern loanwords from Italian, Spanish, or English.",
                "~90%", "das Auto, das Kino, das Foto, das Radio, das Büro, das Studio, das Casino", "💡"
            )
        if lower_noun.endswith("ett"):
            return make_rule(
                "Suffix", "Suffix -ett (100% Neuter)",
                "Ending <b>-ett</b> &rarr; 100% Neuter (<i>das</i>)",
                "French-derived objects, arts, and forms.",
                "100%", "das Bett, das Ballett, das Buffet, das Kabarett, das Bankett", "⭐"
            )
        if lower_noun.endswith("ing") and len(lower_noun) > 4 and lower_noun not in {"frühling", "schmetterling", "zwilling", "lehrling", "flüchtling", "ring", "ding"}:
            return make_rule(
                "Suffix", "English Gerund -ing (100% Neuter)",
                "English gerund <b>-ing</b> &rarr; 100% Neuter (<i>das</i>)",
                "Borrowed activity nouns and gerunds always take das.",
                "100%", "das Training, das Recycling, das Bowling, das Shopping, das Meeting", "⭐"
            )
        if lower_noun.endswith("nis") and lower_noun not in {"erlaubnis", "kenntnis", "finsternis", "wildnis"}:
            return make_rule(
                "Suffix", "Suffix -nis (~75% Neuter)",
                "Suffix <b>-nis</b> &rarr; ~75% Neuter (<i>das</i>)",
                "Verbal nouns denoting results or conditions.",
                "~75%", "das Ergebnis, das Ereignis, das Geheimnis, das Erlebnis, das Zeugnis", "💡"
            )
        if lower_noun.startswith("ge") and len(lower_noun) > 4 and lower_noun not in {"gedanke", "geschmack", "geruch", "gewinn", "geduld", "geschichte", "gefahr"}:
            return make_rule(
                "Prefix", "Collective Prefix Ge-... (~90% Neuter)",
                "Prefix <b>Ge-...</b> &rarr; ~90% Neuter (<i>das</i>)",
                "Collective nouns and grouped entities.",
                "~90%", "das Gebäude, das Gebirge, das Gemüse, das Gespräch, das Gefühl, das Geschenk", "💡"
            )

    # ---------------------------------------------------------
    # C. SEMANTIC / CATEGORY RULES
    # ---------------------------------------------------------
    
    # --- MASCULINE SEMANTIC CATEGORIES ---
    if article == "der":
        if lower_noun in DAYS_OF_WEEK or any(lower_noun.endswith(d) for d in DAYS_OF_WEEK):
            return make_rule(
                "Semantic", "Days of the Week (100% Masculine)",
                "Days of the week &rarr; 100% Masculine (<i>der</i>)",
                "All 7 weekdays take the masculine article der.",
                "100%", "der Montag, der Dienstag, der Mittwoch, der Donnerstag, der Freitag", "⭐"
            )
        if lower_noun in MONTHS:
            return make_rule(
                "Semantic", "Months of the Year (100% Masculine)",
                "Months of the year &rarr; 100% Masculine (<i>der</i>)",
                "All 12 calendar months take the masculine article der.",
                "100%", "der Januar, der Februar, der März ... der Dezember", "⭐"
            )
        if lower_noun in SEASONS:
            return make_rule(
                "Semantic", "Seasons (100% Masculine)",
                "Seasons &rarr; 100% Masculine (<i>der</i>)",
                "All four seasons take the masculine article der.",
                "100%", "der Frühling, der Sommer, der Herbst, der Winter", "⭐"
            )
        if lower_noun in TIMES_OF_DAY:
            return make_rule(
                "Semantic", "Times of Day (Masculine)",
                "Times of day &rarr; Masculine (<i>der</i>)",
                "Parts of the day take der (Major exception: <i>die Nacht</i>).",
                "High", "der Morgen, der Vormittag, der Mittag, der Nachmittag, der Abend", "💡"
            )
        if lower_noun in WEATHER_PRECIPITATION:
            return make_rule(
                "Semantic", "Precipitation & Weather (Masculine)",
                "Precipitation & weather &rarr; Masculine (<i>der</i>)",
                "Rain, snow, fog, and wind types are predominantly masculine.",
                "High", "der Regen, der Schnee, der Hagel, der Nebel, der Wind, der Sturm", "💡"
            )
        if lower_noun in COMPASS_DIRECTIONS:
            return make_rule(
                "Semantic", "Compass Directions (100% Masculine)",
                "Compass directions &rarr; 100% Masculine (<i>der</i>)",
                "Cardinal and intermediate directions take der.",
                "100%", "der Norden, der Süden, der Osten, der Westen", "⭐"
            )
        if lower_noun in ALCOHOLIC_DRINKS:
            return make_rule(
                "Semantic", "Alcoholic Beverages (Masculine)",
                "Alcoholic drinks &rarr; Masculine (<i>der</i>)",
                "Spirits, wines, and cocktails take der (Key exception: <i>das Bier</i>).",
                "High", "der Wein, der Wodka, der Schnaps, der Gin, der Likör, der Rum", "💡"
            )
        if lower_noun in CAR_TRAIN_BRANDS:
            return make_rule(
                "Semantic", "Automobile Brands (100% Masculine)",
                "Car makes & trains &rarr; 100% Masculine (<i>der</i>)",
                "Automobile brands and express trains take der.",
                "100%", "der BMW, der Mercedes, der Audi, der Volkswagen, der Porsche, der ICE", "⭐"
            )

    # --- MASCULINE SUFFIX -er (AGENT / INSTRUMENT) ---
    if article == "der" and lower_noun.endswith("er") and len(lower_noun) > 3 and lower_noun not in {"fenster", "zimmer", "messer", "wasser"}:
        return make_rule(
            "Suffix", "Suffix -er (Agent / Instrument ~85% Masculine)",
            "Agent suffix <b>-er</b> &rarr; ~85% Masculine (<i>der</i>)",
            "Nouns derived from verbs for professions, performers, and tools.",
            "~85%", "der Lehrer, der Fahrer, der Bäcker, der Computer, der Wecker, der Koffer", "💡"
        )

    # --- NEUTER SEMANTIC CATEGORIES ---
    if article == "das":
        if lower_noun in METALS_ELEMENTS:
            return make_rule(
                "Semantic", "Metals & Elements (~90% Neuter)",
                "Metals & elements &rarr; ~90% Neuter (<i>das</i>)",
                "Chemical elements and precious metals take das (Exception: <i>der Stahl</i>).",
                "~90%", "das Gold, das Silber, das Eisen, das Kupfer, das Aluminium, das Blei", "💡"
            )
        if lower_noun in LANGUAGES:
            return make_rule(
                "Semantic", "Languages (100% Neuter)",
                "Languages &rarr; 100% Neuter (<i>das</i>)",
                "Language names used as nouns always take das.",
                "100%", "das Deutsch, das Englisch, das Französisch, das Spanisch", "⭐"
            )
        if lower_noun in FRACTIONS:
            return make_rule(
                "Semantic", "Fractions (Neuter)",
                "Fractions &rarr; Neuter (<i>das</i>)",
                "Fractional numbers take das (Exception: <i>die Hälfte</i>).",
                "High", "das Drittel, das Viertel, das Fünftel, das Zehntel", "💡"
            )
        if lower_noun in COLORS_AS_NOUNS:
            return make_rule(
                "Semantic", "Colors as Nouns (100% Neuter)",
                "Colors &rarr; 100% Neuter (<i>das</i>)",
                "Color names used as nouns take das.",
                "100%", "das Blau, das Rot, das Grün, das Gelb, das Weiß, das Schwarz", "⭐"
            )

    # ---------------------------------------------------------
    # D. MORPHOLOGICAL RULES
    # ---------------------------------------------------------

    # 1. Nominalized Infinitives (Neuter 100%)
    if article == "das" and lower_noun.endswith("en") and len(lower_noun) > 4:
        common_infinitives = {"essen", "trinken", "leben", "schreiben", "lesen", "schwimmen", "reisen", "lernen", "schlafen", "arbeiten", "kochen", "laufen"}
        if lower_noun in common_infinitives or "ing" in meaning.lower() or "to " in meaning.lower():
            return make_rule(
                "Morphology", "Nominalized Infinitive (100% Neuter)",
                "Nominalized Infinitive &rarr; 100% Neuter (<i>das</i>)",
                "Verb infinitives used directly as nouns always take das.",
                "100%", "das Essen, das Trinken, das Leben, das Schreiben, das Lesen, das Schwimmen", "⭐"
            )

    # 2. Feminine 2-syllable nouns ending in -e (~90% Feminine)
    if article == "die" and lower_noun.endswith("e") and not lower_noun.startswith("ge"):
        if lower_noun not in WEAK_MASCULINE_E and lower_noun not in NEUTER_E_EXCEPTIONS:
            return make_rule(
                "Morphology", "Ending in -e (~90% Feminine)",
                "Ending in <b>-e</b> &rarr; ~90% Feminine (<i>die</i>)",
                "Most two-syllable native nouns ending in -e are feminine.",
                "~90%", "die Sonne, die Erde, die Straße, die Blume, die Tasche, die Reise, die Lampe", "💡"
            )

    # 3. Weak Masculine Nouns ending in -e
    if article == "der" and lower_noun.endswith("e") and lower_noun in WEAK_MASCULINE_E:
        return make_rule(
            "Morphology", "Weak Masculine in -e (N-Deklination)",
            "Weak masculine noun in <b>-e</b> (N-Deklination)",
            "Male entity nouns ending in -e take -n in all oblique cases.",
            "100%", "der Junge, der Kunde, der Kollege, der Name, der Löwe, der Experte", "⭐"
        )

    # 4. True Monosyllabic Verb Root Nouns (Stammverben ~80% Masculine)
    if article == "der" and lower_noun in VERB_STEM_NOUNS:
        return make_rule(
            "Morphology", "Monosyllabic Verb-Stem Noun (~80% Masculine)",
            "Verb root noun (Stammverb) &rarr; ~80% Masculine (<i>der</i>)",
            "Nouns formed directly from strong verb roots without a suffix.",
            "~80%", "der Lauf (laufen), der Sprung (springen), der Schlaf (schlafen), der Sitz (sitzen), der Flug (fliegen)", "💡"
        )

    # ---------------------------------------------------------
    # E. FALLBACK FOR ROOT NOUNS WITHOUT RULES (EMPTY)
    # ---------------------------------------------------------
    return {
        "article": article,
        "category": "None",
        "rule_name": "",
        "summary": "",
        "detail": "",
        "rule_text": "",
        "confidence": "",
        "examples": "",
        "icon": ""
    }


# ==========================================
# 4. DETAILED PLURAL RULES LOGIC
# ==========================================

def get_plural_rule(noun: str, article: str, plural: str) -> Dict[str, Any]:
    """
    Determines the linguistic pattern and rule for forming the plural of a German noun.
    Returns structured 2-tier summary and detailed explanation.
    """
    article = article.lower().strip()
    clean_noun = noun.strip()
    clean_plural = plural.strip()
    lower_noun = clean_noun.lower()
    lower_plural = clean_plural.lower()
    
    def make_plural_rule(pattern: str, rule_name: str, summary: str, detail: str, examples: str, icon: str = "💡"):
        return {
            "pattern": pattern,
            "rule_name": rule_name,
            "summary": summary,
            "detail": detail,
            "rule_text": f"{summary}<br><span style='font-size: 13.5px; opacity: 0.85;'>{detail}</span>",
            "examples": examples,
            "icon": icon
        }

    # 0. Singular-only nouns (No plural)
    if not clean_plural or lower_plural in ("-", "kein plural", "ohne plural", "nur singular"):
        return make_plural_rule(
            "Singulariatantum", "Singular-only Noun (Kein Plural)",
            "<b>Singulariatantum</b> &rarr; Nur Singular (kein Plural)",
            "Dieses Substantiv existiert im Deutschen standardmäßig nur im Singular und bildet keine Pluralform.",
            f"{article} {clean_noun}", "📌"
        )

    # 1. Diminutives -chen / -lein (No change)
    if lower_noun.endswith("chen") or lower_noun.endswith("lein"):
        return make_plural_rule(
            "- (No change)", "Diminutives (100% No Change)",
            "Diminutives (<b>-chen / -lein</b>) &rarr; No ending change",
            "Only the article changes to <i>die</i>; the noun itself stays identical.",
            "das Mädchen &rarr; die Mädchen, das Brötchen &rarr; die Brötchen", "⭐"
        )

    # 2. Neuter Collective Ge-...-e (No change)
    if article == "das" and lower_noun.startswith("ge") and lower_noun.endswith("e") and lower_plural == lower_noun:
        return make_plural_rule(
            "- (No change)", "Neuter Ge-...-e Collectives (No Change)",
            "Neuter <b>Ge-...-e</b> collectives &rarr; No ending change",
            "Only the article changes to <i>die</i>; the noun form remains the same.",
            "das Gebäude &rarr; die Gebäude, das Gebirge &rarr; die Gebirge, das Gemälde &rarr; die Gemälde", "⭐"
        )
    
    # 3. Female -in -> -innen
    if lower_noun.endswith("in") and lower_plural.endswith("innen"):
        return make_plural_rule(
            "-nen (-innen)", "Female Suffix -in &rarr; -innen (100%)",
            "Suffix <b>-in</b> &rarr; doubles 'n' and adds <b>-en</b> (<b>-innen</b>)",
            "Standard rule for all female role and profession nouns.",
            "die Lehrerin &rarr; die Lehrerinnen, die Ärztin &rarr; die Ärztinnen", "⭐"
        )

    # 4. Suffix -nis -> -nisse
    if lower_noun.endswith("nis") and lower_plural.endswith("nisse"):
        return make_plural_rule(
            "-nis &rarr; -nisse (+se)", "Suffix -nis &rarr; -nisse",
            "Suffix <b>-nis</b> &rarr; doubles 's' and adds <b>-e</b> (<b>-nisse</b>)",
            "Applies to all neuter and feminine nouns ending in -nis.",
            "das Ergebnis &rarr; die Ergebnisse, das Geheimnis &rarr; die Geheimnisse", "⭐"
        )

    # 5. Suffix -or -> -oren
    if lower_noun.endswith("or") and lower_plural.endswith("oren"):
        return make_plural_rule(
            "-or &rarr; -oren", "Suffix -or &rarr; -oren",
            "Suffix <b>-or</b> &rarr; adds <b>-en</b> (stress shifts: <i>-óren</i>)",
            "Latin masculine nouns in -or shift stress to the plural suffix.",
            "der Motor &rarr; die Motoren, der Doktor &rarr; die Doktoren, der Professor &rarr; die Professoren", "⭐"
        )

    # 6. Suffix -ismus -> -ismen
    if lower_noun.endswith("ismus") and lower_plural.endswith("ismen"):
        return make_plural_rule(
            "-ismus &rarr; -ismen", "Suffix -ismus &rarr; -ismen",
            "Suffix <b>-ismus</b> &rarr; replaces <i>-us</i> with <b>-en</b>",
            "Standard Latinate replacement pattern.",
            "der Optimismus &rarr; die Optimismen, der Realismus &rarr; die Realismen", "⭐"
        )
        
    # 7. Latin / Greek Suffix Transformations
    if lower_noun.endswith("um") and lower_plural.endswith("en"):
        return make_plural_rule(
            "-um &rarr; -en", "Latin -um &rarr; -en (100%)",
            "Latin ending <b>-um</b> &rarr; replaces with <b>-en</b>",
            "Standard plural shift for Latin neuter nouns in -um.",
            "das Museum &rarr; die Museen, das Zentrum &rarr; die Zentren, das Datum &rarr; die Daten", "⭐"
        )

    # 8. S-Plural for loanwords and vowel endings
    if lower_plural.endswith("s") and not lower_noun.endswith("s"):
        return make_plural_rule(
            "+s", "S-Plural (Loanwords & Vowel Endings)",
            "Vowel endings (<b>-a, -i, -o, -u, -y</b>) & Loanwords &rarr; add <b>-s</b>",
            "Common in English/French borrowings, acronyms, and vowel-final words.",
            "das Auto &rarr; die Autos, das Foto &rarr; die Fotos, das Handy &rarr; die Handys", "💡"
        )

    # 9. Weak Masculine Nouns in -e (+n)
    if article == "der" and lower_noun.endswith("e") and lower_plural.endswith("en"):
        return make_plural_rule(
            "+n", "Weak Masculine N-Deklination (+n)",
            "Weak masculine nouns in <b>-e</b> &rarr; add <b>-n</b>",
            "All masculine nouns of the N-Deklination add -(e)n in the plural.",
            "der Junge &rarr; die Jungen, der Kunde &rarr; die Kunden, der Name &rarr; die Namen", "⭐"
        )

    # 10. Feminine standard (-n / -en)
    if article == "die":
        if any(lower_noun.endswith(s) for s in ["ung", "heit", "keit", "schaft", "tät", "taet", "ion", "ik", "anz", "enz", "ei", "ur", "ade", "age", "ette", "thek"]):
            return make_plural_rule(
                "+en", "Feminine Suffixes (+en)",
                "Feminine suffixes (<b>-keit, -heit, -ung, -tät, -ion</b>) &rarr; add <b>-en</b>",
                "Always forms plural with -en without an umlaut.",
                "die Möglichkeit &rarr; die Möglichkeiten, die Wohnung &rarr; die Wohnungen, die Universität &rarr; die Universitäten", "⭐"
            )
        if lower_noun.endswith("e") and lower_plural.endswith("n"):
            return make_plural_rule(
                "+n", "Feminine in -e (+n)",
                "Feminine nouns in <b>-e</b> &rarr; add <b>-n</b>",
                "Nearly all feminine nouns ending in -e take -n in the plural.",
                "die Blume &rarr; die Blumen, die Katze &rarr; die Katzen, die Lampe &rarr; die Lampen", "⭐"
            )
        
        has_umlaut = any(c in lower_plural for c in ["ä", "ö", "ü", "ae", "oe", "ue"]) and not any(c in lower_noun for c in ["ä", "ö", "ü", "ae", "oe", "ue"])
        if has_umlaut and lower_plural.endswith("e"):
            return make_plural_rule(
                "Umlaut + -e", "Monosyllabic Feminine (Umlaut + -e)",
                "Monosyllabic feminine root &rarr; adds <b>Umlaut + -e</b>",
                "A distinct core group of 1-syllable feminine nouns takes an umlaut and -e.",
                "die Hand &rarr; die Hände, die Stadt &rarr; die Städte, die Nacht &rarr; die Nächte", "💡"
            )

        if lower_plural.endswith("en") or lower_plural.endswith("n"):
            return make_plural_rule(
                "+en / +n", "Feminine Standard (+en / +n)",
                "Feminine standard &rarr; adds <b>-n / -en</b>",
                "Over 90% of all feminine German nouns take -(e)n in the plural.",
                "die Frau &rarr; die Frauen, die Zeitung &rarr; die Zeitungen, die Tür &rarr; die Türen", "💡"
            )

    # 11. Masculine / Neuter in -er, -en, -el
    if lower_noun.endswith("er") or lower_noun.endswith("en") or lower_noun.endswith("el"):
        has_umlaut = any(c in lower_plural for c in ["ä", "ö", "ü", "ae", "oe", "ue"]) and not any(c in lower_noun for c in ["ä", "ö", "ü", "ae", "oe", "ue"])
        if has_umlaut:
            return make_plural_rule(
                "Umlaut + -", "Endings in -el/-en/-er with Umlaut",
                "Endings in <b>-el, -en, -er</b> &rarr; <b>Umlaut</b> only (no ending)",
                "Vowel changes to an umlaut without adding an extra suffix.",
                "der Apfel &rarr; die Äpfel, der Vater &rarr; die Väter, der Garten &rarr; die Gärten", "💡"
            )
        else:
            return make_plural_rule(
                "- (No ending)", "Endings in -el/-en/-er without Ending",
                "Endings in <b>-el, -en, -er</b> &rarr; No ending change",
                "Takes no additional plural suffix.",
                "der Lehrer &rarr; die Lehrer, der Wagen &rarr; die Wagen, das Fenster &rarr; die Fenster", "💡"
            )

    # 12. Neuter / Masculine in -er (+ Umlaut)
    if lower_plural.endswith("er") and not lower_noun.endswith("er"):
        has_umlaut = any(c in lower_plural for c in ["ä", "ö", "ü", "ae", "oe", "ue"])
        return make_plural_rule(
            "+er" + (" (with Umlaut)" if has_umlaut else ""), "Neuter/Masculine (+er + Umlaut)",
            "Monosyllabic root &rarr; adds <b>-er" + (" + Umlaut" if has_umlaut else "") + "</b>",
            "Common pattern for short 1-syllable neuter nouns.",
            "das Buch &rarr; die Bücher, das Kind &rarr; die Kinder, das Haus &rarr; die Häuser", "💡"
        )

    # 13. Masculine / Neuter monosyllabic standard in -e (+ Umlaut)
    if lower_plural.endswith("e") and not lower_noun.endswith("e"):
        has_umlaut = any(c in lower_plural for c in ["ä", "ö", "ü", "ae", "oe", "ue"]) and not any(c in lower_noun for c in ["ä", "ö", "ü", "ae", "oe", "ue"])
        if has_umlaut:
            return make_plural_rule(
                "+e with Umlaut", "Monosyllabic Masculine (+e + Umlaut)",
                "Monosyllabic masculine root &rarr; adds <b>-e + Umlaut</b>",
                "Most 1-syllable masculine nouns add an umlaut and -e in the plural.",
                "der Baum &rarr; die Bäume, der Stuhl &rarr; die Stühle, der Zug &rarr; die Züge", "💡"
            )
        else:
            return make_plural_rule(
                "+e (No Umlaut)", "Standard (+e)",
                "Takes standard plural suffix <b>-e</b>",
                "Regular suffix -e without stem vowel change.",
                "der Hund &rarr; die Hunde, der Tag &rarr; die Tage, das Jahr &rarr; die Jahre", "💡"
            )

    # Fallback
    return {
        "pattern": f"{clean_noun} &rarr; {clean_plural}",
        "rule_name": "Plural Form",
        "summary": f"Plural: <b>die {clean_plural}</b>",
        "detail": "",
        "rule_text": f"Forms plural as <b>die {clean_plural}</b>.",
        "examples": f"{article} {clean_noun} &rarr; die {clean_plural}",
        "icon": "💡"
    }


def get_highlighted_plural(singular: str, plural: str) -> str:
    """
    Highlights the morphological plural changes (Umlaut shifts and plural endings).
    Example:
      Hund -> Hund<span class="plural-highlight">e</span>
      Möglichkeit -> Möglichkeit<span class="plural-highlight">en</span>
      Buch -> B<span class="plural-highlight">ü</span>ch<span class="plural-highlight">er</span>
      Baum -> B<span class="plural-highlight">ä</span>um<span class="plural-highlight">e</span>
      Mutter -> M<span class="plural-highlight">ü</span>tter
      Apfel -> <span class="plural-highlight">Ä</span>pfel
      Auto -> Auto<span class="plural-highlight">s</span>
    """
    import difflib
    
    sing = singular.strip()
    plur = plural.strip()
    if not plur or sing == plur:
        return plur

    # Check simple suffix first (e.g. Hund -> Hunde, Frau -> Frauen)
    if plur.startswith(sing):
        suffix = plur[len(sing):]
        return f"{sing}<span class=\"plural-highlight\">{suffix}</span>"

    # Common foreign transformations (e.g. Museum -> Museen, Thema -> Themen)
    for old_suf, new_suf in [("um", "en"), ("us", "en"), ("a", "en"), ("ium", "ien"), ("is", "en")]:
        if sing.lower().endswith(old_suf) and plur.lower().endswith(new_suf):
            stem = sing[:-len(old_suf)]
            if plur.lower().startswith(stem.lower()):
                return f"{plur[:len(stem)]}<span class=\"plural-highlight\">{plur[len(stem):]}</span>"

    # Sequence alignment for Umlaut changes and endings
    matcher = difflib.SequenceMatcher(None, sing.lower(), plur.lower())
    result = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            result.append(plur[j1:j2])
        elif tag in ("replace", "insert"):
            result.append(f"<span class=\"plural-highlight\">{plur[j1:j2]}</span>")
            
    return "".join(result)
