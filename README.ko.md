# deslop

[English](README.md) | 한국어 | [日本語](README.ja.md)

남이 읽을 글에서 슬롭을 막는 Claude 스킬입니다.

여기서 슬롭은 "AI가 쓴 글"이 아니라 **쓰는 쪽이 아낀 수고를 읽는 쪽이 대신 치르는 글**을 뜻합니다. 그래서 특정 단어를 금지하지 않고, 세 층을 순서대로 점검합니다.

1. **내용**: 전할 것이 있고, 그것을 책임질 수 있는가
2. **명확성**: 문장을 해독 없이 읽을 수 있는가
3. **표면**: 독자가 읽기 전에 넘겨버릴 상투 패턴이 있는가

## 대상

- 문서, 보고, 메시지, 메일, 기사, 요약, 답변
- 커밋 메시지, PR 설명, README 같은 코드 주변의 글

코드 자체와 소설·시 같은 창작물은 다루지 않습니다.

## 구성

```
deslop/
├── SKILL.md          # 세 층의 기준과 작업 방식
└── references/
    ├── ko.md         # 한국어 패턴
    ├── ja.md         # 일본어 패턴
    └── en.md         # 영어 패턴
```

스킬 본문은 토큰을 아끼려고 영어로 썼습니다. 적용 대상은 언어를 가리지 않으며, 참조 파일에 한국어·일본어·영어 고유의 패턴이 들어 있습니다.

## 설치

### Claude Code

개인 스킬로 쓰려면 스킬 폴더에 클론합니다.

```bash
git clone https://github.com/prentice7725/deslop ~/.claude/skills/deslop
```

특정 프로젝트에서만 쓰려면 그 프로젝트의 `.claude/skills/deslop`에 클론합니다.

### Claude 앱

`SKILL.md`와 `references/`를 묶어 스킬로 업로드합니다. 앱에 저장한 스킬은 이 저장소와 동기화되지 않으므로, 저장소를 고친 뒤에는 다시 올려야 합니다.

## 쓰는 법

글쓰기 작업에서 자동으로 불려 옵니다. 직접 부를 수도 있습니다.

- 새로 쓰기: "deslop 기준으로 이 PR 설명 써줘"
- 다듬기: "이 보고서 deslop으로 다듬어줘"
- 진단만: "이 글 deslop으로 진단해줘" (문장마다 `[actor]`, `[vague]`, `[empty]`, `[pattern:이름]` 중 하나를 붙이고 결함 문장 비율을 보고합니다)

재료가 비어 있을 때의 동작은 글의 크기에 따라 다릅니다.

- 긴 글: 쓰기 전에 사용자에게 묻습니다.
- 짧은 글: 묻지 않고 쓰되, 빈 곳에 `[확인 필요: 무엇]`을 남깁니다.

## 항상 적용하고 싶다면

스킬은 모델이 글쓰기 작업이라고 판단할 때만 불려 옵니다. Claude Code의 작업 보고처럼 매번 나오는 글에도 적용하려면 `CLAUDE.md`에 핵심만 적어 둡니다.

```markdown
## Writing
- Put the conclusion, result, or request in the first sentence.
- Name the actor in every sentence. Replace pointers and labels coined during the work with real names.
- Separate what was verified from what was not.
- Delete sentences that carry no information.
```

## 한계

- 이 기준은 하한선입니다. 통과했다고 좋은 글이 되지는 않습니다.
- 표면 패턴만 지우면 알아보기 어려운 슬롭이 될 뿐입니다. 내용과 명확성을 먼저 고칩니다.
- 글을 책임지는 것은 내보내는 사람입니다.

## 참고한 글

- [Why AI slop is hard to read](https://zonderlabs.com/slop) (Zonder Labs): 명확성의 세 가지 결함
- [No AI Slop: A Manifesto](https://www.slopmanifesto.com/) (AIE Code Summit 2026): 책임과 검토 비용
- [How we use AI without making AI slop](https://ahrefs.com/blog/how-we-use-ai-without-making-ai-slop/) (Ahrefs): 쓰기 전에 정할 다섯 가지
- [I'm becoming AI blind](https://cymerys.com/w/im-becoming-ai-blind) (cymerys): 독자가 글을 건너뛰게 되는 과정
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing): 징후는 문제 자체가 아니라는 관점
