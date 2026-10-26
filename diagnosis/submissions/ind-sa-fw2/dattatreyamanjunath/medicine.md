# Medicine sheet: ind-sa-fw2 (dattatreyamanjunath)

Pack: 500 Sanskrit documents from FineWeb-2 (Devanagari). Labels: `labels.csv` (291 fix, 115 clean, 94 drop).

## About the harm tests

The official Sanskrit gold set is not in the lab repository yet. The Data A and Data B teams own it. Until it is
published, every harm test below runs on a **proxy gold set: the 115 documents of this pack that I labelled
`clean`**. The 1% limit on 115 documents allows at most one changed or dropped document.

This proxy is weaker than the real gold set. One reader (me) marked these documents clean, and some of my
labelling tools use the same patterns as these medicines. I will rerun every test on the gold set when it is
published and update the numbers.

For each medicine I also give its **reach**: how many of the documents that I labelled with the disease it changes
or drops. This shows how much of the disease the medicine removes.

### Shared definitions

All the code below is Python 3 with `re`. Each medicine is `f(text, url)`. It returns the new text, or `None` to drop
the document.

```python
import re
from urllib.parse import urlparse

DEVA  = "\u0900-\u097F"                    # Devanagari block
CONS  = "\u0915-\u0939\u0958-\u095F"       # consonants
MATRA = "\u093E-\u094C\u0962\u0963"        # dependent vowel signs

def host(url):
    return urlparse(url).netloc.lower().removeprefix("www.")
```

### Running order

1. Drop medicines: D4, A3 (drop part), A4, C3, G3, D1.
2. Line removal: C1, C5, then D2/D3/H3.
3. Character fixes: B5, A5, A6, A3 (fix part), G1, C4.
4. F1 masking last, so that no other rule moves a masked span.

### Summary

| Disease | Count | Action | Proxy gold: changed / dropped | Result | Reach on labelled docs |
|---|---|---|---|---|---|
| A3 | 14 | fix (drop if ≥ 3 Latin-1 letters) | 0 / 0 | pass | 7 of 14 |
| A4 | 6 | drop | 0 / 0 | pass | 2 of 6 |
| A5 | 20 | fix | 0 / 0 | pass | 14 of 20 |
| A6 | 140 | fix | 0 / 0 | pass | 114 of 140 |
| B5 | 38 | fix | 0 / 0 | pass | 30 of 38 |
| C1 | 159 | fix (remove lines) | 0 / 0 | pass | 100 of 159 |
| C3 | 45 | drop | 0 / 0 | pass | 31 of 45 |
| C4 | 14 | fix (split items) | 1 / 0 (0.9%) | pass | 2 of 14 |
| C5 | 7 | fix (remove lines) | 0 / 0 | pass | 2 of 7 |
| D2 | 6 | fix (remove lines) | 0 / 0 | pass | 6 of 6 |
| D3 | 98 | fix (remove lines) | 0 / 0 | pass | 53 of 98 |
| D4 | 56 | drop | 0 / 0 | pass | 42 of 56 |
| F1 | 8 | fix (mask) | 0 / 0 | pass | 5 of 8 |
| G1 | 11 | fix | 0 / 0 | pass | 6 of 11 |
| G3 | 10 | drop | 0 / 0 | pass | 4 of 10 |
| H3 | 9 | fix (remove lines) | 0 / 0 | pass | 8 of 9 |

---

## Medicine 1: A6, ASCII and other-script look-alikes for Devanagari signs

1. **Disease:** A6, 140 documents.
   - `6da72db6a95c25b8`: `बुद्धि: वर्धते` at 382. U+003A COLON is used for U+0903 VISARGA.
   - `ab5a31ed73334c94`: `वनामवीरा:` at 51762, 96 times.
   - `faa8d8f77429473d`: `पलायिता |` at 1726. U+007C VERTICAL LINE is used for U+0964 DANDA.

   Other forms in the pack: `S`/`s` for avagraha (`कोSपि`), `||` for `॥`, Latin `I` for `।`, and Dravidian short
   vowel signs U+0946/U+094A and RRA U+0931 typed on South-Indian keyboards.
