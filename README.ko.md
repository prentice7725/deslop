# kouetsu

[English](README.md) | 한국어 | [日本語](README.ja.md)

kouetsu는 남이 읽을 글을 위한 Claude 플러그인입니다. 이름은 일본어 校閲(교열)에서 왔습니다. 글을 내보내기 전에 사실관계와 앞뒤가 맞는지 확인하는 편집 작업을 뜻합니다. AI 말투로 들리는 단어를 찾아 지우는 대신, 독자가 무엇을 대신 치르게 되는지를 내용, 명확성, 표면 패턴 순서로 Claude가 점검하게 합니다.

## 여기서 말하는 슬롭

슬롭은 쓰는 쪽이 아낀 수고를 읽는 쪽이 대신 치르는 글입니다. 독자가 무엇이 맞는지, 무엇이 중요한지, 문장이 무슨 뜻인지를 직접 가려내야 합니다. 사람이 쓴 글도 슬롭일 수 있고, 모델이 쓴 글이라고 슬롭인 것은 아닙니다.

스킬은 세 층을 순서대로 점검합니다. 위층이 비어 있으면 아래층을 고쳐도 소용이 없기 때문입니다.

1. 내용: 전할 것이 있고, 쓴 사람이 그것을 책임질 수 있는가
2. 명확성: 문장을 해독 없이 읽을 수 있는가
3. 표면: 독자가 읽기 전에 넘겨버릴 상투 패턴이 있는가. 예를 들어 "단순한 X가 아니라 Y입니다"나, 문단 내용을 되풀이하기만 하는 마무리 문장

## 언제 불리는가

남이 읽을 글을 쓰거나, 고쳐 쓰거나, 검토해 달라고 하면 Claude가 이 스킬을 불러옵니다. 스킬 이름을 말하지 않아도 됩니다. PR 설명, 커밋 메시지, README, 설계서, 사양서, 장애 회고, 보고서, 제안서, 메일, 팀 공지가 그 예입니다. 요청이 이런 작업인지는 Claude가 스스로 판단하므로 놓칠 수도 있습니다. 확실히 하려면 "kouetsu로"라고 이름을 붙이세요.

코드는 검토하지 않고, 소설·시·한 줄 답변에는 적용하지 않습니다.

어느 언어의 글에도 쓸 수 있습니다. 한국어·일본어·영어는 `references/`에 언어별 패턴 목록이 따로 있습니다. 그 밖의 언어에서는 첫 두 층과 모든 언어에 공통인 패턴 표(`SKILL.md`에 있음)가 그대로 적용되지만, 언어별 목록은 없습니다.

## 설치

kouetsu는 스킬 하나를 담은 Claude 플러그인입니다. Claude Code와 Claude 앱에서 동작합니다. Python 3은 없어도 됩니다. Claude가 패턴을 셀 때 쓰고, 없으면 검색해서 셉니다.

### Claude Code

Claude Code에서 다음 두 명령을 실행합니다.

```
/plugin marketplace add prentice7725/kouetsu
/plugin install kouetsu@prentice7725
```

업데이트하려면 `/plugin marketplace update prentice7725`를 실행하고 새 세션을 시작합니다.

설치하지 않고 로컬 사본으로 시험하려면, 클론한 폴더의 상위 폴더에서 `claude --plugin-dir ./kouetsu`를 실행합니다.

### Claude 앱

웹과 데스크톱 앱의 Claude를 말합니다. 스킬은 Free, Pro, Max, Team, Enterprise 요금제에서 쓸 수 있고, 코드 실행이 켜져 있어야 돕니다. 개인 요금제는 Settings > Capabilities에서 켭니다. Team과 Enterprise는 소유자가 조직 설정에서 켜고, 구성원이 플러그인을 추가할 수 있는지도 조직 설정이 정합니다. Plugins 메뉴가 보이지 않으면 소유자에게 문의하세요. 그다음 두 방법 중 하나로 플러그인을 추가합니다.

- Customize > Plugins > Add > Add marketplace에 `https://github.com/prentice7725/kouetsu`를 입력합니다. 앱이 이 저장소를 따라가므로 업데이트를 받습니다.
- GitHub에서 Code > Download ZIP으로 저장소를 받아, Customize > Plugins > Add > Upload plugin에서 올립니다. 앱은 그 사본을 보관하므로, 저장소가 바뀌면 새 ZIP을 다시 올려야 합니다.

메뉴 이름은 영어 화면 기준입니다.

### 스킬만 쓰기 (Claude Code)

Claude Code에서 플러그인 없이 스킬만 쓰려면 `skills/kouetsu` 폴더를 `~/.claude/skills/kouetsu`에 복사합니다. 업데이트하려면 다시 복사합니다.

### 파일

```
kouetsu/
├── .claude-plugin/
│   ├── plugin.json           # 플러그인 정보
│   └── marketplace.json      # /plugin marketplace add가 플러그인을 찾게 한다
├── skills/
│   └── kouetsu/
│       ├── SKILL.md          # 세 층과 작업 순서
│       ├── references/
│       │   ├── ko.md         # 한국어 패턴
│       │   ├── ja.md         # 일본어 패턴
│       │   └── en.md         # 영어 패턴
│       └── scripts/
│           └── surface_scan.py   # 문장과 패턴을 센다 (Python 3, 표준 라이브러리만 사용)
├── README.md, README.ko.md, README.ja.md
└── LICENSE
```

