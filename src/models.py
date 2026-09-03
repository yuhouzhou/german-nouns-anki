"""
Anki Note Models, Card Templates, and Full-Screen Responsive Styling.
Supports 2-tier concise glanceable summary + detailed rule explanation.
"""

import genanki

# Unique stable Model IDs for Anki
GERMAN_GENDER_MODEL_ID = 1725109411
GERMAN_PLURAL_MODEL_ID = 1725109422

# Full-screen, edge-to-edge modern styling for all devices (with native iOS / system Dark Mode support)
FULL_SCREEN_CSS = """
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #ffffff;
}

.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 20px;
  text-align: center;
  color: #0f172a;
  background-color: #ffffff;
  padding: 24px 20px 40px 20px;
  margin: 0 auto;
  max-width: 640px;
  min-height: 85vh;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

/* Top Header Bar */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 28px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.badge {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 5px 12px;
  border-radius: 9999px;
  display: inline-flex;
  align-items: center;
}

.badge-gender {
  background: #ede9fe;
  color: #6d28d9;
}

.badge-plural {
  background: #fef3c7;
  color: #b45309;
}

.badge-level {
  background: #e0f2fe;
  color: #0369a1;
}

/* Prompts & Typography */
.prompt-title {
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 16px;
}

.main-word-area {
  margin: 12px 0 16px 0;
}

.main-noun {
  font-size: 42px;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.25;
  margin: 0;
}

.placeholder {
  color: #94a3b8;
  font-weight: 400;
  border-bottom: 3px dashed #cbd5e1;
  padding: 0 6px;
  margin-right: 4px;
}

.meaning {
  font-size: 19px;
  color: #64748b;
  margin-top: 8px;
  margin-bottom: 24px;
  font-style: italic;
  font-weight: 400;
}

/* Color Coding for Articles and Nouns */
.article {
  font-weight: 900;
  margin-right: 6px;
}

.noun {
  font-weight: 800;
}

/* Masculine - Vibrant Blue (Article + Noun) */
.der, .article-der, .der .noun, .der .article, span.der {
  color: #0284c7 !important;
}

/* Feminine - Vibrant Red (Article + Noun) */
.die, .article-die, .die .noun, .die .article, span.die {
  color: #dc2626 !important;
}

/* Neuter - Vibrant Green (Article + Noun) */
.das, .article-das, .das .noun, .das .article, span.das {
  color: #16a34a !important;
}

/* Plural Neutral Article 'die' (Black/Standard) */
.plural-article-neutral {
  color: #0f172a;
  font-weight: 800;
  margin-right: 6px;
}

/* Plural Morphology Highlight (Umlaut + Suffix) */
.plural-highlight {
  color: #e11d48 !important;
  font-weight: 900;
  border-bottom: 2.5px solid #e11d48;
  padding-bottom: 1px;
}

/* Reference Information Subtitle */
.reference-banner {
  font-size: 15px;
  color: #64748b;
  margin: 12px 0 24px 0;
  padding: 8px 14px;
  background: #f8fafc;
  border-radius: 8px;
  display: inline-block;
  align-self: center;
}

/* 2-Tier Rule / Mnemonic Box */
.rule-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 5px solid #6366f1;
  border-radius: 12px;
  padding: 16px 18px;
  text-align: left;
  margin-top: 20px;
  width: 100%;
  box-sizing: border-box;
}

.rule-header {
  font-weight: 700;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #4338ca;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Concise 1-glance headline */
.rule-summary {
  font-size: 16px;
  font-weight: 750;
  color: #0f172a;
  line-height: 1.35;
  margin-bottom: 4px;
}

/* Detailed context */
.rule-detail {
  font-size: 14px;
  color: #475569;
  line-height: 1.45;
  margin-top: 4px;
}

.rule-examples {
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px dashed #cbd5e1;
  font-size: 13px;
  color: #64748b;
  font-style: italic;
}

/* ==========================================================================
   DARK MODE / NIGHT MODE (Supports Anki nightMode & iOS system dark mode)
   ========================================================================== */

/* 1. Anki Desktop & AnkiDroid Night Mode Classes */
.nightMode html, .nightMode body, .night_mode html, .night_mode body,
body.nightMode, body.night_mode {
  background-color: #0f172a !important;
}

.nightMode .card, .night_mode .card,
.nightMode.card, .night_mode.card {
  color: #f8fafc !important;
  background-color: #0f172a !important;
}

.nightMode .card-header, .night_mode .card-header {
  border-bottom-color: #1e293b;
}

.nightMode .badge-gender, .night_mode .badge-gender {
  background: #3b0764;
  color: #d8b4fe;
}

.nightMode .badge-plural, .night_mode .badge-plural {
  background: #451a03;
  color: #fde68a;
}

.nightMode .badge-level, .night_mode .badge-level {
  background: #082f49;
  color: #7dd3fc;
}

.nightMode .prompt-title, .night_mode .prompt-title {
  color: #94a3b8;
}

.nightMode .meaning, .night_mode .meaning {
  color: #94a3b8;
}

.nightMode .der, .night_mode .der,
.nightMode .article-der, .night_mode .article-der,
.nightMode .der .noun, .night_mode .der .noun,
.nightMode .der .article, .night_mode .der .article,
.nightMode span.der, .night_mode span.der {
  color: #38bdf8 !important;
}

.nightMode .die, .night_mode .die,
.nightMode .article-die, .night_mode .article-die,
.nightMode .die .noun, .night_mode .die .noun,
.nightMode .die .article, .night_mode .die .article,
.nightMode span.die, .night_mode span.die {
  color: #f87171 !important;
}

.nightMode .das, .night_mode .das,
.nightMode .article-das, .night_mode .article-das,
.nightMode .das .noun, .night_mode .das .noun,
.nightMode .das .article, .night_mode .das .article,
.nightMode span.das, .night_mode span.das {
  color: #4ade80 !important;
}

.nightMode .plural-article-neutral, .night_mode .plural-article-neutral {
  color: #f8fafc !important;
}

.nightMode .plural-highlight, .night_mode .plural-highlight {
  color: #fb7185 !important;
  border-bottom-color: #fb7185;
}

.nightMode .reference-banner, .night_mode .reference-banner {
  background: #1e293b;
  color: #94a3b8;
}

.nightMode .rule-box, .night_mode .rule-box {
  background: #1e293b;
  border-color: #334155;
  border-left-color: #818cf8;
  color: #f1f5f9;
}

.nightMode .rule-header, .night_mode .rule-header {
  color: #a5b4fc;
}

.nightMode .rule-summary, .night_mode .rule-summary {
  color: #f8fafc;
}

.nightMode .rule-detail, .night_mode .rule-detail {
  color: #94a3b8;
}

.nightMode .rule-examples, .night_mode .rule-examples {
  border-top-color: #334155;
  color: #94a3b8;
}

/* 2. System Dark Mode: iOS / AnkiMobile / macOS System Theme */
@media (prefers-color-scheme: dark) {
  html, body {
    background-color: #0f172a !important;
  }

  .card {
    color: #f8fafc !important;
    background-color: #0f172a !important;
  }

  .card-header {
    border-bottom-color: #1e293b !important;
  }

  .badge-gender {
    background: #3b0764 !important;
    color: #d8b4fe !important;
  }

  .badge-plural {
    background: #451a03 !important;
    color: #fde68a !important;
  }

  .badge-level {
    background: #082f49 !important;
    color: #7dd3fc !important;
  }

  .prompt-title {
    color: #94a3b8 !important;
  }

  .meaning {
    color: #94a3b8 !important;
  }

  .der, .article-der, .der .noun, .der .article, span.der {
    color: #38bdf8 !important;
  }

  .die, .article-die, .die .noun, .die .article, span.die {
    color: #f87171 !important;
  }

  .das, .article-das, .das .noun, .das .article, span.das {
    color: #4ade80 !important;
  }

  .plural-article-neutral {
    color: #f8fafc !important;
  }

  .plural-highlight {
    color: #fb7185 !important;
    border-bottom-color: #fb7185 !important;
  }

  .reference-banner {
    background: #1e293b !important;
    color: #94a3b8 !important;
  }

  .rule-box {
    background: #1e293b !important;
    border-color: #334155 !important;
    border-left-color: #818cf8 !important;
    color: #f1f5f9 !important;
  }

  .rule-header {
    color: #a5b4fc !important;
  }

  .rule-summary {
    color: #f8fafc !important;
  }

  .rule-detail {
    color: #94a3b8 !important;
  }

  .rule-examples {
    border-top-color: #334155 !important;
    color: #94a3b8 !important;
  }
}
"""

