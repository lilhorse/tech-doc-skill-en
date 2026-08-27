# Mechanics and formatting

Source of record: Google developer documentation style guide. Where this file marks a rule **(Microsoft)**, Google is silent and Microsoft supplies the answer.

## Capitalization

- Sentence case for page titles, section headings, table headers, list items, and any UI text you write.
- When you document existing UI, reproduce its label exactly, whatever its case: the **Save All** button stays **Save All**. Capitalize the first word and proper nouns only.
- Don't use title case, and don't capitalize a common noun to make it look important.
- Match the capitalization of product names, API names, and code identifiers exactly as they're defined.

## Headings

- One `h1` per page, and it's unique.
- Task headings start with a bare infinitive: "Create an instance", not "Creating an instance".
- Conceptual headings are noun phrases: "Migration to Google Cloud". Don't start them with an *-ing* verb.
- Don't skip levels (`h2` then `h4`).
- No period or colon at the end of a heading.
- No links inside headings.
- No numbers to convey sequence—the hierarchy conveys it.
- Don't stack a heading directly on another heading with no text between them.
- Don't stack a heading directly on another heading. Introduce a run of subsections with a sentence: "The following sections describe each step."

## Lists

| List type | Use for |
|---|---|
| Numbered | A sequence that matters: ordered steps, phases, ranked priorities |
| Bulleted | A set with no meaningful order |
| Description | Terms paired with definitions or explanations |

- A single item isn't a list.
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

Use code font for: attribute names and values, class names, command output, command-line utility names, data types, database column and row names, constants, DNS record types, element names, enum names, environment variables, filenames, file extensions, paths, folders, HTTP content types, HTTP status codes (`400 Bad Request`), HTTP verbs (`POST`), IAM role names, language keywords, method and function names, namespace aliases, package names, placeholder variables, port numbers, query parameters, strings used in code, and text the reader types.

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
- No empty cells. Write `N/A` or `None` so the reader knows nothing was lost.
- Use a table when readers compare items across two axes. Use a list for anything simpler.

## Notices

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
- Don't include shell prompts (`$`, `>`). Readers copy the whole line.
- Don't mix a command and its output in one block. Separate them and introduce each.
- Uppercase placeholders: `PROJECT_ID`, `REGION`. Explain each one after the block.
- Mark truncation with `...` on its own line and say what you cut.

## Abbreviations

- Expand on first use, then use the abbreviation consistently.
- No periods in an all-caps abbreviation: `US`, not `U.S.`
- Choose *a* or *an* by how the abbreviation is spoken: *an SLO*, *a URL*.
- Don't expand an abbreviation you use only once. Use the full term instead.
- Pluralize without an apostrophe: `APIs`, not `API's`.

## Quotation marks and possessives

- Punctuation goes inside a closing quotation mark in American English, unless it would change a literal string.
- Form the possessive of a singular noun ending in s with `'s`: the class's method.
- Don't make a possessive out of a code element. Write "the value of the `ADDRESS` constant".

## Images

- Every image that carries information needs alt text conveying that information. A purely decorative image takes empty alt text (`alt=""`), not a description.
- Don't rely on position or color to carry meaning. Write "the preceding table", not "the table above"; name a control instead of "the button on the left"; pair any color cue with a label or shape.
- Any information that only exists inside an image is lost to translation and to screen readers. Put it in text.
- Supply high-resolution or vector images where practical.
