"""Assign a script class to a token from its true (raw) bytes.

Complete characters are classed by Unicode block. A token that holds no
complete character (a partial UTF-8 sequence) is classed from its lead
byte: the missing continuation bits are filled with all-0 and all-1 to get
the range of code points it could start, and if that range sits inside one
class, the fragment gets that class (e.g. E0 A4 -> U+0900..U+093F ->
Devanagari).
"""

from __future__ import annotations

from collections import Counter

# (lo, hi, class), checked in order.
RANGES = [
    (0x0000, 0x007F, "ASCII"),
    (0x0080, 0x024F, "Latin-ext"), (0x1E00, 0x1EFF, "Latin-ext"),
    (0x0250, 0x02FF, "Latin-ext"),            # IPA, spacing modifiers
    (0x0300, 0x036F, "Combining marks"),
    (0x0370, 0x03FF, "Greek"), (0x1F00, 0x1FFF, "Greek"),
    (0x0400, 0x052F, "Cyrillic"), (0x1C80, 0x1C8F, "Cyrillic"),
    (0x0530, 0x058F, "Other scripts"),        # Armenian
    (0x0590, 0x05FF, "Hebrew"),
    (0x0600, 0x06FF, "Arabic"), (0x0750, 0x077F, "Arabic"), (0x08A0, 0x08FF, "Arabic"),
    (0xFB50, 0xFDFF, "Arabic"), (0xFE70, 0xFEFF, "Arabic"),
    (0x0700, 0x08FF, "Other scripts"),        # Syriac, Thaana, NKo, ...
    (0x0900, 0x097F, "Devanagari"), (0xA8E0, 0xA8FF, "Devanagari"),
    (0x0980, 0x09FF, "Bengali"),
    (0x0A00, 0x0A7F, "Gurmukhi"),
    (0x0A80, 0x0AFF, "Gujarati"),
    (0x0B00, 0x0B7F, "Oriya"),
    (0x0B80, 0x0BFF, "Tamil"),
    (0x0C00, 0x0C7F, "Telugu"),
    (0x0C80, 0x0CFF, "Kannada"),
    (0x0D00, 0x0D7F, "Malayalam"),
    (0x0D80, 0x0DFF, "Other scripts"),        # Sinhala
    (0x0E00, 0x0E7F, "Thai"),
    (0x0E80, 0x109F, "Other scripts"),        # Lao, Tibetan, Myanmar
    (0x10A0, 0x10FF, "Other scripts"),        # Georgian
    (0x1100, 0x11FF, "Hangul"), (0x3130, 0x318F, "Hangul"), (0xA960, 0xA97F, "Hangul"),
    (0xAC00, 0xD7FF, "Hangul"),
    (0x1200, 0x1DFF, "Other scripts"),        # Ethiopic ... Khmer, Mongolian, etc.
    (0x2000, 0x206F, "Punctuation/symbols"),
    (0x2070, 0x2BFF, "Punctuation/symbols"),  # super/subscripts, arrows, math, box, misc
    (0x2C00, 0x2E7F, "Other scripts"),
    (0x2E80, 0x2FFF, "CJK Han"),              # radicals
    (0x3000, 0x303F, "CJK symbols"),
    (0x3040, 0x30FF, "Kana"), (0x31F0, 0x31FF, "Kana"),
    (0x3100, 0x33FF, "CJK symbols"),          # bopomofo, enclosed, compat
    (0x3400, 0x4DBF, "CJK Han"), (0x4DC0, 0x4DFF, "Punctuation/symbols"),
    (0x4E00, 0x9FFF, "CJK Han"),
    (0xA000, 0xABFF, "Other scripts"),
    (0xE000, 0xF8FF, "Private use"),
    (0xF900, 0xFAFF, "CJK Han"),
    (0xFE00, 0xFE0F, "Emoji"),                # variation selectors
    (0xFE10, 0xFE6F, "CJK symbols"),
    (0xFF00, 0xFF65, "CJK symbols"),          # fullwidth forms
    (0xFF66, 0xFF9F, "Kana"),
    (0xFFA0, 0xFFFC, "CJK symbols"),
    (0xFFFD, 0xFFFD, "Replacement char"),
    (0xFFFE, 0xFFFF, "Other scripts"),
    (0x1F000, 0x1FAFF, "Emoji"),
    (0x10000, 0x1EFFF, "Other scripts"),
    (0x20000, 0x3FFFF, "CJK Han"),
    (0xE0000, 0xE007F, "Emoji"),              # tags (flag sequences)
    (0xE0080, 0x10FFFF, "Private use"),
]
EMOJI_CHARS = {0x200D, 0x20E3}  # ZWJ, keycap


