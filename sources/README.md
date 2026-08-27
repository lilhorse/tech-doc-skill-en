# Source snapshot

Plain-text snapshot of both style guides. Every rule in this skill was checked against it.

**The text itself is not in this repository.** Google's pages are CC BY 4.0, but the
Microsoft pages carry no open license, so neither set is redistributed here. Fetch your own
copy first:

```bash
scripts/refresh_sources.sh
```

That writes 70 Google pages and 9 Microsoft pages into the following directories, about 900 KB.

The script fills these:

| Directory | Contents |
|---|---|
| `google/` | All 70 pages of the Google developer documentation style guide |
| `microsoft/` | The 9 Microsoft Writing Style Guide pages this skill relies on |

## Why it's here

The rules in this skill were first written from summarized fetches of these pages. That
produced entries for words the guide doesn't carry, a fabricated example, and a rule
stated backwards. Grepping the text avoids all three.

## Check a rule

```bash
grep -ri "serial comma" sources/
grep -i "prompt symbol" sources/google/code-syntax.txt
```

Entries in `google/word-list.txt` are anchored, so a term's own entry is findable by its
id: `grep -o 'id="utilize".\{0,400\}' sources/google/word-list.txt`.

## Limits

This is a snapshot, not the authority. Both guides change. When a rule carries real
weight, confirm it against the live page:

- https://developers.google.com/style
- https://learn.microsoft.com/style-guide

Run `scripts/refresh_sources.sh` to re-fetch. Diff the result before trusting it: a page
that shrinks to a few kilobytes means the fetch failed, not that the rule was deleted.
