import re
import spacy
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

# EntityRuler for nlp — prevents false positives like "CH", "HR" etc.
_ruler = nlp.add_pipe("entity_ruler", before="ner")
_ruler.add_patterns(
    [
        {"label": "IGNORE", "pattern": [{"LOWER": "hello"}]},
        {"label": "IGNORE", "pattern": [{"LOWER": "ch"}]},
        {"label": "IGNORE", "pattern": [{"LOWER": "eu"}]},
        {"label": "IGNORE", "pattern": [{"LOWER": "ceo"}]},
        {"label": "IGNORE", "pattern": [{"LOWER": "hr"}]},
    ]
)

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

PATTERNS = {
    "EMAIL": re.compile(
        r"[\w.%+\-]+@[\w.\-]+\.[a-zA-Z]{2,}",
        re.IGNORECASE,
    ),
    "IBAN": re.compile(
        r"\bCH\d{2}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{1}\b",
        re.IGNORECASE,
    ),
    "AHV": re.compile(r"\b756\.\d{4}\.\d{4}\.\d{2}\b"),
    "PHONE": re.compile(
        r"(?:\+41|0041|0)"  # Swiss prefix or leading 0
        r"[\s\-]?"
        r"(?:\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"  # 044 123 45 67
        r"|\d{2}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"  # 79 123 45 67 (after +41)
        r"|\d{3}[\s\-]?\d{2}[\s\-]?\d{2}[\s\-]?\d{2}"  # 079 12 34 56
        r"|\d{3}[\s\-]?\d{3}[\s\-]?\d{3})"  # 079 123 456
        r"|\+\d{1,3}[\s\-]?\d{6,14}",  # generic intl
        re.IGNORECASE,
    ),
    "IP_ADDRESS": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "ADDRESS": re.compile(
        r"\b\w+(?:strasse|gasse|weg|allee|platz|str\.)\s*\d+",
        re.IGNORECASE,
    ),
}

# Regex dynamic data validation pattern (not masking data if it more than 16 years old)
_DATE_PATTERN = re.compile(
    r"\b(?:0?[1-9]|[12]\d|3[01])[./\-](?:0?[1-9]|1[0-2])[./\-](?:(?:19|20)\d{2}|\d{2})\b"  # DD.MM.YYYY or DD.MM.YY
    r"|\b(?:19|20)\d{2}[./\-](?:0?[1-9]|1[0-2])[./\-](?:0?[1-9]|[12]\d|3[01])\b"  # YYYY-MM-DD
)


def is_date_of_birth(date_str: str):
    for date_format in [
        "%d.%m.%Y",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y.%m.%d",
        "%Y/%m/%d",
        "%Y-%m-%d",
        "%d.%m.%y",
        "%d/%m/%y",
        "%d-%m-%y",
    ]:
        try:
            parsed = datetime.strptime(date_str, date_format)
            years_ago = (datetime.now() - parsed).days / 365.25
            return years_ago >= 16
        except ValueError:
            continue
    return False


def apply_date_of_birth(text: str, _replace):
    def replace_date(match):
        date_str = match.group()
        if is_date_of_birth(date_str):
            return _replace("DATE", date_str)
        return date_str

    return _DATE_PATTERN.sub(replace_date, text)


# ---------------------------------------------------------------------------
# Masking functions
# ---------------------------------------------------------------------------


# Regex-based masking
def apply_regex(text: str, _replace):
    def make_replacer(label):
        return lambda match: _replace(label, match.group())

    for label, pattern in PATTERNS.items():
        text = pattern.sub(make_replacer(label), text)
    return text


#  spaCy library — catches person names, Regex cannot catch free-form names like 'Sarah' or 'Hans Meier'.
def apply_spacy(text: str, _replace):
    doc = nlp(text)
    
    # Entities are processed right-to-left (reverse=True) to preserve character positions — replacing left-to-right would shift indices and corrupt subsequent replacements.
    ents = sorted(doc.ents, key=lambda el: el.start_char, reverse=True)
    for ent in ents:
        #  Minimum length of 3 characters filters out abbreviations that spaCy incorrectly labels as PER (e.g. 'EU', 'IT')
        if ent.label_ in {"PER", "PERSON"} and len(ent.text) >= 3:
            placeholder = _replace(ent.label_, ent.text)
            text = text[: ent.start_char] + placeholder + text[ent.end_char :]
    return text


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def mask(text: str):
    token_map: dict[str, str] = {}
    counters: dict[str, int] = {}

    def _replace(label: str, value: str):
        counters.update({label: counters.get(label, 0) + 1})
        placeholder = f"[{label}_{counters[label]}]"
        token_map.update({placeholder: value})
        return placeholder

    text = apply_regex(text, _replace)
    text = apply_date_of_birth(text, _replace)
    text = apply_spacy(text, _replace)
    return text, token_map


def unmask(masked_text: str, token_map: dict):
    for placeholder, original in token_map.items():
        masked_text = masked_text.replace(placeholder, original)
    return masked_text