# HTML Template: GENDER CARD FRONT
GENDER_FRONT_HTML = """
<div class="card">
  <div class="card-header">
    <span class="badge badge-gender">GENDER</span>
    {{#Level}}<span class="badge badge-level">{{Level}}</span>{{/Level}}
  </div>
  
  <div class="prompt-title">Which article (der / die / das)?</div>
  
  <div class="main-word-area">
    <div class="main-noun"><span class="placeholder">___</span> {{Noun}}</div>
    {{#Meaning}}<div class="meaning">{{Meaning}}</div>{{/Meaning}}
  </div>
</div>
"""

# HTML Template: GENDER CARD BACK
GENDER_BACK_HTML = """
<div class="card">
  <div class="card-header">
    <span class="badge badge-gender">GENDER</span>
    {{#Level}}<span class="badge badge-level">{{Level}}</span>{{/Level}}
  </div>
  
  <div class="main-word-area">
    <div class="main-noun {{Article}}">
      <span class="article {{Article}}">{{Article}}</span> <span class="noun {{Article}}">{{Noun}}</span>
    </div>
    {{#Meaning}}<div class="meaning">{{Meaning}}</div>{{/Meaning}}
  </div>

  {{#GenderRuleSummary}}
  <div class="rule-box">
    <div class="rule-header"><span>💡</span> Rule Hint</div>
    <div class="rule-summary">{{GenderRuleSummary}}</div>
    {{#GenderRuleDetail}}
    <div class="rule-detail">{{GenderRuleDetail}}</div>
    {{/GenderRuleDetail}}
    {{#GenderRuleExamples}}
    <div class="rule-examples">Examples: {{GenderRuleExamples}}</div>
    {{/GenderRuleExamples}}
  </div>
  {{/GenderRuleSummary}}

  {{#Notes}}
  <div class="rule-box" style="border-left-color: #10b981; margin-top: 12px;">
    <div class="rule-header" style="color: #059669;"><span>📌</span> Note</div>
    <div class="rule-body">{{Notes}}</div>
  </div>
  {{/Notes}}
</div>
"""

