# Project overrides

A target project overrides this skill. Copy this template into the project (for example, into its `CLAUDE.md`, `AGENTS.md`, or `docs/STYLE.md`), fill in what actually applies, and delete the rest.

Don't treat the placeholder values in this template as anyone's real conventions.

```markdown
## Documentation style

Base: Google developer documentation style guide, then the Microsoft Writing Style Guide where Google is silent.
The overrides in this section beat both.

### Product and term names

Use the left column everywhere, including headings and UI text:

| Write | Never write |
|---|---|
| Acme Cloud Run | ACR, acme-cloud-run, Acme CloudRun |
| workspace | org, tenant, account |
| API key | token, secret key |

### Spelling and locale

- Locale: en-US (default) | en-GB | en-AU | other: ___
- Variant, if not en-US: <Oxford (-ize) | Guardian (-ise) | other>
- Date format in prose: <default: January 19, 2026>
- Numeric date format: <default: ISO 8601, 2026-01-19>

### Voice exceptions

- Second person: <default: required>
- Contractions: <default: allowed>
- Marketing pages may use <list the exceptions, or state none>

### Formatting

- Headings: sentence case <default>
- Code fences: language tag required | optional
- UI element formatting: bold <default> | other: ___
- Line length in Markdown source: <e.g. one sentence per line, or 100 columns, or unlimited>

### Content that must not be edited

- <paths, generated files, vendored docs, legal text, verbatim error strings>

### Review conventions

- Where to file style questions: <link>
- Who owns the glossary: <role or team>
```

## How to use overrides

1. Read the project's own instruction files and glossary before editing anything.
2. When the project contradicts this skill, follow the project and note the divergence in your summary.
3. When the project is silent, follow this skill.
4. Don't invent a project convention from a single example in the codebase. One occurrence is a data point, not a rule—check whether it's consistent before generalizing.