2. **Medicine:** replace each look-alike with the Devanagari sign, but only in a Devanagari context.
   - Colon: only after a consonant or vowel sign. Keep abbreviations (`डा:`, `प्रो:`) and labels followed by
     another script.
   - Pipes: never inside `|table|` lines.

   ```python
   ABBR = re.compile(r"(?:^|[\s(])(डा|डॉ|प्रो|डो|श्री|सं|पृ|ई|क्र|पं|मो|फो|दू)$")

   def m_a6(t, url=""):
       def colon(m):
           before = t[max(0, m.start() - 6):m.start()]
           after = t[m.end():m.end() + 3].lstrip()
           if ABBR.search(before) or (after and after[0].isalpha() and not "\u0900" <= after[0] <= "\u097F"):
               return m.group()          # 'डा:' abbreviation, or a label like '(गुजराती: મહારાજા'
           return "ः"
       t = re.sub(f"(?<=[{CONS}{MATRA}]):(?=[\\s।॥]|$)", colon, t)
       t = re.sub(f"(?<=[{CONS}{MATRA}\u0902\u0903])[Ss](?=[{CONS}])", "ऽ", t)        # कोSपि -> कोऽपि
       out = []
       for line in t.split("\n"):
           if not (line.startswith("|") or line.rstrip().endswith("|") and line.count("|") > 2):
               line = re.sub(f"(?<=[{DEVA}]) ?\\|\\|(?=\\s|$)", " ॥", line)
               line = re.sub(f"(?<=[{DEVA}]) ?\\|(?=\\s|$)", " ।", line)
           line = re.sub(f"(?<=[{DEVA}]) ?I(?=\\s*$|\\s+[{DEVA}])", " ।", line)   # not the pronoun 'I have'
           out.append(line)
       return "\n".join(out).translate({0x0946: 0x0947, 0x094A: 0x094B, 0x0931: 0x0930})
   ```
3. **Action:** fix the text.
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 114 of 140 labelled documents.
5. **Side effects:**
   - A colon inside a film or book title written in Devanagari becomes a visarga (`पुष्पा: द राइज` →
     `पुष्पाः द राइज`, doc `437c577e8ee18f35`).
   - Abbreviations missing from the list (for example a new title like `ले:`) also change.
   - Rarer look-alikes are not covered: Tamil `உ`, `∫` and `$` for avagraha, `..` for danda, and the Bengali danda
     `৷`. These are the 26 documents that the medicine does not reach.

## Medicine 2: A5, broken vowel composition

1. **Disease:** A5, 20 documents.
   - `58b5cd30c9ab7965`: `सुखाभेेदेऽपि` at 5572. U+0947 is written twice, 3 times in the document.
   - `18f91690f821fc5c`: `नियुुक्तवान्` at 922. U+0941 is written twice.
   - `1c9a474c47bee521`: `भाागं` at 350. U+093E is written twice.

   NFC normalisation repairs neither doubled signs nor `अ` + vowel sign (`अा` for `आ`).
2. **Medicine:** join `अ` + vowel sign into the full vowel, and remove a repeated identical vowel sign.
   ```python
   FULL = {"ा": "आ", "ि": "इ", "ी": "ई", "ु": "उ", "ू": "ऊ", "ृ": "ऋ", "े": "ए", "ै": "ऐ", "ो": "ओ", "ौ": "औ"}

   def m_a5(t, url=""):
       t = re.sub("अ([ािीुूृेैोौ])", lambda m: FULL[m.group(1)], t)
       return re.sub(f"([{MATRA}])\\1+", r"\1", t)
   ```
