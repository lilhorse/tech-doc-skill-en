# Word list

Entries from the Google developer documentation style guide word list, plus a few Microsoft entries marked **(MS)** where Google is silent. Google wins any conflict. Anything not in either guide is confined to the last section and labelled as such.

## Replace these

The following entries come from Google's word list unless marked otherwise:

| Don't use | Use instead | Why |
|---|---|---|
| abort | stop, exit, cancel, end | Violent metaphor. Google says *avoid in general usage*; the Linux signal keeps its name |
| and/or | *and*, or *or*, or rewrite | Ambiguous; hard to translate. Allowed only where space is tight, such as a table |
| at this time | now, or delete | Filler |
| black box | synthetic monitoring (monitoring), opaque-box testing (testing) | Google scopes this entry to monitoring and testing |
| displays (intransitive) | is displayed, appears | *display* is transitive and needs an object |
| blacklist | denylist, blocklist, excludelist | Charged |
| chubby | unused, overextended | Charged |
| click here | descriptive link text | Meaningless out of context |
| cripple | slows down, degrades | Ableist |
| dummy variable | placeholder | Ableist |
| e.g. | for example | Latin abbreviation; often misread |
| easy, easily, simple, simply, just | delete, or state the actual steps | In a procedure this is a prohibition. In prose the word list says only "try eliminating this word" |
| email (as a verb) | send an email | |
| execute | run | *run* is plainer. Keep *execute* where it's the precise technical term |
| first-class citizen | higher-order, anonymous, nested | Charged and imprecise |
| grandfathered | legacy, exempt | Charged |
| guys | everyone, folks, all | Gendered |
| hang, hung | stop responding, not responding | Violent metaphor |
| hit | click, press, or type | Violent metaphor |
| i.e. | that is | Latin abbreviation; often misread |
| in order to | to | Wordy |
| insane, crazy | baffling, unexpected | Ableist |
| kill | stop, exit, cancel, end | Violent metaphor. Avoid where possible; command-line syntax is the exception |
| leverage (as a verb) | use, build on, take advantage of | Jargon |
| login (as a verb) | sign in, or log in | *login* is the noun; Google prefers *sign in* unless the product says *log in* |
| man hours | person hours | Gendered |
| manpower | staff, workforce | Gendered |
| man-in-the-middle, MITM | on-path attacker, person-in-the-middle (PITM) | Gendered |
| mankind | humanity, people | Gendered |
| master/slave | primary/replica, main, controller | Charged. **(MS says primary/subordinate; Google wins.)** |
| native | built-in, integrated, or name the platform | Vague value judgment |
| please note, note that | delete | Filler |
| sanity check | quick check, confidence check, preliminary check, coherence check | Ableist |
| setup (as a verb) | set up | *setup* is the noun |
| terminate | stop, exit, cancel, end | Violent metaphor. Keep it where it's the precise technical term |
| via | through, by, using | Latin; harder to translate |
| we (meaning the reader) | you | Wrong person |
| whitelist | allowlist, trustlist, safelist | Charged |

## Use with care

These are reserved rather than banned:

| Term | Guidance |
|---|---|
| please | Omit from ordinary steps. Both guides keep it where the request genuinely inconveniences the reader or the product is at fault. |
| utilize | Don't use where you mean *use*. It's fine for a quantity of a resource: "When CPU utilization exceeds 75%". |
| the user | Reserve for the end user of the software your reader is building. Address your reader as *you*. |
| dropdown, drop-down | Don't use as a noun for a menu. Write *list* or *menu*. |
| should | Generally avoid: ambiguous by definition. Use *must* for a requirement, *can* for an ability. |
| appears | Fine for something a person perceives; not for UI that *is displayed*. |
| between, among | *between* for two or more distinct things; *among* for things in a group or not distinct: shared *among* multiple apps. |
| once | Means both "one time" and "after". Use *after* when that's the meaning. |
| since | Use for time. Use *because* for causation. |
| may | Reserve for official policy and legal wording. Use *can* for permission or ability, *might* for possibility. |
| DMZ, demilitarized zone | Use *perimeter network*. |
| K, M, B for thousand/million/billion | Spell out or give the full number. **(MS)** |

Google's own Recommended examples still contain the comparative *easier*, so don't extend the row above to every form of the word. The prohibition covers *simply*, *It's easy*, *It's that simple*, and *quickly* inside a procedure.

## Keep these as-is

Established terms that read as phrasal verbs but shouldn't be simplified: *set up*, *log in*, *sign in*, *back up*, *roll back*, *fall back*.

## Not in either guide

Standard editorial practice, kept here because it earns its place. Don't cite these as Google or Microsoft rules.

| Prefer | Over | Why |
|---|---|---|
| lets you | allows you to | Wordy |
| delete it | obvious, of course, trivial | Same condescension the guides flag in *easy* and *simple* |
| state the mechanism | the system wants, knows, thinks, decides | Anthropomorphism |
