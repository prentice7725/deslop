# deslop

[English](README.md) | [한국어](README.ko.md) | 日本語

他人が読む文章からスロップをなくすための Claude スキルです。

ここでいうスロップは「AI が書いた文章」ではなく、**書き手が省いた手間を読み手が払わされる文章**を指します。そのため特定の単語を禁止せず、三つの層を順番に点検します。

1. **内容**: 伝えることがあり、書き手がその内容に責任を持てるか
2. **明確さ**: 文を解読せずに読めるか
3. **表面**: 読む前に読み飛ばされる定型パターンがないか

## 対象

- ドキュメント、報告、メッセージ、メール、記事、要約、回答
- コミットメッセージ、PR の説明、README など、コードまわりの文章

コードそのものと、小説・詩などの創作は対象外です。

## 構成

```
deslop/
├── SKILL.md          # 三つの層の基準と作業手順
└── references/
    ├── ko.md         # 韓国語のパターン
    ├── ja.md         # 日本語のパターン
    └── en.md         # 英語のパターン
```

スキル本文はトークンを節約するために英語で書いています。対象の文章は言語を問いません。参照ファイルには韓国語・日本語・英語それぞれに固有のパターンが入っています。

## インストール

### Claude Code

個人用スキルとして使う場合は、スキルフォルダにクローンします。

```bash
git clone https://github.com/prentice7725/deslop ~/.claude/skills/deslop
```

特定のプロジェクトだけで使う場合は、そのプロジェクトの `.claude/skills/deslop` にクローンします。

### Claude アプリ

`SKILL.md` と `references/` をまとめてスキルとしてアップロードします。アプリに保存したスキルはこのリポジトリと同期されないため、リポジトリを変更したらアップロードし直してください。

## 使い方

文章を書く作業では自動的に読み込まれます。名前で呼び出すこともできます。

- 新しく書く: 「deslop の基準でこの PR の説明を書いて」
- 直す: 「この報告書を deslop で直して」
- 診断だけ: 「この文章を deslop で診断して」（文に `[actor]` `[vague]` `[empty]` `[buried]` `[pattern:名前]` を付け、節どうしの食い違いには `[inconsistent]` を付けて、欠陥のある文の割合を報告します）

材料が足りないときの動作は、文章の長さで変わります。

- 長い文章: 書く前にユーザーに質問します。
- 短い文章: 質問せずに書き、足りない箇所に `[要確認: 何を]` を残します。

## 常に適用したい場合

スキルは、モデルが文章を書く作業だと判断したときだけ読み込まれます。Claude Code の作業報告のように毎回出る文章にも適用するには、`CLAUDE.md` に要点だけ書いておきます。

```markdown
## Writing
- Put the conclusion, result, or request in the first sentence.
- Name the actor in every sentence. Replace pointers and labels coined during the work with real names.
- Separate what was verified from what was not.
- Delete sentences that carry no information.
```

## 限界

- この基準は下限です。通過しても良い文章になるとは限りません。
- 表面のパターンだけを消すと、見分けにくいスロップになるだけです。内容と明確さを先に直します。
- 文章に責任を持つのは、それを送り出す人です。

## 参考にした文章

- [Why AI slop is hard to read](https://zonderlabs.com/slop) (Zonder Labs): 明確さの三つの欠陥
- [No AI Slop: A Manifesto](https://www.slopmanifesto.com/) (AIE Code Summit 2026): 責任とレビューコスト
- [How we use AI without making AI slop](https://ahrefs.com/blog/how-we-use-ai-without-making-ai-slop/) (Ahrefs): 下書きの前に決める五つのこと
- [I'm becoming AI blind](https://cymerys.com/w/im-becoming-ai-blind) (cymerys): 読み手が読み飛ばすようになる過程
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing): 兆候は問題そのものではないという見方
