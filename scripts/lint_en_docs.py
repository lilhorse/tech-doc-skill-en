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

LEVELS = {"info": 0, "warning": 1, "error": 2}

MASK_PATTERNS = [
    re.compile(r"^---\n.*?^---\n", re.DOTALL | re.MULTILINE),
    re.compile(r"^( {0,3}```|~~~).*?^\1.*?$", re.DOTALL | re.MULTILINE),
    re.compile(r"`[^`\n]+`"),
    re.compile(r"<!--.*?-->", re.DOTALL),
    re.compile(r"(?<=\]\()[^)\s]+(?:\s+\"[^\"]*\")?(?=\))"),
    re.compile(r"<https?://[^>\s]+>"),
    re.compile(r"(?<![\w/\[])https?://\S+"),
    re.compile(r"^ {4,}\S.*$", re.MULTILINE),
]

WORD_RULES = [
    ("banned-word", "warning", r"\babort(s|ed|ing)?\b", "Violent metaphor. Use stop, exit, cancel, or end."),
    ("banned-word", "warning", r"\bkill(s|ed|ing)?\b", "Violent metaphor. Use stop, exit, cancel, or end."),
    ("banned-word", "warning", r"\bterminat(e|es|ed|ing)\b", "Use stop, exit, cancel, or end."),
    ("banned-word", "warning", r"\bexecut(e|es|ed|ing)\b", "Prefer run."),
    ("banned-word", "warning", r"\bhangs?\b", "Use stops responding or doesn't respond."),
    ("banned-word", "warning", r"\bblack ?list(s|ed|ing)?\b", "Use denylist or blocklist."),
    ("banned-word", "warning", r"\bwhite ?list(s|ed|ing)?\b", "Use allowlist."),
    ("banned-word", "warning", r"\bmaster[/ -]slave\b", "Use primary/replica, main, or controller."),
    ("banned-word", "warning", r"\bsanity[- ]check\b", "Use final check or validation."),
    ("banned-word", "warning", r"\bdummy\b", "Use placeholder."),
    ("banned-word", "warning", r"\bgrandfathered\b", "Use legacy or exempt."),
    ("banned-word", "warning", r"\bman[- ]hours\b", "Use person hours."),
    ("banned-word", "warning", r"\bguys\b", "Use everyone, folks, or all."),
    ("banned-word", "warning", r"\bmankind\b", "Use humanity or people."),
    ("banned-word", "warning", r"\bcrippl(e|es|ed|ing)\b", "Ableist. Use slows down or degrades."),
    ("banned-word", "warning", r"\b(insane|crazy)\b", "Ableist. Use baffling or unexpected."),
    ("banned-word", "warning", r"\bplease\b", "Omit please in instructions."),
    ("banned-word", "warning", r"\b(e\.g\.|i\.e\.)", "Use for example or that is."),
    ("banned-word", "warning", r"\band/or\b", "Use and, or or, or rewrite."),
    ("banned-word", "warning", r"\ballows you to\b", "Use lets you."),
    ("banned-word", "warning", r"\butiliz(e|es|ed|ing|ation)\b", "Use use."),
    ("banned-word", "warning", r"\bleverag(e|es|ed|ing)\b", "Jargon. Use use."),
    ("banned-word", "warning", r"\bin order to\b", "Use to."),
    ("banned-word", "warning", r"\bvia\b", "Use through, by, or using."),
    ("banned-word", "warning", r"\bhit\s+the\b", "Use click, press, or tap."),
    ("banned-word", "warning", r"\bthe user\b", "Address the reader as you."),
    ("banned-word", "warning", r"\b(login|setup|backup)\s+(to|the|your)\b", "Verb form is two words: log in, set up, back up."),
    ("banned-word", "warning", r"\bdrop-?downs?\b", "Use list or menu."),
    ("condescending", "warning", r"\b(easy|easily|simple|simply|obvious(ly)?|trivial(ly)?|of course)\b",
     "Condescending. Delete, or state the actual steps."),
    ("filler", "warning", r"\b(please note|note that|at this time|it should be noted)\b", "Filler. Delete."),
    ("hedge", "info", r"\b(just)\b", "Often filler or condescending. Check whether it carries meaning."),
    ("weak-phrase", "info", r"\bthere (is|are|was|were)\b", "Weak opener. Start with the subject."),
    ("first-person", "info", r"(?<![\w'])(we|our|us)(?![\w'])", "Use second person (you) for the reader."),
    ("future-tense", "info", r"\bwill\b", "Use present tense unless the event genuinely happens later."),
    ("hypothetical", "warning", r"\bwould (then )?\w+", "Cut would/could hypotheticals. State cause and effect."),
]