3. **Action:** fix the text.
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 14 of 20.
5. **Side effects:**
   - Two different stacked vowel signs (`ोि`) come from OCR. The right letter is unknown, so the medicine leaves
     them; that is 6 of the 20 documents.
   - A doubled sign that is in fact a typo for a different sign is "fixed" to the wrong spelling.

## Medicine 3: A3, legacy-font conversion damage

1. **Disease:** A3, 14 documents.
   - `8c013ba00a9f2d63`: `मूÞर्य` at 5094. U+00DE LATIN CAPITAL LETTER THORN sits inside a Devanagari word.
   - `4a7f9e10226e7615`: `कोऽलडूकारः` at 81, for `अलङ्कारः`.
   - `9391f62e9dfa7a72`: `त्तमालङकृतं` at 1326. ङ has no virama before क (`ङ्क` expected).
2. **Medicine:**
   - Drop a document with three or more Latin-1 letters glued to Devanagari; such text cannot be mapped back.
   - Otherwise, restore the virama in `ङ` + velar consonant. Without the virama this pair does not occur in
     Sanskrit, except after `ङ्ङ्` in Vedic.

   ```python
   LEGACY = re.compile(f"(?<=[{DEVA}])[\u00C0-\u00FF]|[\u00C0-\u00FF](?=[{DEVA}])")

   def m_a3(t, url=""):
       if len(LEGACY.findall(t)) >= 3:
           return None
       return re.sub("(?<!ङ्)ङ(?=[कखगघ])", "ङ्", t)     # 'हिङ्ङकृणोत्' is correct Vedic, keep it
   ```
3. **Action:** fix the text (drop when the font damage cannot be mapped).
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 7 of 14.
5. **Side effects:**
   - Sandhi of `ङ्` + `अ` + velar (`प्राङ् + अकरोत्` → `प्राङकरोत्`) is correct Sanskrit and would wrongly get a
     virama. I found no such case in the pack. An earlier version of this rule also hit `क्यङभाव`
     (`क्यङ् + अभाव`), so it now fires only before velars.
   - The `न्त` → `त्त` and `ङ्क` → `डू` font swaps (`भगवत्तमेव`, `अलडूकारः`) are not repaired. They need a
     dictionary.

## Medicine 4: A4, lost characters

1. **Disease:** A4, 6 documents.
   - `935e30775b66fab4`: the illegible-character marker `{??}` in `{??}रुणं` at 43354.
   - `605046c0f09bb50f`: `नक्तम{??}दञ्च{??}` at 90485, 3 markers.
   - `64a9b96746d003f8`: syllables lost with no marker, `विरराग्सुतर्पितः` at 1390.
2. **Medicine:** drop a document that contains U+FFFD or the `{??}` marker.
   ```python
   def m_a4(t, url=""):
       return None if ("\uFFFD" in t or "{??}" in t) else t
   ```
3. **Action:** drop the document.
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 2 of 6.
5. **Side effects:**
   - One `{??}` in a 90,000-character commentary drops a long, otherwise good text. A softer version would cut only
     the marked sentence.
   - Syllables lost without a marker (4 of 6 documents) are not found. A Sanskrit language model flags some of them
     (high bits per character), but it also flags Vedic accents, so I did not make it a rule.

## Medicine 5: B5, wiki and edition markup

1. **Disease:** B5, 38 documents.
   - `903b4cc1c43738cd`: `[सम्पादन]` at 5, 3 times.
   - `b54ef4486f508f61`: `[[लेखकः :|]]` at 106.
   - `f4b042caef15747c`: `[सम्पाद्यताम्]` at 20, 3 times.

   Other forms: `{{…}}` templates, `'''` bold marks, `[Page1234-a+ 12]` page markers, `↩` footnote back-links and
   `[^१]` footnote marks.
