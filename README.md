# deslop

English | [한국어](README.ko.md) | [日本語](README.ja.md)

deslop is a Claude skill for text that other people will read. Instead of hunting for words that sound like AI, it has Claude check what the reader will pay for, in three layers: content first, then clarity, then surface patterns.

## What slop means here

Slop is text where the writer saved effort and the reader pays for it. The reader has to work out what is true, what matters, or what a sentence means. Text a person wrote can be slop, and text a model wrote need not be.

The skill checks three layers in order, because fixing a lower layer does nothing while the one above it is empty.

1. Content: is there something to say, and can the writer stand behind it?
2. Clarity: can each sentence be read without decoding?
3. Surface: are there stock patterns that make the reader skip before reading, such as "it's not X, it's Y" or a closing line that only repeats the paragraph?

## When it runs

Claude loads the skill when you ask it to draft, rewrite, or review prose for other people, even if you do not name the skill. Examples are PR descriptions, commit messages, READMEs, design docs, specs, postmortems, reports, proposals, emails, and team updates. Claude decides on its own whether a request is that kind of task, so it can miss one. To be sure, name the skill: "with deslop".

It does not review code, and it does not apply to fiction, poetry, or one-line answers.

It works on text in any language. Korean, Japanese, and English also have their own pattern lists in `references/`. For other languages, the first two layers and the table of patterns common to all languages (in `SKILL.md`) still apply, but there is no language-specific list.

## Install

### Claude Code

To use it in every project, clone it into your personal skills folder.

```bash
git clone https://github.com/prentice7725/deslop ~/.claude/skills/deslop
```

To use it in one project, clone it into that project's `.claude/skills/deslop` instead. To update, run `git pull` in that folder and start a new session.

### Claude app

This means Claude on the web and in the desktop app. Custom skills are available on the Free, Pro, Max, Team, and Enterprise plans and need code execution. On an individual plan, turn on code execution under Settings > Capabilities. On Team and Enterprise, an owner enables it in the organization settings. Then:

1. Get the repository: `git clone` it, or use Code > Download ZIP on GitHub and unzip it.
2. Make sure the folder is named `deslop`. A downloaded ZIP unzips to `deslop-main`, so rename it. The folder name must match the skill's name.
3. Make a ZIP file that contains the `deslop` folder.
4. Upload it under Customize > Skills.

The app keeps its own copy. When this repository is updated, upload a new ZIP.

### Files

```
deslop/
├── SKILL.md              # the three layers and the workflow
├── references/
│   ├── ko.md             # Korean patterns
│   ├── ja.md             # Japanese patterns
│   └── en.md             # English patterns
├── scripts/
│   └── surface_scan.py   # counts sentences and patterns (Python 3, standard library only)
└── LICENSE
```

`SKILL.md` is written in English to use fewer tokens.

## Usage

### Write

Ask for the text as usual, for example "Write the PR description for this branch."

Before writing, Claude answers five questions from the material you gave it: who reads the text, what they should be able to do afterwards, what the point is, what evidence the claims need, and what the text adds. Where the material does not answer one, Claude sorts the gap:

- If precedent or common practice settles it, Claude decides, writes the reason, and labels it as its own decision so you can overrule it.
- If it depends on your own rules, money, people, or policy, Claude leaves it to you. How depends on the length of the text.

| | Long text | Short text |
|---|---|---|
| Examples | Design docs, reports, proposals, articles: several paragraphs that the reader spends time on | Messages, emails, commits, short answers, summaries of one or two paragraphs |
| Gaps that depend on you | Claude asks you before drafting, one or two questions at a time | Claude writes without asking and marks each gap as `[needs confirmation: what]`, written in the language of the text, with who can answer and what stays blocked |
| Outline | Shown to you before the draft | None |
| Separate review | Yes (see below) | No |

Claude decides which kind a text is. You can override it: tell Claude to treat a text as short, to skip the questions or the separate review, or to run the review on a short text.

### Revise

Ask Claude to revise existing text with deslop, for example "Revise this report with deslop." Claude keeps the facts and the author's voice and changes only the sentences that fail a check. It does not fill in an actor, number, or source that the original lacks. For long text, it asks you. For short text, it marks the gap as `[needs confirmation: what]`.

### Diagnose

