# Voice and language

Source of record: Google developer documentation style guide. Microsoft fills the gaps noted below.

## Person

- Address the reader as *you*. Don't use *we* for the reader, and don't call the reader *the user* in the same document where *you* appears.
- *We* is acceptable only for the organization publishing the document, and only when the actor genuinely matters.
- Don't use *he*, *him*, *his*, *she*, *her*, or *hers* in generic references. Rewrite to second person, make the noun plural, use *the* or *a*, name the role (*reader*, *administrator*, *customer*), or use *person*. Singular *they* is acceptable when a rewrite fails. Never write *he/she* or *s/he*.
- Use the pronouns a real person uses for themselves.

| Recommended | Not recommended |
|---|---|
| If you have the required permissions, you can reset other users' passwords. | If the user has the required permissions, he can reset other users' passwords. |
| Developers need access to servers in their development environments. | A developer needs access to servers in his development environment. |

## Voice

Use active voice and name the actor. Passive voice is acceptable when the actor is genuinely unknown, irrelevant, or the system itself in a context where naming it adds nothing.

| Recommended | Not recommended |
|---|---|
| You must configure the firewall rules before you deploy the service. | Configuring the firewall rules is required before deploying the service. |
| The server sends an acknowledgment. | An acknowledgment is sent. |

## Tense

- Use present tense for behavior that isn't tied to a moment in time.
- Use *will* only for something that genuinely happens later, including asynchronous work: "The file is archived the next time the backup runs."
- Cut *would*, *should*, and *could* hypotheticals. State cause and effect directly.

| Recommended | Not recommended |
|---|---|
| Send a query to the service. The server sends an acknowledgment. | Send a query to the service. The server will send an acknowledgment. |
| If you send an unsubscribe message, the server removes you from the list. | You can send an unsubscribe message. The server would then remove you from the list. |

## Register

Aim for a knowledgeable colleague explaining something, not a brochure and not a legal filing.

| Too informal | Just right | Too formal |
|---|---|---|
| Dude! This API is totally awesome! | This API lets you collect data about user preferences. | The API may enable acquisition of information pertaining to user preferences. |
| Just garbage-collect, and you're golden. | To clean up, call the `collectGarbage` method. | Completion requires executing an automated memory management function. |

Avoid:

- Exclamation marks, humor, wackiness, and internet slang
- Idioms and figurative language: *ballpark figure*, *on the back burner*, *hang in there*
- Pop-culture references, holidays, sports, and seasons as time markers
- Filler openers: *please note*, *at this time*, *it should be noted that*
- Condescension: *easy*, *simple*, *simply*, *just*, *obvious*, *of course*, *trivial*
- *please* in instructions

Contractions (*it's*, *you're*, *don't*) are fine and usually read better. Microsoft pushes them harder than Google does; in developer documentation, use them where they fall naturally and don't force them.

## Requirements vocabulary

| Word | Means |
|---|---|
| must | A requirement. Ignoring it breaks something. |
| must not | A prohibition. |
| should | A recommendation with real exceptions. Name the exception. |
| can | An ability or a permission. |
| might | A possibility. |

Don't use *should* for a requirement. Readers treat it as optional, and Google's word list says to use *must* when you mean a requirement.

## Anthropomorphism

Systems don't want, know, think, see, or decide. Name the mechanism instead.

| Recommended | Not recommended |
|---|---|
| The scheduler retries the job three times. | The scheduler decides to try again. |
| The parser rejects input longer than 4 KB. | The parser doesn't like long input. |

## Write for a global audience

Most readers of English technical documentation aren't first-language English speakers, and much of this content gets machine-translated.

- Shorter sentences translate better. This is the single most useful rule here.
- Prefer plain words: *use* not *utilize*, *start* not *commence*, *some* not *a number of*, *through* not *via*.
- Avoid phrasal verbs where a single verb exists. Keep the established ones: *set up*, *log in*, *sign in*.
- Keep *that* in relative clauses: "the rules that you defined", not "the rules you defined".
- Keep *then* in if-then constructions and *of* where it's optional.
- Use at most two noun modifiers in a row. Break up longer strings.
- Place modifiers next to what they modify: "Request only one token", not "Only request one token".
- Repeat a noun rather than let a pronoun dangle: "both IAM segmentation and network segmentation".
- Spell out abbreviations on first use.
- Put information in text, not in images. Images don't get translated.
- Use a consistent, formulaic frame for recurring elements such as link sentences, code sample intros, and output blocks.

## Inclusive language

Google's rules first. Where Google is silent, Microsoft's bias-free communication guidance applies.

### Ableist language

| Use | Instead of |
|---|---|
| complicated, complex, baffling, unexpected (inanimate objects only) | crazy, insane |
| quick check, confidence check, preliminary check | sanity check |
| placeholder | dummy variable |
| slows down, degrades | cripples |
| doesn't respond, stops responding | hangs |

Focus on people, not disabilities: *a reader who is blind*, *a customer with limited dexterity*. Don't write *the disabled*, *suffering from*, *stricken with*, *wheelchair-bound*, *normal*, or *healthy* as the contrast to disabled. Use *nondisabled* or *neurotypical*. Some communities prefer identity-first language (*autistic*, *Deaf*); follow the community's own usage.

### Socially charged terms

| Use | Instead of |
|---|---|
| allowlist | whitelist |
| denylist, blocklist, excludelist | blacklist |
| primary/replica, main, controller | master/slave |
| legacy, exempt | grandfathered |
| built-in, integrated | native (as a value judgment) |
| person hours | man hours |
| everyone, folks, all | guys |
| humanity, people | mankind |
| perimeter network | DMZ, demilitarized zone |

Google prefers `primary/replica`; Microsoft prefers `primary/subordinate`. Follow Google.

### Violent and militaristic language

Avoid *kill*, *abort*, *hit*, *hang*, and military metaphors. Use *stop*, *exit*, *cancel*, *end*, *click*, *press*, *not responding*.

Each of these has a narrow technical carve-out in Google's own word list: *abort* is a Linux signal, *kill* survives in command-line syntax, and *terminate* and *execute* keep their meanings in telephony, networking, and SQL. Outside those, use the plain word.

### Examples and personas

- Use names from a range of cultures and gender identities.
- Don't stereotype job roles, family structures, or economic circumstances.
- Don't name politically disputed places. Keep example regions comparable in kind—don't mix countries with states or continents.
- Don't generalize about any country, region, or culture, including positively.