2. **Medicine:** unwrap `[[link|text]]` to `text`, and remove the other markup tokens.
   ```python
   B5 = [r"\[(सम्पाद्यताम्|सम्पादयतु|सम्पादन)\]", r"\{\{[^{}\n]*\}\}", r"'''", r"\[Page\d+-[a-z]\+ ?\d+\]", "↩",
         r"\[\^[०-९\d]+\]"]

   def m_b5(t, url=""):
       t = re.sub(r"\[\[(?:[^|\]\n]*\|)?([^\]\n]*)\]\]", r"\1", t)
       for p in B5:
           t = re.sub(p, "", t)
       return t
   ```
3. **Action:** fix the text.
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 30 of 38.
5. **Side effects:**
   - `'''` inside a quoted Sanskrit text, used as a real triple quote, would be removed.
   - Not covered: edition page numbers glued into words (`पूर्वोत्त772रपद`), which need a per-site rule, and
     infobox table remnants (`|लेखकः||…|`).

## Medicine 6: C1, boilerplate lines

1. **Disease:** C1, 159 documents.
   - `6da72db6a95c25b8`: 27 blog-menu lines, first `Menu` at 0.
   - `76073b33992af5b6`: `Did you see any mistake/variation in the content above?…` at 621. This is the
     stotranidhi footer.
   - `7d763858a5acae02`: `अथर्ववेद में पूरणः के 10 संदर्भ मिले` at 109. This is a Hindi site banner.
2. **Medicine:** remove whole lines that match a list of site boilerplate patterns. A pattern that could be real
   Sanskrit is tied to its site: SARIT's closing `श्रीः` is removed only on `sarit.indology.info`, only as the last
   line.
   ```python
   C1_ANY = [r"^(Menu|Home|Newer Post|Older Post|Gallery|BASPS|marquee|Technical Details|BACK TO TOP)$",
       r"^(Read Also|Read More|Leave a Reply|Click Here|Archives|ReplyDelete|Reply|Delete|Share|Tweet|Email This|BlogThis!)$",
       r"^(Labels?|Categories|Posted by|Source):", r"Did you see any mistake/variation", r"Digitized by Google",
       r"Since you are not logged in", r"^% (Site access|Language|Text title|File name|Location|Author|Transliterated by|Proofread by|Description|Latest update|Send corrections)",
       r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), \w+ \d{1,2}, \d{4}$", r"^\d{1,2}:\d\d [AP]M$",
       r"^\|← ", r"→\|$", r"^इतर .*पश्यतु\s*[।|]?$", r"^\[सम्पाद्यताम्\]$", r"^— .*\(@\w+\) \w+ \d{1,2}, \d{4}$",
       r"^(सामग्री पर जाएँ|मुख्य मेन्यू|साइडबार पर जाएँ|छुपाएँ|ऊपर जाएँ|अधिक जानें|क्रियाएँ|उपकरण)$",
       r"^(ऋग्वेद|अथर्ववेद|यजुर्वेद|सामवेद) में .* संदर्भ मिले$", r"Copyright|©|All rights reserved",
       r"हम उम्मीद करते हैं आपको", r"^इसे भी पढ़ें"]
   C1_RX = re.compile("|".join(f"(?:{p})" for p in C1_ANY), re.I)
   C1_SITE = {"sarit.indology.info": re.compile(r"^श्रीः$")}

   def m_c1(t, url=""):
       keep = [l for l in t.split("\n") if not C1_RX.search(l.strip())]
       site = C1_SITE.get(host(url))
       while site and keep and site.match(keep[-1].strip()):
           keep.pop()
       return "\n".join(keep)
   ```
3. **Action:** fix the text (remove the lines).
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 100 of 159.
5. **Side effects:**
   - A Sanskrit line that is exactly `Home` or `Source: …` would go. A stotra that ends with the word `श्रीः` on
     SARIT would lose it.
   - Not covered: one-off boilerplate (author credit lines, English SEO titles, translator credits, embedded
     tweets without a handle line). Those 59 documents need new patterns per site.

## Medicine 7: C3, scan-page and cut fragments

