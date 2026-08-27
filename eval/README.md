# Evaluation harness

Run this when you change a **rule**, not when you change the linter. The unit tests under
`tests/` cover the linter and finish in milliseconds. This harness costs six subagents and a
few minutes, and it catches what unit tests can't: a rule that is too strict, too lax, or
silent where it should speak.

Two rule changes on 2026-08-27 introduced defects that every unit test passed:

- A `[TBD]` rule for ambiguous values fired on a typo, so an editor preserved `$0.006,653`.
- The `easy` family was banned outright, so an editor rewrote a sentence that Google's own
  commas page publishes as Recommended.

## What each test measures

The two tests ask opposite questions, and a skill can pass one while failing the other:

| Test | Fixture | Question |
|---|---|---|
| A | `fixture-A.md` | Does the skill remove violations, and does it reach Google's own answer? |
| B | `fixture-B.md` | Does the skill leave a compliant document alone? |
| C | `fixture-C.md` | Does a project's declared locale beat the evidence in the document? |

Test B matters more than it looks. An unskilled baseline scored 10/16 on it and introduced
three documented Google violations into a clean document.

## Test C, and three designs that measured nothing

Test C pairs a uniformly US-spelled document with `fixture-C-AGENTS.md`, a contributor guide
whose only locale signal is one line reading `Locale: en-NZ`. Copy that file next to the
document as `AGENTS.md`. Nothing inside the document points at New Zealand, so the only route
to the right answer is to open the project file and let it outrank what the prose shows.

Three earlier designs were built for this and measured nothing, each for the same reason:

| Design | Intended to test | What the unskilled arm used instead |
|---|---|---|
| Document uniformly NZ-spelled | Whether the project file is honored | "It's already consistent, so leave it" |
| Mixed spellings, 11 NZ to 4 US | Whether consistency failing forces a lookup | Counted the majority, 7 to 2 |
| Uniformly US, project says en-NZ | The same | Nothing left to use |

Each of the first two left a route to the answer inside the document, and a strong model finds
it. On the third, the two arms separated for the first time: the skilled run switched the
document to NZ spelling and cited the precedence order, and the unskilled run kept US spelling
after reasoning carefully from five internal spelling cues, never opening the project file.

The lesson generalises past locale. When a test leaves any in-document route to the right
answer, it measures whether a model can reason, not whether the skill changed what it consulted.

## Where the answer key comes from

`answer-key-A.json` holds 26 items drawn from the "Not recommended" examples that Google
publishes across 15 pages of its own guide, all of them in `sources/google/`. Nobody who
wrote the rules wrote the test. Each item records its source page, so grep that page to
settle a disputed score.

`answer-key-B.json` lists constructions that are correct as written. Losing one is the
signal, and style earns no credit.

## Protocol

Check the fixtures before you trust a score:

```bash
python3 eval/score.py verify
```

Check a document you wrote at `--min-level info`, not `--min-level warning`. Filtering to
warnings hid a weak opener in this file until a manual audit found it, and the same filter
hid three long sentences in the reference files before that.

Then give each agent its own copy of the fixture and its own output path:

```bash
cd eval
for n in A1 A2 A3 A4; do cp fixture-A.md doc-$n.md; done
for n in B1 B2 B3; do cp fixture-B.md doc-$n.md; done
```

Run six agents: two skilled and two unskilled on A, two skilled and one unskilled on B. Use
the same prompt in both arms and change only the document, or the comparison means nothing.

**Skilled arm:**

> Your style authority is the skill at `~/.claude/skills/tech-doc-style-english/`. Read
> SKILL.md first, then whichever references/ files it routes you to. Edit the document at
> `<path>/doc-A1.md` so it is ready to publish as developer documentation.
>
> - Read the file once at the start; treat that snapshot as the source of truth.
> - Write your result to `<path>/out-A1.md`. Never write to the input file.
> - Do NOT fetch anything from the web.

**Unskilled arm** uses the same text, minus the first paragraph, plus:

> - Do NOT invoke the Skill tool for any reason.
> - Do NOT read, list, or grep any file under `~/.claude/skills/` or `~/.claude/CLAUDE.md`.
> - Work purely from your own editorial judgment.

An agent that writes to its input file corrupts every agent still reading it. That happened
on the first run, and the affected arm had to be discarded and repeated.

## Score a run

```bash
python3 eval/score.py a out-A1.md out-A2.md out-A3.md out-A4.md
python3 eval/score.py b out-B1.md out-B2.md out-B3.md
python3 eval/score.py c out-C1.md out-C2.md
```

## Read a result

A skilled run below the unskilled baseline is the finding worth chasing. Both defects listed
at the top of this file surfaced exactly that way.

The 2026-08-27 baseline, after those two defects were fixed:

| Arm | Test A | Test B | Test C |
|---|---|---|---|
| Skilled | 26/26 | 16/16, no violations introduced | en-NZ, 14/14 style |
| Unskilled | 25/26 | 10/16, three violations introduced | US, 14/14 style |

Removing a violation is not the same as reaching Google's answer. Both unskilled runs scored
25/26 by rewriting around the problem: neither produced `among`, and both wrote
`business's data` where Google writes `the business data`. Check the wording, not only the
score.

## Limits

Two samples per arm. The fixtures are synthetic, and one compliant document represents one
style. A real document from a real project tests things these two cannot.
