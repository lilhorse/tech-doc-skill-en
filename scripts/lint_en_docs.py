#!/usr/bin/env python3
"""Flag candidate style problems in English technical docs.

Rules follow the Google developer documentation style guide, with a few
Microsoft entries where Google is silent. Findings are candidates, not
verdicts: several rules are deliberately heuristic and need human judgment.

Usage:
    lint_en_docs.py FILE [FILE ...]
    lint_en_docs.py -            # read stdin
    lint_en_docs.py --min-level warning FILE
    lint_en_docs.py --json FILE
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict

LEVELS = {"info": 0, "warning": 1}

MASK_PATTERNS = [
    re.compile(r"\A---\n.*?^---\n", re.DOTALL | re.MULTILINE),
    re.compile(r"^( {0,3}```|~~~).*?^\1.*?$", re.DOTALL | re.MULTILINE),
    re.compile(r"`[^`\n]+`"),
    re.compile(r"<!--.*?-->", re.DOTALL),
    re.compile(r"(?<=\]\()[^)\s]+(?:\s+\"[^\"]*\")?(?=\))"),
    re.compile(r"<https?://[^>\s]+>"),
    re.compile(r"(?<![\w/\[])https?://\S+"),
]

CI = re.IGNORECASE

# (rule, level, pattern, message, flags, raw)
# raw=True runs the rule against unmasked text.
RULES = [
    ("banned-word", "warning", r"\babort(s|ed|ing)?\b", "Violent metaphor. Use stop, exit, cancel, or end.", CI, False),
    ("banned-word", "warning", r"\bkill(s|ed|ing)?\b", "Violent metaphor. Use stop, exit, cancel, or end.", CI, False),
    ("banned-word", "warning", r"\b(hangs?|hung)\b", "Use stop responding or not responding.", CI, False),
    ("banned-word", "warning", r"\bblack ?list(s|ed|ing)?\b", "Use denylist or blocklist.", CI, False),
    ("banned-word", "warning", r"\bwhite ?list(s|ed|ing)?\b", "Use allowlist.", CI, False),
    ("banned-word", "warning", r"\bmaster[/ -]slave\b", "Use primary/replica, main, or controller.", CI, False),
    ("banned-word", "warning", r"\bsanity[- ]check\b", "Use quick check, confidence check, or preliminary check.", CI, False),
    ("banned-word", "warning", r"\bdummy\b", "Use placeholder.", CI, False),
    ("banned-word", "warning", r"\bgrandfathered\b", "Use legacy or exempt.", CI, False),
    ("banned-word", "warning", r"\bman[- ]hours\b", "Use person hours.", CI, False),
    ("banned-word", "warning", r"\bguys\b", "Use everyone, folks, or all.", CI, False),
    ("banned-word", "warning", r"\bmankind\b", "Use humanity or people.", CI, False),
    ("banned-word", "warning", r"\bcrippl(e|es|ed|ing)\b", "Ableist. Use slows down or degrades.", CI, False),
    ("banned-word", "warning", r"\b(insane|crazy)\b", "Ableist. Use complicated, baffling, or unexpected.", CI, False),
    ("banned-word", "warning", r"\b(e\.g\.|i\.e\.)", "Use for example or that is.", CI, False),
    ("banned-word", "warning", r"\band/or\b", "Use and, or or, or rewrite.", CI, False),
    ("wordy", "info", r"\ballows you to\b", "Use lets you. (Not in either guide; standard practice.)", CI, False),
    ("banned-word", "warning", r"\bleverag(e|es|ed|ing)\b", "Jargon. Use use.", CI, False),
    ("banned-word", "warning", r"\bin order to\b", "Use to.", CI, False),
    ("banned-word", "warning", r"\bvia\b", "Use through, by, or using.", CI, False),
    ("banned-word", "warning", r"\bhit\s+(?!rate|count|ratio|percentage)", "Use click, press, or type.", CI, False),
    ("banned-word", "warning", r"\b(login|setup|backup)\s+(to|the|your)\b",
     "Verb form is two words: log in, set up, back up.", CI, False),
    ("banned-word", "warning", r"\bdrop-?downs?\b", "Use list or menu.", CI, False),
    ("filler", "warning", r"\b(please note|note that|at this time|it should be noted)\b", "Filler. Delete.", CI, False),
    ("hypothetical", "warning", r"\bwould (then )?\w+", "Cut would/could hypotheticals. State cause and effect.", CI, False),

    # Case-sensitive: uppercase forms are usually product names or acronyms.
    ("condescending", "warning", r"\b([Ee]asy|[Ee]asily|[Ss]imply|simple)\b",
     "Condescending. Google: what is simple for you might not be simple for others.", 0, False),
    ("condescending", "info", r"\b([Oo]bvious(ly)?|[Tt]rivial(ly)?|of course)\b",
     "Condescending. (Not in either guide; same principle as easy and simple.)", 0, False),
    ("first-person", "info", r"(?<![\w'])([Ww]e|[Oo]ur|us)(?![\w'])",
     "Use second person (you) for the reader. The organizational we is allowed.", 0, False),

    ("please", "info", r"\bplease\b",
     "Omit in ordinary steps. Both guides keep it when the request inconveniences the reader "
     "or the product is at fault.", CI, False),
    ("utilize", "info", r"\butiliz(e|es|ed|ing)\b",
     "Use use. (utilization is fine for a quantity of a resource.)", CI, False),
    ("the-user", "info", r"\bthe user\b(?!\s+(agent|interface|experience|account|data|name|id|ID|pool|group))",
     "Address your reader as you. the user is for the end user of the software your reader builds.", CI, False),
    ("weak-phrase", "info", r"\bthere (is|are|was|were)\b", "Weak opener. Start with the subject.", CI, False),
    ("hedge", "info", r"\b(just)\b", "Often filler or condescending. Check whether it carries meaning.", CI, False),
    ("future-tense", "info", r"\bwill\b", "Use present tense unless the event genuinely happens later.", CI, False),

    ("en-dash", "warning", r"–", "Google: don't use en dashes. Use a hyphen or 'to'.", 0, False),
    ("spaced-em-dash", "warning", r"[  ]—|—[  ]", "No spaces around an em dash.", 0, False),
    ("double-hyphen", "warning", r"(?<=\w)--(?=\w)|\s--\s", "Use a real em dash, not two hyphens.", 0, False),
    ("link-text", "warning",
     r"\[\s*(click here|here|this link|this document|this article|read more|more|link)\s*\]\(",
     "Use descriptive link text.", CI, False),
    ("bare-url-link", "info", r"\[\s*https?://", "Use the page title or a description as link text.", CI, False),
    ("numeric-date", "warning", r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
     "Ambiguous date. Use ISO 8601 or spell out the month.", 0, False),
    ("ordinal-numeral", "warning", r"\b\d+(st|nd|rd|th)\b", "Spell out ordinals: first, fifth, twenty-first.", CI, False),
    ("percent-word", "warning", r"\b\d+\s+percent\b", "Google: use a numeral plus %, no space (40%).", CI, False),
    ("decimal-comma", "warning", r"\b\d+\.\d+,\d", "No punctuation to the right of a decimal point: 0.006653.", 0, False),
    ("dimensions", "warning", r"\b\d{2,5}\s*×\s*\d{2,5}\b|\b\d{2,5}\s+x\s*\d{2,5}\b",
     "Google: dimensions take a lowercase x and no spaces (1280x1024).", 0, False),
    ("unit-space", "warning", r"\b\d+(?:\.\d+)?(GB|MB|KB|TB|Mbps|Gbps|ms|kg|mm|cm|km)\b",
     "Put a space between the numeral and the unit: 64 GB.", 0, False),
    ("am-pm", "warning", r"\b\d(?::\d{2})?\s?[ap]\.?m\.?\b", "Use uppercase AM or PM: 3 PM.", 0, False),
    ("am-pm", "warning", r"\b\d(?::\d{2})?(AM|PM)\b", "Put a space before AM or PM: 3 PM.", 0, False),
    ("passive-voice", "warning", r"\b(is|are|was|were)\s+\w+ed\s+by\b", "Passive voice. Name the actor.", CI, False),
    ("directional", "warning",
     r"\b(?:tables?|lists?|examples?|sections?|figures?|images?|diagrams?|code|snippets?|steps?"
     r"|procedures?|paragraphs?|director(?:y|ies)|files?|columns?|rows?)\s+(?:above|below)\b"
     r"|\b(?:see|shown|described|listed|noted)\s+(?:above|below)\b"
     r"|\b(?:left|right)-hand side\b",
     "Don't orient the reader with direction; it fails for screen readers and inverts in RTL. "
     "Name the thing, or write 'the following'.", CI, False),
    ("curly-quotes", "warning", r"[\u201c\u201d\u2018\u2019]",
     "Use straight quotation marks and apostrophes.", 0, False),
    ("double-space", "info", r"(?<=[.?:])  +", "Use one space after a period, question mark, or colon.", 0, True),
]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
LIST_MARKER_RE = re.compile(r"^[\s>]*(?:[-*+]|\d+\.)?\s*")
LONG_SENTENCE_WORDS = 32
TITLE_CASE_MIN_CANDIDATES = 3
SMALL_WORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into", "nor",
    "of", "off", "on", "onto", "or", "over", "per", "so", "the", "to", "up", "via", "with", "yet",
}


@dataclass
class Finding:
    path: str
    line: int
    column: int
    level: str
    rule: str
    message: str
    excerpt: str


def mask(text: str) -> str:
    """Blank out spans that style rules must not read, keeping offsets intact."""
    masked = text
    for pattern in MASK_PATTERNS:
        masked = pattern.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), masked)
    return masked


def _position(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    line_start = text.rfind("\n", 0, offset) + 1
    return line, offset - line_start + 1


def _excerpt(text: str, offset: int, width: int = 60) -> str:
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    if line_end == -1:
        line_end = len(text)
    return text[line_start:line_end].strip()[:width]


def _looks_title_case(heading: str) -> bool:
    """Heuristic. The threshold keeps proper-noun headings such as
    'Deploy to Google Cloud' from tripping the rule."""
    words = re.findall(r"[A-Za-z][\w'-]*", heading)
    if len(words) < 3:
        return False
    candidates = [w for w in words[1:] if w.lower() not in SMALL_WORDS]
    if len(candidates) < TITLE_CASE_MIN_CANDIDATES:
        return False
    return all(w[0].isupper() for w in candidates)


def lint_text(text: str, path: str = "<stdin>") -> list[Finding]:
    masked = mask(text)
    findings: list[Finding] = []

    for rule, level, pattern, message, flags, raw in RULES:
        for match in re.finditer(pattern, text if raw else masked, flags):
            line, column = _position(text, match.start())
            findings.append(Finding(path, line, column, level, rule, message,
                                    _excerpt(text, match.start())))

    for match in HEADING_RE.finditer(masked):
        heading = match.group(2).strip()
        if not heading:
            continue
        line, column = _position(text, match.start(2))
        if heading.endswith((".", ":")):
            findings.append(Finding(path, line, column, "warning", "heading-punctuation",
                                    "No period or colon at the end of a heading.", heading[:60]))
        if _looks_title_case(heading):
            findings.append(Finding(path, line, column, "info", "heading-case",
                                    "Use sentence case for headings.", heading[:60]))

    lines = masked.split("\n")
    offset, starts = 0, []
    for line in lines:
        starts.append(offset)
        offset += len(line) + 1
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        if i + 1 >= len(lines) or not TABLE_SEP_RE.match(lines[i + 1]):
            continue
        intro = next((lines[j].strip() for j in range(i - 1, max(-1, i - 4), -1) if lines[j].strip()), "")
        if not intro or intro.startswith(("#", "|", ">")) or not intro.endswith((".", ":")):
            line_no, column = _position(text, starts[i])
            findings.append(Finding(path, line_no, column, "warning", "table-intro",
                                    "Introduce a table with a complete sentence.", line.strip()[:60]))

    for match in re.finditer(r"^(?![#>|]).*\S.*$", masked, re.MULTILINE):
        body = LIST_MARKER_RE.sub("", match.group(0))
        for sentence in SENTENCE_SPLIT_RE.split(body):
            words = sentence.split()
            if len(words) > LONG_SENTENCE_WORDS:
                line, column = _position(text, match.start())
                findings.append(Finding(path, line, column, "info", "long-sentence",
                                        f"{len(words)} words. Keep sentences under "
                                        f"{LONG_SENTENCE_WORDS} words where you can.",
                                        sentence.strip()[:60]))

    findings.sort(key=lambda f: (f.line, f.column, f.rule))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", help="files to check, or - for stdin")
    parser.add_argument("--min-level", choices=sorted(LEVELS, key=LEVELS.get), default="info")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--quiet", action="store_true", help="exit status only")
    args = parser.parse_args(argv)

    threshold = LEVELS[args.min_level]
    findings: list[Finding] = []
    for path in args.paths:
        if path == "-":
            findings += lint_text(sys.stdin.read())
            continue
        try:
            with open(path, encoding="utf-8") as handle:
                findings += lint_text(handle.read(), path)
        except OSError as error:
            print(f"{path}: {error}", file=sys.stderr)
            return 2

    findings = [f for f in findings if LEVELS[f.level] >= threshold]

    if args.as_json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    elif not args.quiet:
        for f in findings:
            print(f"{f.path}:{f.line}:{f.column}: {f.level}: [{f.rule}] {f.message}  |  {f.excerpt}")
        print(f"\n{len(findings)} finding(s) at level {args.min_level} or above.", file=sys.stderr)

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
