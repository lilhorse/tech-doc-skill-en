---
name: tech-doc-style-english
description: Use when writing, rewriting, editing, proofreading, or reviewing English technical content—developer docs, API reference, READMEs, release notes, how-to guides, runbooks, troubleshooting, error messages, UI text, or Markdown docs—and when a draft reads like marketing copy, is wordy or inconsistent, or was translated into English. Applies Google developer documentation style as the primary authority and the Microsoft Writing Style Guide where Google is silent.
---

# English technical documentation and product copy style

## Style authority

1. **Google developer documentation style guide** (https://developers.google.com/style) is the primary authority.
2. **Microsoft Writing Style Guide** (https://learn.microsoft.com/style-guide) applies only where Google is silent.
3. **When the two conflict, follow Google.** See [Conflicts between Google and Microsoft](#conflicts-between-google-and-microsoft).
4. Target-project conventions override both. See [Project overrides](#project-overrides).

Don't attribute a Microsoft rule to Google. When a visible choice rests on Microsoft because Google is silent, say so in your review notes.

## Checking a rule

`sources/` holds a plain-text snapshot of both guides, fetched 2026-08-27. Every rule here was
checked against it. When you're about to rely on a rule, or you disagree with one, grep the
snapshot instead of recalling the guide:

```
grep -ri "serial comma" ~/.claude/skills/tech-doc-style-english/sources/
```

The snapshot is a convenience, not the authority. See `sources/README.md`.

## Scope

Use this skill for English technical content:

- Landing pages, overviews, concept guides, release notes, and changelogs
- API reference, parameter tables, error codes, and FAQs
- How-to guides, tutorials, runbooks, troubleshooting, and security notes
- UI text: buttons, navigation, empty states, status, and error messages

Don't rewrite code literals, JSON keys, URLs, API paths, database field names, commands, configuration keys, or other machine-readable identifiers.

## Rule priority

When rules collide, resolve in this order:

1. Preserve facts, logic, limits, safety information, and legal meaning.
2. Follow explicit user instructions and target-project conventions.
3. Keep technical terms and machine-readable content exact.
4. Improve structure, meaning, tone, and scannability.
5. Fix punctuation, capitalization, and spacing last.

Never trade a higher item for a lower one—not for a shorter sentence, not for a more confident tone, not for a tidier format.

## Factual fidelity

- Don't add dates, numbers, limits, SLAs, capabilities, conditions, causes, or conclusions that the source doesn't supply.
- Don't drop prerequisites, scope, exceptions, risks, safety warnings, compatibility notes, or failure handling.
- Don't turn hedged statements (*may*, *plans to*, *typically*) into certainties.
- When information is missing, keep the original meaning or mark it `[TBD]`. Don't fill the gap yourself.
- When a source value is itself ambiguous (`04/06/2026` is either April 6 or June 4), keep the original string verbatim and mark it `[TBD]`. Normalizing it to one reading is filling the gap yourself.
- When editing quotations, regulations, contracts, verbatim error strings, or user-supplied fixed copy, preserve the original and list suggestions separately.

Examples:

- `The job will be terminated` -> `The job stops`
- `Handle this ASAP` -> `Handle this within the agreed time limit [TBD: state the limit]`
- Don't invent `within 30 minutes`.

## Pick the task mode first

### Write

- Establish audience, content type, sources of fact, publishing surface, and length before drafting.
- When a missing fact would change the conclusion, flag the gap and continue with what can be confirmed.

### Rewrite

- Preserve facts, logical relationships, information hierarchy, limits, and necessary exceptions.
- Deliver a complete rewrite by default. Call out significant meaning changes and open questions separately.

### Proofread

- Fix only what's in scope: typos, punctuation, spacing, capitalization, and term consistency.
- Don't change structure, tone, or factual phrasing unless asked.

### Review

- List problems first, then recommendations. Rank by impact and quote the specific source text.
- Don't edit files without authorization.

## Core rules

### Voice and tone

- Use second person (*you*). Avoid *we* in instructions, and don't call the reader *the user*.
- Use active voice and name who performs the action.
- Use present tense. Reserve *will* for genuinely later or asynchronous events. Cut *would*, *should*, and *could* hypotheticals.
- Be conversational but professional: no exclamation marks, humor, idioms, pop-culture references, or internet slang.
- Delete *easy*, *simple*, *simply*, *just*, *obvious*, and *of course*. They tell readers how to feel about a task that may not be going well for them.
- Omit *please* from ordinary steps. Both guides keep it where the request genuinely inconveniences the reader or the product is at fault.
- Put conditions before instructions: "To view the document, click **View**", not "Click **View** to view the document".
- Don't pre-announce unreleased features.

### Structure and sentences

- Front-load. State what the thing is, who it's for, what to do, and where to go next.
- One idea per paragraph. One clear main clause per sentence; don't stack conditions, actions, and exceptions.
- Keep sentences short—the primary lever for both scanning and translation. Treat 32 words as the point where a sentence needs a second look.
- Keep *that* in relative clauses and *then* in if-then constructions: "rules that you defined", "If the key isn't found, then the default is returned".
- Use at most two noun modifiers in a row. Repeat a word when repeating clarifies.
- Replace an ambiguous *it*, *this*, or *these* with the actual noun.
- Keep list items parallel in structure, length, and information density.
- Expand an abbreviation on first use, then use it consistently.
- Use one preferred term per concept. Don't vary wording for variety.

### Mechanics

- Sentence case for page titles and section headings.
- Standard American spelling and punctuation. Serial comma.
- Code font for code-related text. Bold for UI element names.
- Descriptive link text. Never *click here*, *this link*, or a bare URL.
- Unambiguous dates. Alt text on every image.

Details: [Mechanics and formatting](references/mechanics-and-formatting.md).

## Conflicts between Google and Microsoft

Follow the Google column. This table lists the differences that actually change output.

| Topic | Follow Google | Microsoft says (don't apply here) |
|---|---|---|
| En dashes | Don't use. Use a hyphen or *to*: `2012-2016`, `from 9 to 17` | *from X through Y* in prose; en dash for page ranges or tight space: `2016–2020` |
| Percentages | Numeral plus `%`, no space: `40%` | Numeral plus the word: `50 percent` |
| Dimensions | No spaces, lowercase x: `192x192` | Multiplication sign with spaces: `1280 × 1024` |
| *master/slave* | `primary/replica`, `main`, `controller` | `primary/subordinate` |
| Numeric-only dates | ISO 8601: `2026-04-15` | Spell out the month; numeric form only in locale-aware UI |
| Register | Conversational but professional; no ad voice | "Write like you speak"; ad-style brevity ("Ready to buy? Contact us.") |

Both guides agree on these, and drafts get them wrong often enough to check: sentence case headings, serial comma, no spaces around em dashes, spell out ordinals (`first`, not `1st`), and spell out zero through nine while using numerals for 10 and above. They agree on *please* too: omit it from ordinary steps, and keep it where the request genuinely inconveniences the reader or the product is at fault.

Microsoft is the right fallback where Google says little: consumer-facing UI and marketing copy, Windows and desktop terminology, and A-Z term entries Google's word list doesn't carry. Google is not silent on inclusive language or global audiences, so don't reach for Microsoft there.

"Landing pages" in Scope means developer landing pages, and those follow Google. A consumer marketing page falls outside this skill; say so rather than quietly switching register.

## By content type

### Overview and landing pages

The first paragraph answers:

- What this covers
- Who it's for
- Where to start

Don't repeat the same sentence in the title, the intro, and the call to action.

### Procedures, tutorials, and runbooks

Read and apply [Procedures and API reference](references/procedures-and-api.md). Don't apply its step-level formulas mechanically to conceptual or narrative content.

### API reference

- Protect request methods, paths, fields, and values in code font.
- Give each parameter one meaning per row, with type, unit, default, limits, and whether it's required.
- State prerequisites, the success result, the failure result, and how to recover.

Details: [Procedures and API reference](references/procedures-and-api.md).

### Release notes and changelogs

- Group entries by change type: new, changed, deprecated, removed, fixed, security.
- Lead each entry with what changed for the reader, not the internal component that changed.
- Give the version and the date in the standard date format.
- State the action a reader has to take, and link to the migration path.
- Don't announce unreleased work.

### UI text and error messages

- A button states the action and its object. It doesn't repeat the page title.
- An error states what happened, what it affects, and how to recover.
- A destructive action states the object, the consequence, and whether it can be undone.
- Empty states distinguish "no data", "not created yet", "no permission", and "failed to load".

## Project overrides

Check the target project's own `CLAUDE.md`, `AGENTS.md`, glossary, brand guide, existing docs, and any instructions you were given. Don't treat this skill's examples as a target project's conventions.

To establish conventions for a project, adapt [Project overrides](references/project-overrides-example.md) and put the resulting file in that project.

## Editing workflow

1. Confirm task mode, content type, audience, and project conventions.
2. Mark facts, numbers, limits, quotations, and machine-readable content as untouchable.
3. Fix meaning errors, ambiguity, omissions, and inconsistencies.
4. Reorder information, paragraphs, headings, and lists.
5. Fix voice, tense, terminology, punctuation, capitalization, and spacing.
6. Re-check against the source: facts, conditions, scope of negation, causation, and degree of certainty.
7. Run the linter and judge each finding. It flags candidates, not verdicts.

   ```
   python3 ~/.claude/skills/tech-doc-style-english/scripts/lint_en_docs.py --min-level warning FILE
   ```

   It skips code fences, code spans, front matter, and link targets. It can't tell a term being used
   from one being mentioned, so a document that has to *name* a banned word reports findings. Ignore
   those and keep the correct formatting; a word used as a word takes italics.

## Final checklist

- No dates, numbers, limits, capabilities, or conclusions were added without a source
- No conditions, exceptions, risks, units, defaults, or recovery steps were dropped
- Subject, object, scope of negation, causation, and degree of certainty are unchanged
- One term per concept throughout
- Second person, active voice, present tense
- Headings, body, cards, and buttons don't repeat each other
- Code, paths, fields, commands, and quotations are byte-identical to the source
- Link text describes its destination
- Google won every conflict with Microsoft

## Reference routing

- Tone, person, voice, tense, must/should/can, anthropomorphism, translation-readiness, inclusive language: read [Voice and language](references/voice-and-language.md)
- Capitalization, punctuation, headings, lists, tables, notices, code blocks, links, code font, UI elements, numbers, dates, units, abbreviations: read [Mechanics and formatting](references/mechanics-and-formatting.md)
- A specific word to keep or replace: read [Word list](references/word-list.md)
- Numbered steps, prerequisites, API reference descriptions, error text: read [Procedures and API reference](references/procedures-and-api.md)
- Establishing a target project's own conventions: read [Project overrides](references/project-overrides-example.md)
