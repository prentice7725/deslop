#!/usr/bin/env python3
"""kouetsu 3층(표면) 점검용 스캐너.

LLM이 눈으로 세면 틀리기 쉬운 것을 기계적으로 센다.
- 문장 수와 문장 번호([S1], [S2] ...)
- 언어별 상투 패턴의 등장 횟수와 위치
- 굵은 글씨, 제목 수
- 문장·문단 길이의 편차(균일한 리듬 탐지용)

표준 라이브러리만 쓴다. 판정은 하지 않는다. 숫자를 보고 고칠지 정하는 것은 사람이나 모델의 몫이다.

사용법:
    python3 surface_scan.py FILE [--lang ko|ja|en] [--number] [--threshold N]

    --lang       글의 언어. 생략하면 문자 비율로 추정한다.
    --number     패턴 집계 대신, 문장마다 [S번호]를 붙인 본문을 출력한다(진단 모드용).
    --threshold  이 횟수를 넘는 패턴에 표시를 붙인다. 기본값 2.
"""

import argparse
import re
import statistics
import sys

# 언어별 패턴. 각 항목은 (이름, 정규식). references/*.md의 항목과 대응한다.
PATTERNS = {
    "ko": [
        ("명사화(~에 대한/~를 통해/~함으로써)", r"에 대한|[을를] 통해|함으로써"),
        ("~을/를 진행했다", r"[을를] 진행(했|하|합|한)"),
        ("~할 수 있습니다", r"할 수 있습니다"),
        ("흐린 종결(~라고 할 수 있/~것으로 보입니다)", r"라고 할 수 있|것으로 보입니다"),
        ("빈 수식어", r"다양한|효과적인|체계적인|혁신적인|핵심적인"),
        ("안내 문장", r"살펴보겠습니다|정리하면 다음과 같습니다|결론적으로"),
        ("부정-대비(~가 아니라/~를 넘어)", r"단순한 \S+[이가] 아니라|[을를] 넘어"),
        ("조사 연쇄(~의 ~의)", r"\S+의 \S+의 "),
    ],
    "ja": [
        ("「〜を行う」", r"を行[ういっわ]"),
        ("「〜における」", r"における"),
        ("「〜することができ」", r"することができ"),
        ("ぼかした文末", r"と言えるでしょう|と考えられ|かもしれ"),
        ("空の修飾語", r"さまざまな|様々な|多岐にわたる|効果的な|重要な役割"),
        ("案内文", r"見ていきましょう|まとめると|結論として|いかがでしたか"),
        ("否定対比(ではなく/だけでなく)", r"ではなく|だけでなく"),
        ("敬語の重ね(させていただ)", r"させていただ"),
        ("「〜になります」", r"になります"),
    ],
    "en": [
        ("Nominalization", r"\bperform(ed|s|ing)? an? \w+ of\b|\bcarried out\b"),
        ("Agentless passive (it was decided)", r"\bit was (decided|determined|agreed)\b"),
        ("Negative parallelism", r"\bnot (just|only|merely) \w+|\bit'?s not \w+, it'?s\b"),
        ("Significance claims", r"crucial role|testament to|pivotal|game[- ]changer"),
        ("Trailing -ing clause", r", (highlighting|ensuring|underscoring|showcasing|reflecting)\b"),
        ("Signposting", r"let'?s dive|here'?s the thing|worth noting|in conclusion"),
        ("Stacked hedges", r"\bmay potentially\b|\bcould possibly\b"),
        ("Stock vocabulary", r"\bdelve|\blandscape\b|\brobust\b|\bseamless|\bleverag|fast-paced world"),
        ("Chat residue", r"great question|hope this helps|let me know if"),
    ],
}

# 언어와 관계없이 세는 서식
FORMAT_PATTERNS = [
    ("bold (**)", r"\*\*[^*\n]+\*\*"),
]