`SKILL.md`는 토큰을 덜 쓰려고 영어로 썼습니다.

## 데이터

kouetsu는 커넥터를 추가하지 않고, 네트워크 요청을 하지 않습니다. 무엇이 어디서 도는지는 다음과 같습니다.

- 스킬은 Claude에게 주는 지시문입니다. Claude는 요청을 받은 세션 안에서 글을 읽습니다.
- Claude가 점검하는 초안에 `surface_scan.py`를 돌릴 수 있습니다. Claude Code에서는 사용자 컴퓨터에서, Claude 앱에서는 코드 실행 환경에서 돕니다. 스크립트는 넘겨받은 파일만 읽고 개수를 출력합니다.
- 긴 글의 별도 검토(쓰는 법 참고)는 Claude Code에서는 같은 세션 안의 서브에이전트로 돕니다. 서브에이전트를 띄울 수 없는 곳에서는 Claude가 글을 담은 프롬프트를 드리고, 새 대화에 붙여 넣을지는 사용자가 정합니다.

## 쓰는 법

### 쓰기

평소처럼 글을 부탁하면 됩니다. 예: "이 브랜치의 PR 설명을 써줘."

쓰기 전에 Claude는 받은 재료를 보고 다섯 가지에 답합니다. 누가 읽는지, 읽고 나서 무엇을 할 수 있어야 하는지, 요점이 무엇인지, 주장에 어떤 근거가 필요한지, 이 글이 무엇을 보태는지입니다. 재료로 답할 수 없는 빈 곳은 Claude가 나눠서 처리합니다.

- 선례나 통상의 관행으로 정할 수 있으면, Claude가 정하고, 이유를 적고, 사용자가 뒤집을 수 있게 Claude의 결정이라고 표시합니다.
- 사용자의 업무 규칙·비용·사람·방침에 달린 것이면 사용자에게 맡깁니다. 맡기는 방식은 글의 길이에 따라 다릅니다.

| | 긴 글 | 짧은 글 |
|---|---|---|
| 예 | 설계서, 보고서, 제안서, 기사처럼 여러 문단이고 독자가 시간을 들여 읽는 글 | 메시지, 메일, 커밋, 짧은 답변, 한두 문단 요약 |
| 사용자에게 달린 빈 곳 | 초안 전에 Claude가 묻습니다. 한 번에 한두 가지씩 | 묻지 않고 쓰되, 빈 곳마다 `[확인 필요: 무엇]`을 글의 언어로 남기고 누가 답할 수 있는지와 무엇이 막히는지를 적습니다. 영어 글이면 `[needs confirmation: what]`입니다 |
| 개요 | 초안 전에 보여 줍니다 | 없음 |
| 별도 검토 | 있음 (아래 참고) | 없음 |

긴 글인지 짧은 글인지는 Claude가 정합니다. 바꾸고 싶으면 말하면 됩니다. 짧은 글로 다루라거나, 질문이나 별도 검토를 건너뛰라거나, 짧은 글에도 검토를 돌리라고 하면 됩니다.

### 다듬기

기존 글을 kouetsu로 다듬어 달라고 하면 됩니다. 예: "이 보고서 kouetsu로 다듬어줘." Claude는 사실관계와 필자의 목소리를 지키고, 점검에 걸린 문장만 고칩니다. 원문에 없는 행위자·수치·출처를 채워 넣지 않습니다. 긴 글이면 사용자에게 묻고, 짧은 글이면 `[확인 필요: 무엇]`으로 표시합니다.

### 진단

글을 kouetsu로 진단해 달라고 하면 됩니다. 예: "이 사양서 kouetsu로 진단해줘." Claude는 아무것도 고쳐 쓰지 않습니다. 문장에 번호(`[S1]`, `[S2]`, …)를 붙이고, 문제마다 태그를 달고, 층별로 보고하고, 결함 문장의 비율을 알려 줍니다.

| 태그 | 층 | 뜻 |
|---|---|---|
| `[blindspot]` | 내용 | 독자가 추측해야 하거나, 글이 독자에게 없는 지식을 전제한다 |
| `[inconsistent]` | 내용 | 글의 두 곳이 서로 다른 말을 한다 |
| `[actor]` | 명확성 | 누가 무엇을 하는지 문장이 감추고 있다 |
| `[vague]` | 명확성 | 어떤 말이나 숫자가 무엇을 가리키는지 독자가 알 수 없다 |
| `[empty]` | 명확성 | 지워도 잃는 것이 없다 |
| `[buried]` | 명확성 | 실패·위험·요청이 독자가 놓칠 자리에 있다 |
| `[pattern:이름]` | 표면 | 목록에 있는 상투 패턴이다 |

맹점을 찾을 때 Claude는 독자가 이 글에 가지고 올 질문을 5~10개 만들고, 글만 보고 하나씩 답해 봅니다.