1. **Disease:** C3, 45 documents.
   - `046f85c956521bff`: a sa.wikisource scan page cut mid-verse, `…सच्छष्कुलीनास ।` at 1096.
   - `14ee406c9fcc5df9`: ends mid-sentence, `…एकेन वर्धयित्वा न्यूनीकरोतु,` at 1005.
   - `95def3e2f7070b5d`: ends mid-reference, `…॥ 5-192-` at 7138.
2. **Medicine:** sa.wikisource `पृष्ठम्:` pages are single scanned book pages, often unproofread OCR, that start and
   stop mid-text. Drop them by URL.
   ```python
   PAGE_NS = "wikisource.org/wiki/%E0%A4%AA%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A0%E0%A4%AE%E0%A5%8D:"   # 'पृष्ठम्:'

   def m_c3(t, url=""):
       return None if PAGE_NS in url else t
   ```
3. **Action:** drop the document.
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 31 of 45. The rule also drops 12 more
   scan pages that I had labelled `drop` for other reasons (OCR errors).
5. **Side effects:**
   - A well-proofread scan page is dropped together with the bad ones. A better rule keeps pages from the same book
     and joins them in order.
   - Truncated blog posts (14 documents) are not found by URL. A "last line has no final punctuation" rule hit too
     many verse texts on the proxy gold set, so I left it out.

## Medicine 8: C4, several news items joined into one document

1. **Disease:** C4, 14 documents, all from daily news blogs.
   - `209cdb0931854e56`: second item joined with no boundary, `साम्पत्तिकभारः न्यूनीक्रियते` at 977.
   - `875f86117f43fd90`: `कावेरी - तमिळनाटु` at 569.
   - `44866dbca538bc36`: titles fused to the previous item at 317 and 572.
2. **Medicine:** where one item's last danda runs straight into the next item's dateline (`…अकरोत्।चेन्नै >`),
   insert a paragraph break. This happens only in the middle of a line, not at a title.
   ```python
   def m_c4(t, url=""):
       def cut(m):
           line_start = t.rfind("\n", 0, m.start()) + 1
           return m.group(1) + ("\n\n" if m.start() - line_start >= 60 else "")
       return re.sub(f"([।!?])(?=[{DEVA}][{DEVA} ]{{1,40}}\\s?>)", cut, t)
   ```
3. **Action:** fix the text (separate the items; a later step can split them into documents).
4. **Harm test:** proxy gold: 1 changed, 0 dropped (0.9%). **Pass, at the limit.** The changed document
   (`1ece1474b414d6fe`) has a long title fused to its own dateline. The break is harmless there, but it is a
   change.
5. **Side effects:**
   - Reach is low (2 of 14). Most joined items in this pack sit on separate lines, with nothing in the text to show
     that a new story starts. Those need the blog's HTML post boundaries, which FineWeb-2 lost.

## Medicine 9: C5, link and keyword lists

1. **Disease:** C5, 7 documents.
   - `eb2b252468aea92c`: SEO keyword line `श्रीविष्णुपंजरस्तोत्र| … ShriVishnuPanjaraStotram| …` at 0.
   - `aa8e369c2d562c48`: SEO phrase `(Birthday wish to my wife Sanskrit)` repeated 10 times, first at 34.
   - `23d7ef42db7cc671`: list of `|👉…||Click Here|` links to other essays from 1341.
2. **Medicine:** remove lines that end in `Click Here` or are a bare URL.
   ```python
   LINK_LINE = re.compile(r"Click Here\s*\|?$|^https?://\S+$", re.I)

   def m_c5(t, url=""):
       return "\n".join(l for l in t.split("\n") if not LINK_LINE.search(l.strip()))
   ```
3. **Action:** fix the text (remove the lines).
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 2 of 7.
5. **Side effects:**
   - A bare URL that is the source of a quoted text is lost.
   - SEO keyword lines and word clouds have no fixed shape, so they are not found (5 of 7).

