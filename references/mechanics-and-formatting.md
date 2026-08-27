# Mechanics and formatting

Source of record: Google developer documentation style guide. Where this file marks a rule **(Microsoft)**, Google is silent and Microsoft supplies the answer.

## Spelling and locale

Google requires standard American spelling and punctuation, and says to write developer
documentation in US English. That is this skill's default, and it is also the rule a project
overrides most often.

Check the project's own convention before you change a single spelling. A project that
serves a British, Irish, Australian, Indian, or Canadian audience may have chosen its locale
deliberately, and rule priority puts that choice above both guides.

These are what the choice governs:

| Aspect | US default | Common alternative |
|---|---|---|
| Verb endings | organize, analyze | organise, analyse |
| Noun endings | color, behavior | colour, behaviour |
| `-er` and `-re` | center, meter | centre, metre |
| Doubled consonants | labeled, modeling | labelled, modelling |
| Noun and verb split | license (both) | licence (noun), license (verb) |

Three things hold whatever the locale:

- Name the variant, not just "British". Oxford style uses `-ize` where Guardian style uses `-ise`, so "en-GB" alone doesn't settle a spelling.
- Apply one locale across a document set. A page that mixes them reads as unedited.
- Never respell code, identifiers, API names, configuration keys, or quoted source text. `initialize()` stays `initialize()` in every locale.

## Capitalization

- Sentence case for page titles, section headings, table headers, list items, and any UI text you write. Capitalize the first word and proper nouns only.
- When you document existing UI, follow the capitalization shown on the page. If a label is all uppercase, or a set of labels is inconsistent, use sentence case instead: `Click **Refresh**`, not `Click **REFRESH**`.
- Don't use title case, and don't capitalize a common noun to make it look important.
- Match the capitalization of product names, API names, and code identifiers exactly as they're defined.

## Headings

- One `h1` per page, and it's unique.
- Task headings start with a bare infinitive: "Create an instance", not "Creating an instance".
- Conceptual headings are noun phrases: "Migration to Google Cloud". Don't start them with an *-ing* verb.
- Don't skip levels (`h2` then `h4`).
- Keep punctuation in a heading simple. Punctuation is a sign the heading is too complicated; consider rewriting.
- No period or colon at the end of a heading. **(MS)**
- No links inside headings.
- No numbers to convey sequence—the hierarchy conveys it.
- Don't use empty headings. Every heading is followed by content.
- Don't refer to a group of sections as "this section" or "these sections"; both are ambiguous. Introduce a run of lower-level sections with "the following sections": "The following sections describe the recommended steps."

## Lists

Choose the list type from what the content is:

| List type | Use for |
|---|---|
| Numbered | A sequence that matters: ordered steps, phases, ranked priorities |
| Bulleted | A set with no meaningful order |
| Description | Terms paired with definitions or explanations |

- A single item isn't a list. The one exception is a single-step procedure, which Google formats as a bulleted list.
- Introduce a list with a complete sentence. Use a colon when the list follows immediately.
- Keep items parallel: same syntax, same grammatical shape.
- Capitalize the first word of each item unless case is significant.
- End punctuation: use periods for items that are complete sentences or contain a verb. Omit it for single words, verbless fragments, items entirely in code font, link text, and document titles.
- Nest sequential sublists with lowercase letters, then lowercase Roman numerals.

## Punctuation

- **Serial comma.** `Android, iOS, and Windows`
- **Em dash**—no spaces before or after. Don't overuse it; a colon or parentheses is often better.
- **En dash**—don't use. Use a hyphen or *to* for ranges. **(Microsoft allows one for page ranges and tight space; Google wins.)**
- **Hyphen**—joins words and connects prefixes. Don't type two hyphens for an em dash.
- One space after a period, question mark, or colon.
- Don't use a dash to separate a term from its description. Use a colon: `Example: this is an example`, not `Example - this is an example`.
- Don't put quotation marks around code unless the quotation marks are part of the code.
- Punctuation goes outside link text: `see [Test your code].` not `see [Test your code.]`