줄인 예입니다. 입력:

> 로그인 흐름에 대한 개선 작업이 진행되었습니다. 이는 단순한 버그 수정이 아니라 패러다임의 전환입니다. 일부 테스트에서 이슈가 있었으나 전반적으로 양호합니다.

진단:

> 내용: 요점과 근거가 없습니다. 무엇이 바뀌었는지, 머지해도 되는지를 말하지 않습니다.
> [S1] `[actor]` `[pattern:명사화]` 누가 로그인 흐름의 무엇을 바꿨나?
> [S2] `[empty]` `[pattern:부정-대비]`
> [S3] `[buried]` `[vague]` 어느 테스트가 실패했고, 그것이 머지를 막나?
> 결함 문장: 3개 중 3개.

### 긴 글의 별도 검토

쓴 사람은 자기 글의 모순을 놓치고, 이미 알고 있어서 글에서 빠진 것도 보지 못합니다. 그래서 긴 글이면 두 번째 독자가 완성된 글을 점검합니다. 두 번째 독자는 글과, 대상 독자를 설명한 한 줄만 받고, `[inconsistent]`와 `[blindspot]`을 보고합니다. 그러면 Claude가 고칩니다.

- Claude Code에서는 Claude가 두 번째 독자를 서브에이전트로 돌립니다.
- 서브에이전트를 띄울 수 없는 곳에서는(환경에 따라 다릅니다) Claude가 새 대화에 붙여 넣을 프롬프트를 드리고, 사용자가 결과를 가져옵니다.

글을 한 번 더 읽고 보고서를 쓰는 만큼의 비용이 듭니다. 별도 검토를 하지 못했으면 Claude가 글을 넘길 때 그렇게 밝힙니다.

### 패턴 세기

모델은 눈으로 세면 자주 틀립니다. 코드를 실행할 수 있는 곳에서는 Claude가 `surface_scan.py`로 패턴, 굵은 글씨, 제목을 셉니다. 스크립트에는 Python 3이 필요합니다. Claude Code에서는 사용자 컴퓨터에 Python이 있어야 하고, Claude 앱에서는 코드 실행 환경에서 돕니다. 스크립트를 돌릴 수 없으면 Claude가 패턴을 하나씩 검색해서 셉니다.

직접 돌릴 수도 있습니다.

```bash
python3 skills/kouetsu/scripts/surface_scan.py draft.md            # 개수를 세고, 두 번 넘게 나온 패턴에 표시
python3 skills/kouetsu/scripts/surface_scan.py draft.md --number   # 진단용으로 [S1], [S2], ... 을 붙여 출력
```

스크립트는 글자를 보고 언어를 추정합니다. 직접 정하려면 `--lang ko`, `--lang ja`, `--lang en`을 씁니다. 그 밖의 언어에는 영어 목록을 쓰므로, 문장·굵은 글씨·제목의 개수만 참고하세요. 스크립트는 개수만 보고합니다. 많이 나왔다는 것은 살펴볼 이유이지 판정이 아닙니다.

## 항상 적용하려면

스킬은 Claude가 글을 쓰거나 검토하는 작업이라고 판단할 때만 불려 옵니다. Claude Code의 작업 보고처럼 매번 나오는 글에도 적용하려면, Claude가 항상 읽는 곳에 핵심 규칙을 적어 둡니다. Claude Code에서는 `CLAUDE.md`, Claude 앱에서는 프로젝트 지침입니다.

```markdown
## Writing
- Put the conclusion, result, or request in the first sentence.
- Name the actor in every sentence. Replace pointers and labels coined during the work with real names.
- Separate what was verified from what was not.
- Delete sentences that carry no information.
```

규칙이 영어여도 어느 언어의 출력에든 적용됩니다. 옮겨 적어도 됩니다.

## 한계

- 이 점검은 하한선입니다. 통과했다고 좋은 글이 되지는 않습니다.
- 표면 패턴만 지우면 알아보기 어려운 슬롭이 될 뿐입니다. 내용과 명확성을 먼저 고칩니다.
- 글을 책임지는 것은 내보내는 사람입니다. 스킬은 그 사람이 판단할 지점을 보여 줄 뿐, 판단을 대신하지 않습니다.

## 라이선스

MIT. [LICENSE](LICENSE)를 보세요.

## 참고한 글

- [Why AI slop is hard to read](https://zonderlabs.com/slop) (Zonder Labs): 명확성의 세 가지 결함
- [No AI Slop: A Manifesto](https://www.slopmanifesto.com/) (AIE Code Summit 2026): 책임과 검토 비용
- [How we use AI without making AI slop](https://ahrefs.com/blog/how-we-use-ai-without-making-ai-slop/) (Ahrefs): 쓰기 전에 정할 다섯 가지
- [I'm becoming AI blind](https://cymerys.com/w/im-becoming-ai-blind) (cymerys): 독자가 글을 건너뛰게 되는 과정
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing): 징후는 문제 자체가 아니라는 관점
- [doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) (Anthropic): 맥락 없는 독자로 문서를 시험하는 방법