## Medicine 10: D2, D3 and H3, lines in another language or script

One medicine covers the three diseases: it removes whole lines that are not in Sanskrit.

1. **Disease:**
   - **D2 (romanised Sanskrit), 6 documents:**
     - `7bc67301a58f3aec`: `tena … paThyate` at 829.
     - `76282692bca966da`: romanised lines from 88.
     - `8f8f2c783674d31f`: romanised lines from 311.
   - **D3 (Hindi or English mixed in), 98 documents:**
     - `8044a4531f5c6b29`: Hindi line `tet-2014 अभ्यर्थियों के साथ…` at 335.
     - `3cbf9bd2ba360786`: Hindi sentence `दूसरी ओर दक्षिण कन्नड़ जिला…` at 1116.
     - `f322929becc2d910`: Hindi intro and outro, English lines from 517.
   - **H3 (translations), 9 documents:**
     - `8425414f14a1f498`: English translation `Sanskrit is the foundation to all…` at 357.
     - `f5661c3e611fef8b`: English translation after every verse, from 386.
     - `b7d0ec485aed0bd6`: each sentence in Hindi, English and Sanskrit, from 0.
2. **Medicine:** classify each line by script share and Hindi function words, then remove English, Hindi and
   romanised lines. Short lines (under 25 characters) and inline glosses in brackets inside Sanskrit sentences are
   kept, because they are natural code-mixing.
   - Hindi is recognised by words that do not occur in Sanskrit (`है`, `में`, `नहीं`, `के`, …) and by the oblique
     plural `-ों` in words of two or more syllables. Bija mantras like `क्रों` are not Hindi.

   ```python
   STRONG_HIN = set("है हैं था थे थी में और नहीं लिए गया गई हुआ होता होती करने किया करें ने को से का की के भी यह वह कि जो आप हम साथ वाले रहे रही".split())
   HIN_ANCHOR = set("है हैं था थे थी में और नहीं लिए गया गई हुआ होता होती करने किया करें ने साथ वाले रहे रही".split())

   def line_lang(line):
       letters = [c for c in line if c.isalpha()]
       if len(line.strip()) < 25 or len(letters) < 10:
           return "short"
       lat = sum(1 for c in letters if c.isascii() or 0xC0 <= ord(c) <= 0x24F or 0x1E00 <= ord(c) <= 0x1EFF)
       dev = sum(1 for c in letters if "\u0900" <= c <= "\u097F")
       if lat / len(letters) > 0.6:
           return "san_Latn" if re.search(r"[āīūṛṝḷṃḥṅñṭḍṇśṣ]", line) else "eng"
       if dev / len(letters) > 0.6:
           w = re.findall(f"[{DEVA}]+", line)
           obl = lambda x: x.endswith("ों") and len(re.findall(f"[{CONS}](?!\u094D)", x)) >= 2
           h = sum(1 for x in w if x in STRONG_HIN or obl(x))
           a = sum(1 for x in w if x in HIN_ANCHOR or obl(x))
           if a >= 1 and h >= 2 and h / max(1, len(w)) >= 0.15:
               return "hin"
       return "san"

   def m_lines(t, url=""):
       return "\n".join(l for l in t.split("\n") if line_lang(l) not in ("eng", "hin", "san_Latn"))

   def m_d1(t, url=""):            # companion rule: drop when under half of the text is Sanskrit (D1, 5 documents)
       lines = [l for l in t.split("\n") if line_lang(l) != "short"]
       n = sum(len(l) for l in lines) or 1
       return None if sum(len(l) for l in lines if line_lang(l) == "san") / n < 0.5 else t
   ```
3. **Action:** fix the text (remove the lines). Drop the document when less than half of it is Sanskrit.
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%) for `m_lines`, and 0 / 0 for `m_d1`. **Pass.**
   Reach: D2 6 of 6, D3 53 of 98, H3 8 of 9, D1 2 of 5.