def class_of_cp(cp: int) -> str:
    if cp in EMOJI_CHARS:
        return "Emoji"
    if 0x2600 <= cp <= 0x27BF:
        return "Emoji"
    for lo, hi, c in RANGES:
        if lo <= cp <= hi:
            return c
    return "Other scripts"


def _range_class(lo: int, hi: int) -> str | None:
    """Class if the whole code point range [lo, hi] lies in one class."""
    classes = set()
    for a, b, c in RANGES:
        if b < lo or a > hi:
            continue
        classes.add(c)
        if len(classes) > 1:
            return None
    covered = sum(min(b, hi) - max(a, lo) + 1 for a, b, _ in RANGES if not (b < lo or a > hi))
    if 0x2600 <= lo and hi <= 0x27BF:
        return "Emoji"
    return classes.pop() if len(classes) == 1 and covered >= (hi - lo + 1) else None


def _seq_len(lead: int) -> int:
    if lead >> 5 == 0b110:
        return 2
    if lead >> 4 == 0b1110:
        return 3
    if lead >> 3 == 0b11110:
        return 4
    return 0


def fragment_class(raw: bytes) -> str:
    """Class for a byte string with no complete character, from its lead byte."""
    saw_invalid_lead = False
    for k, b in enumerate(raw):
        if b in (0xC0, 0xC1) or b >= 0xF5:
            saw_invalid_lead = True  # can never start valid UTF-8
            continue
        n = _seq_len(b)
        if n == 0:
            continue
        cont = raw[k + 1 : k + n]
        if any((c & 0xC0) != 0x80 for c in cont):
            continue
        payload_bits = {2: 5, 3: 4, 4: 3}[n]
        val = b & ((1 << payload_bits) - 1)
        for c in cont:
            val = (val << 6) | (c & 0x3F)
        missing = n - 1 - len(cont)
        lo = val << (6 * missing)
        hi = lo | ((1 << (6 * missing)) - 1)
        c = _range_class(lo, hi)
        return f"{c} (fragment)" if c else "Mixed (fragment)"
    return "Invalid UTF-8 byte" if saw_invalid_lead else "Continuation bytes only"


def token_class(raw: bytes, kind: str) -> str:
    if kind == "special":
        return "Special"
    if kind == "added_literal":
        return "Added/control literal"
    if kind == "unassigned" or len(raw) == 0:
        return "Empty"
    try:
        text = raw.decode("utf-8")
        valid = True
    except UnicodeDecodeError:
        # Keep only the characters that decode cleanly; a U+FFFD left in
        # `text` is a literal U+FFFD in the token, not a decode artifact.
        text = raw.decode("utf-8", errors="ignore")
        valid = False
    counts = Counter()
    for ch in text:
        c = class_of_cp(ord(ch))
        if c not in ("ASCII", "Combining marks") and not ch.isspace():
            counts[c] += 1
    if counts:
        return counts.most_common(1)[0][0]
    if not valid:
        # Only ASCII/whitespace decoded; the script lives in the fragment.
        return fragment_class(raw)
    if text.isspace():
        return "Whitespace"
    if any(class_of_cp(ord(ch)) == "Combining marks" for ch in text):
        return "Combining marks"
    return "ASCII"