# HTML Template: PLURAL CARD FRONT
PLURAL_FRONT_HTML = """
<div class="card">
  <div class="card-header">
    <span class="badge badge-plural">PLURAL</span>
    {{#Level}}<span class="badge badge-level">{{Level}}</span>{{/Level}}
  </div>
  
  <div class="prompt-title">What is the plural form?</div>
  
  <div class="main-word-area">
    <div class="main-noun {{Article}}">
      <span class="article {{Article}}">{{Article}}</span> <span class="noun {{Article}}">{{Noun}}</span>
    </div>
    {{#Meaning}}<div class="meaning">{{Meaning}}</div>{{/Meaning}}
  </div>

  <div style="margin: 24px 0 16px 0;">
    <div class="prompt-title">Plural Form:</div>
    <div class="main-noun" style="font-size: 34px;">
      <span class="placeholder" style="padding: 0 24px;">__________</span>
    </div>
  </div>
</div>
"""

# HTML Template: PLURAL CARD BACK
PLURAL_BACK_HTML = """
<div class="card">
  <div class="card-header">
    <span class="badge badge-plural">PLURAL</span>
    {{#Level}}<span class="badge badge-level">{{Level}}</span>{{/Level}}
  </div>
  
  <div class="main-word-area">
    <div class="main-noun">
      {{PluralHighlighted}}
    </div>
    {{#Meaning}}<div class="meaning">{{Meaning}}</div>{{/Meaning}}
  </div>

  <div class="reference-banner">
    Singular: <span class="{{Article}}"><b>{{Article}} {{Noun}}</b></span>
  </div>

  {{#PluralRuleSummary}}
  <div class="rule-box">
    <div class="rule-header"><span>💡</span> Plural Formation</div>
    <div class="rule-summary">{{PluralRuleSummary}}</div>
    {{#PluralRuleDetail}}
    <div class="rule-detail">{{PluralRuleDetail}}</div>
    {{/PluralRuleDetail}}
    {{#PluralRuleExamples}}
    <div class="rule-examples">Pattern examples: {{PluralRuleExamples}}</div>
    {{/PluralRuleExamples}}
  </div>
  {{/PluralRuleSummary}}

  {{#Notes}}
  <div class="rule-box" style="border-left-color: #10b981; margin-top: 12px;">
    <div class="rule-header" style="color: #059669;"><span>📌</span> Note</div>
    <div class="rule-body">{{Notes}}</div>
  </div>
  {{/Notes}}
</div>
"""


def create_gender_model() -> genanki.Model:
    """Creates dedicated model for Gender cards with 2-tier rule explanations."""
    return genanki.Model(
        model_id=GERMAN_GENDER_MODEL_ID,
        name="German Noun - Gender Card",
        fields=[
            {"name": "Noun"},
            {"name": "Article"},
            {"name": "Plural"},
            {"name": "Meaning"},
            {"name": "Level"},
            {"name": "GenderRuleSummary"},
            {"name": "GenderRuleDetail"},
            {"name": "GenderRuleExamples"},
            {"name": "Notes"},
        ],
        templates=[
            {
                "name": "Gender Card",
                "qfmt": GENDER_FRONT_HTML,
                "afmt": GENDER_BACK_HTML,
            }
        ],
        css=FULL_SCREEN_CSS
    )


def create_plural_model() -> genanki.Model:
    """Creates dedicated model for Plural cards with morphological highlighting."""
    return genanki.Model(
        model_id=GERMAN_PLURAL_MODEL_ID,
        name="German Noun - Plural Card",
        fields=[
            {"name": "Noun"},
            {"name": "Article"},
            {"name": "Plural"},
            {"name": "PluralHighlighted"},
            {"name": "Meaning"},
            {"name": "Level"},
            {"name": "PluralRuleSummary"},
            {"name": "PluralRuleDetail"},
            {"name": "PluralRuleExamples"},
            {"name": "Notes"},
        ],
        templates=[
            {
                "name": "Plural Card",
                "qfmt": PLURAL_FRONT_HTML,
                "afmt": PLURAL_BACK_HTML,
            }
        ],
        css=FULL_SCREEN_CSS
    )