## Code font

Use code font for these:

- Attribute names and values, class names, constants, data types, enum names, and language keywords
- Method and function names, package names, and namespace aliases
- Filenames, file extensions, paths, and folders
- Environment variables, query parameters, and port numbers
- Command-line utility names, command output, and text the reader types
- HTTP verbs (`POST`), status codes (`400 Bad Request`), and content types
- Database column and row names, DNS record types, and IAM role names
- Element names, placeholder variables, and strings used in code

Don't use code font for: domain names, product names, service names, organization names, and URLs the reader opens in a browser.

Don't inflect a code element. Write "the value of the `ADDRESS` constant", not "`ADDRESS`'s value".

## UI elements

- Bold the visible name of any UI element: `Click **Save**`, `In the **New project** window`.
- Don't use code font for a UI label unless it independently qualifies for code font.
- Verbs: **click** (pointer), **tap** (touch), **select** (list items and checkboxes), **press** (keyboard keys), **enter** or **type** (text input), **drag**, **hold the pointer over** (hover), **turn on** / **turn off** (toggles).
- Don't write *hit*. Don't write *press* for an on-screen button.
- Checkboxes are **select** and **clear**, not *check* and *uncheck*.
- Say *list* or *menu*. Don't write *drop-down* or *dropdown* as a noun for a menu.
- Menu paths use the form `**View > Tools**`. This notation is for menus only.
- Prepositions: **in** a dialog, field, list, menu, pane, or window; **on** a page, tab, or toolbar.

## Links

- Link text is either the destination's title or a description of the destination, with the important words first.
- Never *click here*, *here*, *this link*, *this document*, *read more*, or a bare URL as link text.
- Link text must make sense read on its own, out of context.
- Don't reuse the same link text for two different destinations on one page.
- Don't force a new tab. If you must, say "(opens in a new tab)".

## Numbers

- Spell out zero through nine. Use numerals for 10 and above.
- Use numerals below 10 for version numbers, technical quantities and rates, page and chapter numbers, step numbers, and prices: `version 3`, `6 queries per second`, `step 1`.
- If one item in a set needs a numeral, use numerals for all of them: `15 options, 6 of them deselected`.
- Spell out a number that starts a sentence, or rewrite the sentence.
- When two numbers sit together, spell one out: `fifteen 100,000-byte files`.
- Spell out ordinals: *first*, *fifth*, *twenty-first*. Never `1st` or `5th`.
- Ranges use a hyphen with no spaces: `2012-2016`. **(Microsoft writes *from 9 through 17* in prose, en dash only for page ranges; Google wins.)**
- Commas in numbers of four or more digits: `1,532,784`.
- Leading zero on decimals below one: `0.3 inches`.
- Percentages are a numeral plus `%` with no space: `40%`. **(Microsoft writes `40 percent`; Google wins.)** Spell it out only when it starts a sentence.
- Dimensions have no spaces: `192x192`. **(Microsoft writes `1280 × 1024`; Google wins.)**
- Put a nonbreaking space between a numeral and its unit: `64 GB`, `25 mm`, `50 Mbps`. No space for currency, percent, and degrees of an angle: `$10`, `65%`, `180°`. Temperature keeps the space before the degree symbol and none after it: `50 °C`.

## Dates and times

- Preferred date format: `January 19, 2017`. With a weekday: `Tuesday, April 27, 2021`.
- Numeric-only dates use ISO 8601: `2026-04-15`. Never `04/06/2017` or `02.12.2017`.
- Three-letter month abbreviations only where space is tight, capitalized, no period: `Mon, Sep 3, 2018`. Be consistent across the document.
- Times use the 12-hour clock with uppercase AM or PM and a preceding space: `3 PM`, `3:45 PM`. Omit `:00` for whole hours.
- Use a 24-hour clock only when documenting a feature that displays one.
- Avoid time zones where possible. When required, write the full region name with the offset: `US and Canadian Pacific Standard Time (UTC-8)`. Never abbreviate the zone name. Prefer "10 AM your local time".
- Date and time together: date first, then time—`2017-04-15 at 3 PM`.
- Don't use seasons as time markers. Use months or quarters.

