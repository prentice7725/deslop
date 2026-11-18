# deslop

English | [한국어](README.ko.md) | [日本語](README.ja.md)

A Claude skill that keeps slop out of text other people will read.

Slop here does not mean "text written by AI". It means **text where the writer saved effort and the reader pays for it**. So the skill bans no words. It checks three layers in order.

1. **Content**: is there something to say, and can the writer stand behind it?
2. **Clarity**: can each sentence be read without decoding?
3. **Surface**: are there stock patterns that make the reader skip before reading?

## Scope

- Docs, reports, messages, email, articles, summaries, answers
- Text around code: commit messages, PR descriptions, READMEs

It does not review code itself, and it does not apply to fiction or poetry.

## Layout

```
deslop/
├── SKILL.md          # the three layers and the workflow
└── references/
    ├── ko.md         # Korean patterns
    ├── ja.md         # Japanese patterns
    └── en.md         # English patterns
```

The skill is written in English to keep token use low. It applies to text in any language, and the reference files hold the patterns specific to Korean, Japanese, and English.

## Install

### Claude Code

To use it as a personal skill, clone it into your skills folder.

```bash
git clone https://github.com/prentice7725/deslop ~/.claude/skills/deslop
```

To use it in one project only, clone it into that project's `.claude/skills/deslop`.

### Claude app

Upload `SKILL.md` and `references/` together as a skill. A skill saved in the app does not sync with this repository, so upload it again after the repository changes.

## Usage

The skill loads automatically for writing tasks. You can also call it by name.

- Write: "Write this PR description with deslop"
- Revise: "Revise this report with deslop"
- Diagnose: "Diagnose this text with deslop" (tags each sentence with `[actor]`, `[vague]`, `[empty]`, or `[pattern:name]` and reports the share of defective sentences)

When source material is missing, the behavior depends on the size of the text.

- Long text: the skill asks you before writing.
- Short text: it writes without asking and leaves `[needs confirmation: what]` where the gap is.

## Applying it all the time

A skill loads only when the model decides the task is a writing task. To cover text that appears every turn, such as Claude Code's work reports, put the core rules in `CLAUDE.md`.

```markdown
## Writing
- Put the conclusion, result, or request in the first sentence.
- Name the actor in every sentence. Replace pointers and labels coined during the work with real names.
- Separate what was verified from what was not.
- Delete sentences that carry no information.
```

## Limits

- These checks are a floor. Passing them does not make text good.
- Removing surface patterns alone produces slop that is harder to spot. Fix content and clarity first.
- The person who sends the text owns it.

## References

- [Why AI slop is hard to read](https://zonderlabs.com/slop) (Zonder Labs): three clarity defects
- [No AI Slop: A Manifesto](https://www.slopmanifesto.com/) (AIE Code Summit 2026): responsibility and review cost
- [How we use AI without making AI slop](https://ahrefs.com/blog/how-we-use-ai-without-making-ai-slop/) (Ahrefs): five things to settle before drafting
- [I'm becoming AI blind](https://cymerys.com/w/im-becoming-ai-blind) (cymerys): how readers learn to skip
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing): signs point to a problem and are not the problem