5. **Side effects:**
   - English words and acronyms inside Sanskrit sentences (`(electronic waste)`, `UNESCO`, `BRC`) are kept on
     purpose. They are natural code-mixing; that is most of the D3 documents the medicine does not change.
   - IAST transliteration that is part of a learning page is removed even when the reader wanted it.
   - Marathi and Nepali lines are classed as Sanskrit, because they share the script and most function words differ
     only a little.
   - A Sanskrit line with many Hindi loanwords in a news report could be classed as Hindi. None was in the proxy
     gold set.

## Medicine 11: D4, machine-translated Sanskrit

1. **Disease:** D4, 56 documents. Each D4 row in `labels.csv` has the note "D4 judged by assistant, verify";
   a fluent reader should confirm these.
   - `19ed8d7b0056741b`: `गृह्णातु।` at 52, the Hindi filler `लीजिए` translated literally; `जारीकृते` at 849, Hindi
     `जारी` with a Sanskrit suffix.
   - `2d33ec2d9fc4e9db`: Hindi stem `दबावः` at 392, 4 markers.
   - `59a0682c9a80d27f`: wrong voice and gender, `केन्द्रसर्वकारेण स्थगितवती` at 90.
2. **Medicine:**
   - Drop every page from `sanskritvarta.in`. Its articles are machine translations of Hindi news; all 41 pages in
     this pack showed the calques.
   - Elsewhere, drop a document with three or more Hindi-only stems used inside Sanskrit inflection.

   ```python
   MT_SITES = {"sanskritvarta.in"}
   D4_STEMS = ["जारी", "पीएम", "सीएम", "बयान", "मुताबिक", "दौरान", "हालांकि", "जरिये", "वायरल", "साझा", "कार्यवाही", "विडियो",
               "शूटिंग्", "माङ्गं", "दबाव", "सुनवायी"]

   def m_d4(t, url=""):
       if host(url) in MT_SITES:
           return None
       hits = sum(len(re.findall(f"(?<![{DEVA}]){s}", t)) for s in D4_STEMS)
       return None if hits >= 3 else t
   ```
3. **Action:** drop the document.
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 42 of 56.
5. **Side effects:**
   - A human-written article on that site would also be dropped. A site-level rule is coarse; it is right for this
     sample and must be checked again on the full crawl.
   - Learner Sanskrit with grammar errors (for example `तत् त्वमं असि`) and machine translation from English (a
     software blog) have no Hindi stems, so they are not found.

## Medicine 12: F1, personal data

1. **Disease:** F1, 8 documents. Positions only, never the values.
   - `788a3d1d099f2017`: obfuscated email at offset 16883, twice.
   - `4aac5343e806c60e`: obfuscated email at offset 9985, twice.
   - `540c84255a18f83d`: obfuscated email at offset 16420, 3 times.

   The others are a phone number with a name, and two names with a postal address and PIN.
2. **Medicine:** mask emails (also the `name at gmail dot com` forms) and Indian mobile numbers.
   ```python
   PHONE = re.compile(r"(?<!\d)(?:\+?91[-\s]?)?[6-9]\d{4}[-\s]?\d{5}(?!\d)")
   EMAIL = re.compile(r"[A-Za-z0-9._%+-]+\s*(?:@|\(at\)|\[at\]| at )\s*[A-Za-z0-9-]+\s*(?:\.|\(dot\)|\[dot\]| dot )\s*[A-Za-z]{2,}")

   def m_f1(t, url=""):
       t = EMAIL.sub(lambda m: m.group() if "example." in m.group() else "<EMAIL>", t)
       return PHONE.sub("<PHONE>", t)
   ```
3. **Action:** fix the text (mask the values).
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 5 of 8.
5. **Side effects:**
   - The `x at y dot z` form can match English prose ("look at site dot com").
   - A ten-digit number that starts with 6–9 (a reference or ISBN fragment) is masked.
   - Names with postal addresses are not found by a regex; they need a named-entity model.
   - FineWeb's own `@example.org` placeholders are kept.