## Tables

- Introduce a table with a complete sentence.
- Sentence case headers, no end punctuation.
- Keep cells parallel in structure. One idea per cell.
- A numbered caption takes the form **Table 2.** Description, in sentence case with no final period. Refer to it as "table 2", lowercase.
- Use a table when readers compare items across two axes. Use a list for anything simpler.
- Fill every cell. Write `N/A` or `None` rather than leaving one blank. *(Neither guide states this; it's standard practice.)*

## Notices

Choose the notice from the severity of what can happen:

| Notice | Use for |
|---|---|
| Note | Supplementary information the reader can act on later |
| Caution | Something that can cause data loss, unexpected cost, or a broken state |
| Warning | Something that can cause injury or irreversible loss |

- State the risk and how to avoid it, not just the risk.
- One notice at a time. Don't stack two, and don't bury one inside a step.
- Put the notice before the action it applies to, not after.

## Code blocks

- Tag every fence with its language.
- When a block shows multiple lines of input, start each line with the prompt symbol. Suppress it from click-to-copy by other means rather than dropping it.
- Don't show the current directory path before the prompt.
- Put input and output in separate blocks, and introduce each: "The output is similar to the following:"
- Uppercase placeholders: `PROJECT_ID`, `REGION`. Explain each one after the block.
- Mark truncation with `...` on its own line and say what you cut.

## Abbreviations

- Spell it out on first reference, italicizing both the full term and the abbreviation, then use the abbreviation alone.
- Omit periods in acronyms and initialisms. Keep them in shortened words and in country abbreviations.
- Don't use an abbreviation as a verb.
- No periods in an all-caps abbreviation: `US`, not `U.S.`
- Choose *a* or *an* by how the abbreviation is spoken: *an SLO*, *a URL*.
- Don't expand an abbreviation you use only once. Use the full term instead.
- Pluralize without an apostrophe: `APIs`, not `API's`.

## Quotation marks and possessives

- Always use straight quotation marks and apostrophes, never curly ones.
- Single quotation marks are reserved for code examples and for a quotation nested inside another.
- Commas and periods go inside a closing quotation mark, unless that would change a literal string in code font.
- Technical writing uses quotation marks sparingly outside of code.
- Singular noun ending in s takes `'s`: the class's method. Plural noun ending in s takes a bare apostrophe.
- If a possessive reads awkwardly, rewrite to drop it: `Analyze the business data`, not `Analyze the businesses' data`; `the rule that the Federal Trade Commission (FTC) issued`, not `the Federal Trade Commission's (FTC's) rule`.
- Don't use a possessive for a product, feature, or company name when you describe what it does. Use the name as a modifier, or rephrase with *of*.
- Don't make a possessive out of a code element, a product name, or a feature name. Write "the value of the `ADDRESS` constant".

## Images

- Every image that carries information needs alt text conveying that information. A purely decorative image takes empty alt text (`alt=""`), not a description.
- Don't use directional language to orient the reader: not *above*, *below*, or *right-hand side*. It fails for screen readers, and left and right swap in right-to-left languages. Write "the preceding table"; name a control instead of "the button on the left".
- Keep text contrast at 4.5:1 or better, and don't hide content with `visibility: hidden` or `display: none`.
- Don't let color alone carry meaning. *(Neither guide states this; it's WCAG 1.4.1.)*
- Any information that only exists inside an image is lost to translation and to screen readers. Put it in text.
- Supply high-resolution or vector images where practical.