Ask Claude to diagnose text with deslop, for example "Diagnose this spec with deslop." Claude does not rewrite anything. It numbers the sentences (`[S1]`, `[S2]`, …), tags each problem, reports the problems by layer, and gives the share of defective sentences.

| Tag | Layer | Meaning |
|---|---|---|
| `[blindspot]` | Content | The reader would have to guess, or needs knowledge the text assumes |
| `[inconsistent]` | Content | Two places in the text say different things |
| `[actor]` | Clarity | The sentence hides who does what |
| `[vague]` | Clarity | The reader cannot tell what a word or number refers to |
| `[empty]` | Clarity | Deleting the sentence would lose nothing |
| `[buried]` | Clarity | A failure, risk, or request sits where the reader will miss it |
| `[pattern:name]` | Surface | A stock pattern from the lists |

To find blindspots, Claude lists 5 to 10 questions the reader would bring to the text and answers each from the text alone.

A shortened example. The input:

> An improvement to the login flow was carried out. This is not just a bug fix, it's a paradigm shift. Some tests had issues, but overall it looks good.

The diagnosis:

> Content: the text has no point and no evidence. It does not say what changed or whether it is safe to merge.
> [S1] `[actor]` `[pattern:nominalization]` Who changed what in the login flow?
> [S2] `[empty]` `[pattern:negative parallelism]`
> [S3] `[buried]` `[vague]` Which tests failed, and does that block the merge?
> Defective sentences: 3 of 3.

### Separate review for long text

Writers miss their own contradictions, and they cannot see what the text leaves out because they already know it. So for long text, a second reader checks the finished text. That reader gets only the text and a one-line description of the intended reader, and reports `[inconsistent]` and `[blindspot]` items. Claude then fixes them.

- In Claude Code, Claude runs the second reader as a subagent.
- Where Claude cannot start a subagent, which depends on the environment, it gives you a prompt to paste into a new conversation, and you bring the findings back.

This costs one more pass over the text: the second reader reads it once and writes a report. If no separate review ran, Claude says so when it hands the text over.

### Pattern counts

Models miscount when they count by eye. Where Claude can run code, it counts patterns, bold text, and headings with `scripts/surface_scan.py`. The script needs Python 3. In Claude Code it needs Python on your machine. In the Claude app it runs in the code execution environment. Where the script cannot run, Claude searches for each pattern one at a time instead.

You can run the script yourself:

```bash
python3 scripts/surface_scan.py draft.md            # counts, and flags patterns that appear more than twice
python3 scripts/surface_scan.py draft.md --number   # prints the text with [S1], [S2], ... for diagnosis
```

The script guesses the language from the characters in the text. Use `--lang ko`, `--lang ja`, or `--lang en` to set it. For other languages it uses the English list, so rely only on its counts of sentences, bold text, and headings. It reports counts only. A high count is a reason to look, not a verdict.

## Applying it all the time

The skill loads only when Claude decides the task is writing or reviewing prose. To cover text that appears in every turn, such as Claude Code's work reports, put the core rules where Claude always reads them: `CLAUDE.md` in Claude Code, or a project's instructions in the Claude app.

```markdown
## Writing
- Put the conclusion, result, or request in the first sentence.
- Name the actor in every sentence. Replace pointers and labels coined during the work with real names.
- Separate what was verified from what was not.
- Delete sentences that carry no information.
```

These rules apply to output in any language. You can also translate them.

## Limits

- The checks are a floor. Passing them does not make text good.
- Removing surface patterns alone produces slop that is harder to spot. Fix content and clarity first.
- The person who sends the text owns it. The skill shows where that person must judge. It does not judge for them.

## License

MIT. See [LICENSE](LICENSE).

## References

- [Why AI slop is hard to read](https://zonderlabs.com/slop) (Zonder Labs): three clarity defects
- [No AI Slop: A Manifesto](https://www.slopmanifesto.com/) (AIE Code Summit 2026): responsibility and review cost
- [How we use AI without making AI slop](https://ahrefs.com/blog/how-we-use-ai-without-making-ai-slop/) (Ahrefs): five things to settle before drafting
- [I'm becoming AI blind](https://cymerys.com/w/im-becoming-ai-blind) (cymerys): how readers learn to skip
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing): signs point to a problem and are not the problem
- [doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) (Anthropic): testing a document with a reader who has no context
