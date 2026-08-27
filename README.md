# tech-doc-skill-en

A Claude Code skill for writing, editing, and reviewing English technical documentation.
It applies the [Google developer documentation style guide](https://developers.google.com/style)
first, and the [Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide) only
where Google is silent. Google wins every conflict, and the conflicts that actually change
output are listed in one table.

Every rule was checked against the text of both guides rather than recalled. Rules that
belong to neither guide are confined to a labeled section and marked as such.

## Install

```bash
git clone https://github.com/lilhorse/tech-doc-skill-en.git \
  ~/.claude/skills/tech-doc-style-english
cd ~/.claude/skills/tech-doc-style-english
scripts/refresh_sources.sh
```

The skill loads in the next session. The second command fetches the style guide text that
the skill greps to settle a rule; see [Sources](#sources) for why it isn't bundled.

Other agent runtimes read `SKILL.md` the same way. Codex and Gemini CLI look in
`~/.codex/skills/` and `~/.agents/skills/`.

## Layout

The entry point is `SKILL.md`; everything else is loaded on demand or run by hand:

| Path | Contents |
|---|---|
| `SKILL.md` | Entry point: authority, scope, rule priority, conflict table, routing |
| `references/` | Voice, mechanics, word list, procedures, and a project override template |
| `scripts/lint_en_docs.py` | Style checker; `--min-level warning` reports only sourced rules |
| `scripts/refresh_sources.sh` | Fetches both guides as plain text |
| `tests/` | 61 unit tests for the checker |
| `eval/` | Held-out evaluation harness, scored against Google's own counter-examples |

## Check a document

```bash
python3 scripts/lint_en_docs.py --min-level warning FILE
```

Findings are candidates, not verdicts. Several rules are heuristic, and a document that has
to *name* a banned word reports findings that should be ignored.

## Sources

`sources/` holds both guides as plain text. Google publishes its pages under CC BY 4.0.
The Microsoft pages carry no open license, so neither set is redistributed here. Run
`scripts/refresh_sources.sh` to fetch your own copy, about 900 KB.

The text matters because summarized fetches proved unreliable while the rules were being
written. They truncated a long page, then reported the missing part as absent from the
guide. That produced an entry banning a word Google recommends, a fabricated example, and
one rule stated backwards. Grepping the text caught all three.

## Tests

Two layers, for two kinds of change:

```bash
python3 tests/test_lint_en_docs.py   # after changing the checker
python3 eval/score.py verify         # before trusting an evaluation score
```

`eval/README.md` describes the harness. Run it after changing a **rule**, since unit tests
cannot see a rule that is too strict or too lax. Both defects it has caught so far passed
every unit test.

## License

This skill is MIT licensed; see [LICENSE](LICENSE).

That covers the rules, the checker, and the harness. It does not cover the style guides
themselves, which are not redistributed here. The Google developer documentation style
guide is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), and the
Microsoft Writing Style Guide belongs to Microsoft.

## Credits

The layout follows [Fenng/tech-doc-style-chinese](https://github.com/Fenng/tech-doc-style-chinese),
which does the same job for Chinese technical writing.