LINE_RULES = [
    ("en-dash", "warning", r"–", "Google: don't use en dashes. Use a hyphen or 'to'."),
    ("spaced-em-dash", "warning", r"[  ]—|—[  ]", "No spaces around an em dash."),
    ("double-hyphen", "warning", r"(?<!-)--(?!-)", "Use a real em dash, not two hyphens."),
    ("link-text", "warning", r"\[\s*(click here|here|this link|this document|this article|read more|more|link)\s*\]\(",
     "Use descriptive link text."),
    ("bare-url-link", "info", r"\[\s*https?://", "Use the page title or a description as link text."),
    ("numeric-date", "warning", r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "Ambiguous date. Use ISO 8601 or spell out the month."),
    ("ordinal-numeral", "warning", r"\b\d+(st|nd|rd|th)\b", "Spell out ordinals: first, fifth, twenty-first."),
    ("percent-word", "warning", r"\b\d+\s+percent\b", "Google: use a numeral plus %, no space (40%)."),
    ("am-pm", "warning", r"\b\d(?::\d{2})?\s?(am|pm|a\.m\.|p\.m\.)\b", "Use uppercase AM or PM with a space: 3 PM."),
    ("passive-voice", "warning", r"\b(is|are|was|were)\s+\w+ed\s+by\b", "Passive voice. Name the actor."),
    ("double-space", "info", r"(?<=[.?:])  +", "Use one space after a period, question mark, or colon."),
    ("serial-comma", "info", r"\b\w+,\s+(?:\w+\s+){0,2}\w+\s+(?:and|or)\s+\w+",
     "Check for a missing serial comma. Heuristic: verify before acting."),
]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
LONG_SENTENCE_WORDS = 32
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
    words = re.findall(r"[A-Za-z][\w'-]*", heading)
    if len(words) < 3:
        return False
    candidates = [w for w in words[1:] if w.lower() not in SMALL_WORDS]
    if len(candidates) < 2:
        return False
    capped = [w for w in candidates if w[0].isupper()]
    return len(capped) == len(candidates)


def lint_text(text: str, path: str = "<stdin>") -> list[Finding]:
    masked = mask(text)
    findings: list[Finding] = []

    for rule, level, pattern, message in WORD_RULES + LINE_RULES:
        for match in re.finditer(pattern, masked, re.IGNORECASE):
            line, column = _position(text, match.start())
            findings.append(Finding(path, line, column, level, rule, message,
                                    _excerpt(text, match.start())))

    for match in HEADING_RE.finditer(masked):
        heading = match.group(2).strip()
        if not heading:
            continue
        offset = match.start(2)
        line, column = _position(text, offset)
        if heading.endswith((".", ":")):
            findings.append(Finding(path, line, column, "warning", "heading-punctuation",
                                    "No period or colon at the end of a heading.", heading[:60]))
        if _looks_title_case(heading):
            findings.append(Finding(path, line, column, "info", "heading-case",
                                    "Use sentence case for headings.", heading[:60]))

    for match in re.finditer(r"^(?![#>|\-*\d ]).+$", masked, re.MULTILINE):
        for sentence in SENTENCE_SPLIT_RE.split(match.group(0)):
            words = sentence.split()
            if len(words) > LONG_SENTENCE_WORDS:
                offset = match.start() + match.group(0).find(sentence)
                line, column = _position(text, max(offset, match.start()))
                findings.append(Finding(path, line, column, "info", "long-sentence",
                                        f"{len(words)} words. Shorter sentences translate better.",
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
