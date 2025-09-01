#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PF2e Feats Conversion From FVTT (Python)
---------------------------------------
입력:  feat.json (객체 또는 배열)
출력:  feat_converted.json

필드 매핑 규칙
    id ← _id
    name
    type
    actionType ← system.actionType.value
    actionCost ← system.actions.value (숫자면 "1 action"/"2 actions"/… 형식으로 변환, 그 외는 원문 보존)
    level ← system.level.value
    traits.rarity ← system.traits.rarity
    traits.values ← system.traits.value[]
    prerequisites[] ← system.prerequisites.value[].value
    source ← system.publication.title
    description ← system.description.value  →  (HTML → 텍스트 규칙 적용)

설명(description) 변환 규칙
    • UUID 치환
        @UUID[...] {텍스트} → 텍스트
        단독 @UUID[...] (또는 {…} 포함) → 제거
    • 기타 토큰 보존: @Damage[...], @Template[...] 등은 원문 그대로 유지
    • 강조 태그 치환: <strong>…</strong>, <b>…</b> → 내부 텍스트를 대문자 + 콜론(예: TRIGGER:)
    • HTML 제거/치환
        <br> → 줄바꿈, <hr> → --- (앞뒤 줄바꿈)
        블록 태그(<p>, <div>, <li>, <h1-6>, <table> 등) → 줄바꿈
        나머지 태그는 제거
    • 공백 정리
        탭→공백, 연속 공백 축소, 3개↑ 연속 개행→2개, 각 라인 트림 후 전체 트림

사용법
    $ python pf2e_fvtt_feat_converter.py            # feat.json → feat_converted.json
    $ python pf2e_fvtt_feat_converter.py --in in.json --out out.json
"""

from __future__ import annotations
import json
import re
import argparse
from html import unescape
from typing import Any, Dict, List, Union

# ------------------------------ 유틸리티 ------------------------------


def dig(obj: Any, path: str, default: Any = None) -> Any:
    cur = obj
    for key in path.split('.'):
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur

# --------------------------- description 처리 ---------------------------


# @UUID[...]{텍스트} → 텍스트
UUID_WITH_LABEL = re.compile(r"@UUID\[[^\]]+\]\{([^}]+)\}")
# 단독 @UUID[...] (뒤에 {..} 있을 수도 있음) → 제거
UUID_ALONE = re.compile(r"@UUID\[[^\]]+\](?:\{[^}]*\})?")

# <strong>/<b> 치환을 위해 태그 내부 텍스트만 뽑아 대문자+콜론으로
STRONG_OR_B = re.compile(
    r"<(strong|b)(?:\s+[^>]*)?>([\s\S]*?)</\1>", re.IGNORECASE)

# 블록 태그 목록 (열림/닫힘 모두 줄바꿈으로 치환)
BLOCK_TAGS = [
    'p', 'div', 'section', 'article', 'header', 'footer', 'aside',
    'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre'
]

BR_TAG = re.compile(r"<br\s*/?>", re.IGNORECASE)
HR_TAG = re.compile(r"<hr\s*/?>", re.IGNORECASE)

# 남은 태그 제거 (보존 토큰은 그대로 두지만, 태그 형태는 삭제)
ANY_TAG = re.compile(r"<[^>]+>")


def strip_all_tags(s: str) -> str:
    s = BR_TAG.sub("\n", s)
    s = HR_TAG.sub("\n---\n", s)
    s = ANY_TAG.sub("", s)
    return s


def transform_description(html: Any) -> str:
    if html is None:
        return ""
    s = str(html)

    # 1) UUID 치환
    s = UUID_WITH_LABEL.sub(lambda m: m.group(1), s)
    s = UUID_ALONE.sub("", s)

    # 2) 강조 태그: 내부 텍스트 → 대문자 + 콜론
    def _strong_to_label(m: re.Match) -> str:
        inner = strip_all_tags(m.group(2)).strip()
        return (inner.upper() + ":") if inner else ""
    s = STRONG_OR_B.sub(_strong_to_label, s)

    # 3) 줄바꿈/블록 처리
    s = BR_TAG.sub("\n", s)
    s = HR_TAG.sub("\n---\n", s)
    for tag in BLOCK_TAGS:
        s = re.sub(fr"<{tag}[^>]*>", "\n", s, flags=re.IGNORECASE)
        s = re.sub(fr"</{tag}>", "\n", s, flags=re.IGNORECASE)

    # 4) 남은 태그 제거
    s = ANY_TAG.sub("", s)

    # 5) HTML 엔티티 디코드
    s = unescape(s)

    # 6) 공백 정리
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"\t+", " ", s)                  # 탭 → 공백
    s = re.sub(r"[ \u00A0]{2,}", " ", s)          # 연속 공백 축소
    s = re.sub(r"\n{3,}", "\n\n", s)            # 3개 이상 연속 개행 → 2개
    s = "\n".join(line.strip() for line in s.split("\n"))  # 각 라인 트림
    s = s.strip()                                    # 전체 트림
    return s

# ----------------------------- 메인 변환기 -----------------------------


def normalize_action_cost(v: Any) -> Union[str, None]:
    if v is None:
        return None
    try:
        n = int(v)
        return f"{n} action" + ("s" if n != 1 else "")
    except (ValueError, TypeError):
        return str(v)


def extract_prerequisites(arr: Any) -> List[str]:
    if not isinstance(arr, list):
        return []
    out: List[str] = []
    for x in arr:
        if isinstance(x, dict):
            val = x.get('value')
        else:
            val = x
        if isinstance(val, str):
            t = val.strip()
            if t:
                out.append(t)
    return out


def convert_feat(f: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": f.get("_id"),
        "name": f.get("name"),
        "type": f.get("type"),
        "actionType": dig(f, "system.actionType.value"),
        "actionCost": normalize_action_cost(dig(f, "system.actions.value")),
        "level": dig(f, "system.level.value"),
        "traits": {
            "rarity": dig(f, "system.traits.rarity"),
            "values": dig(f, "system.traits.value", []) if isinstance(dig(f, "system.traits.value", []), list) else [],
        },
        "prerequisites": extract_prerequisites(dig(f, "system.prerequisites.value", [])),
        "source": dig(f, "system.publication.title"),
        "description": transform_description(dig(f, "system.description.value", "")),
    }


def convert(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    if isinstance(data, list):
        return [convert_feat(x) for x in data]
    elif isinstance(data, dict):
        return convert_feat(data)
    else:
        raise TypeError("Input JSON must be an object or an array of objects.")


# ------------------------------- CLI 진입 -------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description="PF2e FVTT Feat JSON converter")
    ap.add_argument("--in", dest="inp", default="Resource/feats.json",
                    help="입력 JSON 파일 (기본: feat.json)")
    ap.add_argument("--out", dest="out", default="Resource/feats_converted.json",
                    help="출력 JSON 파일 (기본: feat_converted.json)")
    args = ap.parse_args()

    with open(args.inp, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = convert(data)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"완료: {args.inp} → {args.out}")


if __name__ == "__main__":
    main()