## Medicine 13: G1, words broken by extraction

1. **Disease:** G1, 11 documents.
   - `253e06e749a796be`: `लङ्क ागमनम्` at 290. A space sits before U+093E, 4 times.
   - `29e6b806cfadcdeb`: `पदिश्य ोिक्षयि` at 1251.
   - `1920901e618b8f0c`: `रुन्धे ु` at 5111, 4 times.
2. **Medicine:** no Devanagari word starts with a vowel sign, virama, chandrabindu, anusvara or visarga. Remove any
   space or line break in front of one.
   ```python
   def m_g1(t, url=""):
       return re.sub(f"(?<=[{DEVA}])[ \\t\u00A0\\n]+(?=[{MATRA}\u0901-\u0903\u094D])", "", t)
   ```
3. **Action:** fix the text.
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 6 of 11.
5. **Side effects:**
   - If the space was correct and the vowel sign is the stray character (an OCR error), joining makes a wrong word.
     The word was already wrong, so this does no new harm.
   - Not covered: PDF spaces inside words at a full consonant (`क बीरः`), and words split by print line wraps
     (`वि` + newline + `धाय`). Both look the same as real word boundaries.

## Medicine 14: G3, missing sections

1. **Disease:** G3, 10 documents.
   - `1323891568bac822`: the hymn starts at `॥ २ ॥`; verse 1 `भज गोविन्दं…` is missing.
   - `6d5604f350843975`: only the first half of every verse survives; 16 of 17 lines end in `।` and there is no `॥`
     anywhere.
   - `e2afa14616dded22`: starts mid-verse; the first half of verse 1 is missing.
2. **Medicine:** drop the document in either of two cases.
   - It is a hymn that starts at verse 2, with no verse 1 anywhere.
   - It is a verse text where every line ends in a single danda with no `॥` at all, and the lines are half-verse
     length.

   ```python
   VERSE_NO = re.compile(r"॥\s*([०-९\d]+)\s*(?:॥|$)", re.M)
   DIG = str.maketrans("०१२३४५६७८९", "0123456789")

   def m_g3(t, url=""):
       n = [int(x.translate(DIG)) for x in VERSE_NO.findall(t)]
       if len(n) >= 3 and n[0] == 2 and 1 not in n and VERSE_NO.search(t).start() < 600:
           return None                                   # verse 1 was cut
       lines = [l.strip() for l in t.split("\n") if len(l.strip()) > 15]
       half = sum(1 for l in lines if re.search(r"[^०-९\d\s]\s*।$", l))
       numbered = sum(1 for l in lines if re.search(r"[०-९\d]\s*।$", l))
       short = sorted(len(l) for l in lines)[len(lines) // 2] <= 50 if lines else False
       if len(lines) >= 15 and "॥" not in t and numbered == 0 and short and half / len(lines) >= 0.8:
           return None                                   # every verse lost its second half
       return t
   ```
3. **Action:** drop the document.
4. **Harm test:** proxy gold: 0 changed, 0 dropped (0.0%). **Pass.** Reach: 4 of 10.

   An earlier version, "drop when the verse numbers skip", dropped 3 good Mahabharata and Padma Purana chapters.
   Their numbering restarts in footnotes and in chapter headings, so I removed that rule.
5. **Side effects:**
   - A stotra whose first verse is unnumbered and whose second verse is numbered `॥ २ ॥` is dropped. The `(?:॥|$)`
     form catches `॥ १` with no closing mark (doc `a5537c5833c05ea2`, which kept its verse 1).
   - A prose text written with single dandas in short lines would match the half-verse rule; the 50-character
     median keeps out prose like the Sanskrit Bible.
   - Missing sections that leave no numbering trace (an announced verse that never comes, missing endnotes) are not
     found.