def guess_lang(text):
    """한글·가나 비율로 언어를 추정한다."""
    hangul = len(re.findall(r"[가-힣]", text))
    kana = len(re.findall(r"[ぁ-んァ-ン]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if hangul >= kana and hangul > latin * 0.2:
        return "ko"
    if kana > hangul and kana > latin * 0.1:
        return "ja"
    return "en"


def text_lines(text, tables=False):
    """코드 블록을 뺀 줄을 (줄 번호, 내용)으로 돌려준다. tables=False면 표도 뺀다."""
    out = []
    in_code = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or (not tables and line.lstrip().startswith("|")):
            continue
        out.append((i, line))
    return out


def split_sentences(line):
    """한 줄을 문장으로 나눈다. 마침표류 뒤에서 자른다."""
    body = re.sub(r"^\s*([-*+]|\d+\.)\s+", "", line).strip()
    if not body or body.startswith("#"):
        return []
    # 링크가 둘 이상이고 | 로 나뉜 줄(언어 전환 링크 등)은 문장으로 세지 않는다
    if "|" in body and len(re.findall(r"\[[^\]]*\]\([^)]*\)", body)) >= 2:
        return []
    parts = re.split(r"(?<=[。！？])|(?<=[.!?])\s+(?=\S)", body)
    return [p.strip() for p in parts if p and p.strip()]


def scan(text, lang, threshold):
    lines = text_lines(text)
    # 패턴은 표 안의 글까지 센다. 문장 수와 길이는 표를 뺀 본문만으로 잰다.
    all_lines = text_lines(text, tables=True)
    sentences = [(n, s) for n, l in lines for s in split_sentences(l)]
    headings = sum(1 for _, l in lines if l.lstrip().startswith("#"))

    print(f"language: {lang}")
    print(f"sentences (prose, tables excluded): {len(sentences)}  headings: {headings}")

    # 문장 길이와 문단 길이의 편차. 변동계수가 낮으면 리듬이 균일하다.
    lens = [len(s) for _, s in sentences]
    if len(lens) >= 2:
        cv = statistics.pstdev(lens) / statistics.mean(lens)
        print(f"sentence length: mean {statistics.mean(lens):.0f}, cv {cv:.2f}")
    paras, cur = [], 0
    for _, l in lines:
        if l.strip() and not l.lstrip().startswith("#"):
            cur += len(l)
        elif cur:
            paras.append(cur)
            cur = 0
    if cur:
        paras.append(cur)
    if len(paras) >= 3:
        pcv = statistics.pstdev(paras) / statistics.mean(paras)
        print(f"paragraph length: {len(paras)} paragraphs, cv {pcv:.2f}")

    print()
    print(f"patterns (flag: more than {threshold})")
    for name, rx in PATTERNS[lang] + FORMAT_PATTERNS:
        hits = [(n, m.group(0)) for n, l in all_lines for m in re.finditer(rx, l, re.IGNORECASE)]
        if not hits:
            continue
        flag = "  <-- fix" if len(hits) > threshold else ""
        where = ", ".join(f"L{n}" for n, _ in hits[:8])
        more = " ..." if len(hits) > 8 else ""
        print(f"  {len(hits):3d}  {name}  [{where}{more}]{flag}")


def number(text):
    """진단 모드용: 본문 문장에 [S번호]를 붙여 출력한다. 표와 코드는 그대로 둔다."""
    k = 0
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            print(line)
            continue
        if in_code or line.lstrip().startswith("|") or line.lstrip().startswith("#"):
            print(line)
            continue
        sents = split_sentences(line)
        if not sents:
            print(line)
            continue
        prefix = re.match(r"^\s*([-*+]|\d+\.)?\s*", line).group(0)
        tagged = []
        for s in sents:
            k += 1
            tagged.append(f"[S{k}] {s}")
        print(prefix + " ".join(tagged))
    print(f"\n(total sentences: {k})")


def main():
    ap = argparse.ArgumentParser(description="kouetsu surface scan")
    ap.add_argument("file")
    ap.add_argument("--lang", choices=sorted(PATTERNS))
    ap.add_argument("--number", action="store_true")
    ap.add_argument("--threshold", type=int, default=2)
    a = ap.parse_args()
    with open(a.file, encoding="utf-8") as f:
        text = f.read()
    if a.number:
        number(text)
    else:
        scan(text, a.lang or guess_lang(text), a.threshold)


if __name__ == "__main__":
    sys.exit(main())
