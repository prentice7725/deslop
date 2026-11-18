---
name: deslop
description: Use when writing, revising, or reviewing text that someone else will read (docs, reports, messages, PR descriptions, articles, summaries, final answers). Checks content ownership, sentence clarity, and skip-triggering stock patterns, in that order, to prevent slop. Includes Korean, Japanese, and English patterns.
---

# deslop

Slop is not "text written by AI". Slop is **text where the writer saved effort and the reader pays for it**.
If the reader has to work out what is true, what matters, or what a sentence means, the text is slop.

Readers who meet slop often enough stop reading anything that looks like it. Correct content then goes unread.
So check three layers in order. Fixing a lower layer is pointless while the one above it is empty.

1. **Content**: is there something to say, and can the writer stand behind it?
2. **Clarity**: can each sentence be read without decoding?
3. **Surface**: are there stock patterns that make the reader skip before reading?

## Scope

- Applies to text people read: docs, reports, messages, email, articles, summaries, answers, and text around code such as commit messages, PR descriptions, and READMEs.
- Does not review code itself (structure, quality, commented-out code).
- Does not apply to fiction or poetry.
- Apply in the language of the text. For layer 3, read the reference file for that language.

## Layer 1: Content

Before writing, answer five questions in one line each.

- **Reader**: who reads this, and how much of this conversation or task do they know?
- **Promise**: what should the reader know or be able to do afterwards?
- **Point**: what does the text say in one sentence? Could someone disagree with it?
- **Evidence**: which claims need a source, data, or a run result? Do you have it?
- **Addition**: what does this add beyond what the reader knows or could search for?

### When an answer is missing

Handle it by the size of the text.

- **Long text** (documents, articles, reports, proposals, design docs: several paragraphs that the reader spends time on): ask the user before writing. One or two questions at a time, starting with the one that shapes the text most.
- **Short text** (messages, email, commits, short answers, one- or two-paragraph summaries): write without asking. Do not invent the missing part. Mark it as `[needs confirmation: what]`, written in the language of the text, and list the marks in one line at the end.
- In both cases, never fill a gap with a plausible example, anecdote, number, or source.

### Rules

- Separate what was verified from what was not. Do not mix what you ran, what you only read, and what you inferred.
- If there is nothing to add, write less or do not write. Do not cover a gap with volume.
- Length is review cost for the reader. If reading and checking takes more effort than producing did, cut.
- Every paragraph must serve the promise. Cut paragraphs that do not, even when they are true.

## Layer 2: Clarity

Ask three questions of every sentence.

### Is it obvious who does what?

- Do not turn actions into nouns. "Validation was performed" → "The test suite validated the input"
- Avoid passives with no actor. "The cache was changed to be invalidated" → "`save()` invalidates the cache right after writing"
- Do not use abstract nouns as subjects. The subject is the real actor: a person, a function, a team, or you.
- Leave the sentence alone when the actor truly does not matter or the order is deliberate emphasis.

### Does the reader know what every term refers to?

- Replace pointers ("this", "that part", "the approach above") with names.
- Unpack noun stacks with verbs. "token refresh failure handling logic improvement" → "when token refresh fails, the app now sends the user to the login screen"
- Do not give plain things grand names. A config file is not a "configuration orchestration layer".
- Labels coined during the work ("approach B", "the new pipeline") are unknown to the reader. Spell them out or use the real name.
- Replace evaluative words with numbers and conditions. "much faster" → "p95 latency 420ms → 180ms". If there is no number, say so.
- Do not drop articles, particles, or connectives to save space. Telegraphic text is ambiguous.

### Would the reader lose anything if this were deleted?

- Put the conclusion, result, or request in the first sentence. Background and process come after.
- Delete sentences that carry no information: restating the question, announcing that something is important, a closing summary that repeats the body.
- State what the reader must do (confirm, decide, run) in its own sentence, with who does what.
- Do not bury failures or unfinished work among successes.

## Layer 3: Surface

The patterns below signal "not worth reading". Most are symptoms of layer 1 or 2 defects, so **fix the cause first, then delete what remains**. This is not a banned-word list. People write these too, and one or two instances are fine. Fix them when they repeat.

### All languages

| Pattern | Fix |
|---|---|
| Inflated significance: a small change presented as a breakthrough or turning point | Say what actually changes. If nothing does, delete |
| Negative parallelism: denying a claim nobody made, then stating the point | State the point |
| Reflexive triplets: adjectives or items always in threes | Use the real count, and only items you can support |
| Empty tails: clauses tacked on to say something "shows the importance of" something | Replace with a concrete result, or delete |
| Unsourced authority: "experts say", "it is widely known" | Name the source, or own the claim |
| Stacked hedges: several qualifiers in one sentence | Hedge once, where the uncertainty is, with the reason |
| Leaked reasoning: weighing options at length without deciding | Give the decision and the reason. Mention rejected options only if the reader would ask |
| Heavy formatting: bold in every paragraph, headers on short text, an argument chopped into bullets | Format only what the reader will scan or compare |
| Chat residue: opening with praise, closing with an offer to help | Delete |
| Elegant variation: one thing called a different name in each sentence | One thing, one name |
| Uniform rhythm: paragraphs of equal length, an aphorism closing each one | Write as much as the content needs |

### Per-language patterns

Read only the file for the language of the text.

- Korean: `references/ko.md`
- Japanese: `references/ja.md`
- English: `references/en.md`

## Handing off

When passing the result to a person or another agent, add:

- what you verified directly and what you could not
- the points where the reader must decide, and what they need to decide
- the boundary between material the user gave you and what you added (especially if the user will publish under their own name)
- the list of remaining `[needs confirmation]` marks

Text you hand off stays in docs, chat, and repos and becomes source material for the next text. Wrong or empty sentences get copied from there.

## Workflow

**Writing new text**

1. Answer the five layer-1 questions. Handle gaps as described in "When an answer is missing".
2. Write the point in one sentence. If you cannot, it is not time to write yet.
3. For long text, show an outline first and get confirmation. Check that each section serves the promise.
4. Write the draft.
5. Check layer 2 sentence by sentence. Fix only the sentences that fail.
6. For layer 3, check the all-languages table and the reference file for the language. Fix repeated patterns from the cause.
7. Reread from the top: does a reader who stops after two sentences know the point?

**Revising existing text**

- Do not change facts or the author's voice. Do not touch sentences that have no problem.
- Do not supply information the original lacks (actor, number, source). For long text, ask the author. For short text, mark `[needs confirmation]`.
- If layer 1 is empty (no point, no evidence), say so before polishing sentences.

**Diagnosis only**

- Report by layer, layer 1 first.
- Tag sentences: `[actor]` `[vague]` `[empty]` `[pattern:name]`
- Report defective sentences over total sentences.
- Do not judge whether the text "looks AI-written". This skill measures reader cost, not origin.

## Limits

- These checks are a floor. Passing them does not make text good.
- Do not use this to pass layer 3 alone. Slop with the patterns removed is slop that is harder to spot.
- The person who sends the text owns it. This skill exposes the points where they must judge. It does not judge for them.
