# Procedures and API reference

Source of record: Google developer documentation style guide.

## Before the steps

- Give the reader the context they need to start: what the procedure accomplishes, and what it assumes.
- State required hardware, software, permissions, and prerequisites up front, not at the step where they bite.
- Introduce the procedure with a complete sentence.

## Numbered steps

- Number the steps of a sequence. Write a single-step procedure as an ordinary sentence, not a one-item list: "To clear the log, click **Clear logcat**."
- Start each step with an imperative verb: *Click*, *Run*, *Download*, *Connect*.
- One action per step. Small sequential actions in the same place may combine: `Click **File > New > Document**`.
- State the location before the action: "In Google Docs, click **File**", not "Click **File** in Google Docs".
- Put a condition before its instruction: "If the build fails, check the logs", not "Check the logs if the build fails".
- Mark an optional step with a leading `Optional:`—not parentheses. `Optional: Enter a description.`
- State the action first and the result second, in the same paragraph.
- Give a justification where a step's purpose isn't self-evident: "Store the private key somewhere safe. You need it later."
- Sub-steps use lowercase letters; sub-sub-steps use lowercase Roman numerals.
- A parent step that introduces sub-steps behaves like an introductory sentence—end it with a colon or a period accordingly.

| Recommended | Not recommended |
|---|---|
| In the Google Cloud console, click **Create instance**. | Click **Create instance** in the Google Cloud console. |
| Optional: Enter a display name. | (Optional) Enter a display name. |
| If the key is missing, then generate a new one. | Generate a new one if the key is missing. |

## API reference descriptions

- Present tense. Third-person verb form: "Gets the...", not "Will get the..." or "Get the...".
- Make the first sentence complete, unique, and useful on its own—indexes often extract only that sentence.
- Don't repeat the class or method name in its own description, and don't start with "This method...".
- Write *for example*, not *e.g.*—an abbreviation with a period can truncate the extracted first sentence.

### Opening verbs by member type

| Member | Opens with |
|---|---|
| Method returning data | Adds..., Creates..., Returns... |
| Boolean getter | Checks whether... |
| Non-boolean getter | Gets the... |
| Method with no return value | Sets..., Updates..., Deletes..., Registers... |
| Callback | Called by... |
| Convenience constructor | Creates a... |

### Parameters

- Capitalize the first word and end with a period.
- Non-boolean parameters start with *The* or *A*.
- Action-oriented boolean: "If `true`, the cache is bypassed. If `false`, the cached value is returned."
- State-declaring boolean: "`true` if the record exists; `false` otherwise."
- Parameters with defaults: explain each value, then state `Default: <value>`.
- Give type, unit, allowed range, and whether the parameter is required.

### Return values and exceptions

- Keep return descriptions short; put the elaboration in the class or method description.
- Non-boolean: "The bird specified by the given ID."
- Boolean: "`true` if the bird exists; `false` otherwise."
- Exceptions begin with "If..." when the tool inserts "Throws", and "Thrown when..." when it doesn't.

### Deprecation

Lead with the replacement, then the reason, then the migration path: "Deprecated. Use `CameraPose` instead."

## Error and status text

- Say what happened, what it affects, and what to do next. An error that only names a failure is incomplete.
- Name the object and the actual cause. Don't write "An error occurred".
- Don't blame the reader, and don't apologize at length.
- Keep verbatim error strings from the product byte-identical when you document them. Put the fix in the surrounding prose.
- Document HTTP status codes in code font (`404 Not Found`) with the condition that produces each one and the recovery action.

| Recommended | Not recommended |
|---|---|
| The upload failed because the file is larger than 10 MB. Compress the file or split it, then try again. | An error occurred. Please try again later. |
| You need an ID that looks like this: `someone@example.com` | Invalid ID |
