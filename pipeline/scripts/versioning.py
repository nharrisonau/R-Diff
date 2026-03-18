#!/usr/bin/env python3
from __future__ import annotations

import dataclasses
import re
from typing import Iterable


_PRERELEASE_STAGE_ORDER = {
    "alpha": 0,
    "beta": 1,
    "rc": 2,
    "pre": 3,
    "preview": 3,
}


@dataclasses.dataclass(frozen=True)
class ParsedVersion:
    raw: str
    scheme: str
    tokens: tuple[int, ...]
    is_prerelease: bool
    prerelease_stage: str
    prerelease_num: int
    suffix: str

    @property
    def key(self) -> tuple:
        """
        Comparable key, where bigger means newer.

        Ordering rules:
        - Compare numeric tokens left-to-right.
        - For equal numeric tokens:
          - final release > prerelease (alpha/beta/rc).
          - prerelease stage order: alpha < beta < rc.
          - prerelease numeric suffix increases with recency (beta2 > beta1).
          - For stable versions with letter suffix (e.g., 1.3.3c), compare suffix.
        """
        final_flag = 0 if self.is_prerelease else 1
        stage_order = _PRERELEASE_STAGE_ORDER.get(self.prerelease_stage, -1)
        return self.tokens + (final_flag, stage_order, self.prerelease_num, self.suffix)

    def major_token(self, index: int) -> int | None:
        if index < 0 or index >= len(self.tokens):
            return None
        return self.tokens[index]


def _split_prerelease(value: str) -> tuple[str, str, int, bool]:
    """
    Split prerelease markers from the tail of a version string.

    Supports forms like:
      - 2.9.9-rc1
      - 4.7.1rc2
      - 1.7.0beta85
      - 3.0.0-beta2
    """
    v = (value or "").strip()
    if not v:
        return "", "", 0, False

    m = re.search(r"(?i)(?:[-._]?)(alpha|beta|rc|pre|preview)(\d*)$", v)
    if not m:
        return v, "", 0, False

    stage = (m.group(1) or "").lower()
    num_s = (m.group(2) or "").strip()
    num = int(num_s) if num_s.isdigit() else 0
    base = v[: m.start()]
    base = base.rstrip("-._")
    return base, stage, num, True


def _split_trailing_letter_suffix(value: str) -> tuple[str, str]:
    """
    Handle stable versions like '1.3.3c' (not a prerelease).

    Returns (base, suffix).
    """
    v = (value or "").strip()
    if not v:
        return "", ""
    suffix_chars = []
    for ch in reversed(v):
        if ch.isalpha():
            suffix_chars.append(ch)
        else:
            break
    if not suffix_chars:
        return v, ""
    suffix = "".join(reversed(suffix_chars))
    base = v[: -len(suffix)]
    if not re.search(r"\d", base):
        return v, ""
    return base, suffix


def _parse_numeric_tokens(value: str) -> tuple[int, ...]:
    nums = [int(x) for x in re.findall(r"\d+", value or "")]
    return tuple(nums)


def normalize_version(value: str, scheme: str) -> str:
    v = (value or "").strip()
    if scheme == "sudo":
        return v.replace("_", ".")
    return v


def parse_version(value: str, scheme: str) -> ParsedVersion:
    v = normalize_version(value, scheme)

    if scheme == "dropbear_year":
        tokens = _parse_numeric_tokens(v)
        if len(tokens) < 2:
            raise ValueError(f"invalid dropbear version: {value!r}")
        return ParsedVersion(
            raw=v,
            scheme=scheme,
            tokens=tokens,
            is_prerelease=False,
            prerelease_stage="",
            prerelease_num=0,
            suffix="",
        )

    if scheme == "sudo":
        # Expect A.B.C[pN] where pN is optional.
        m = re.match(r"^(?P<a>\d+)\.(?P<b>\d+)\.(?P<c>\d+)(?:p(?P<p>\d+))?$", v)
        if not m:
            raise ValueError(f"invalid sudo version: {value!r}")
        a = int(m.group("a"))
        b = int(m.group("b"))
        c = int(m.group("c"))
        p = int(m.group("p") or "0")
        return ParsedVersion(
            raw=v,
            scheme=scheme,
            tokens=(a, b, c, p),
            is_prerelease=False,
            prerelease_stage="",
            prerelease_num=0,
            suffix="",
        )

    # semver-ish and openssl: share the same tokenization; prereleases are included
    # only if the caller wants them.
    base, stage, num, is_pre = _split_prerelease(v)
    base, suffix = _split_trailing_letter_suffix(base)
    tokens = _parse_numeric_tokens(base)
    if not tokens:
        raise ValueError(f"invalid version: {value!r}")
    return ParsedVersion(
        raw=v,
        scheme=scheme,
        tokens=tokens,
        is_prerelease=is_pre,
        prerelease_stage=stage,
        prerelease_num=num,
        suffix=suffix,
    )


def choose_tag_for_version(
    existing_tag: str | None, candidate_tag: str, *, prefer_shortest: bool = True
) -> str:
    if not existing_tag:
        return candidate_tag
    if prefer_shortest:
        if len(candidate_tag) < len(existing_tag):
            return candidate_tag
        if len(candidate_tag) > len(existing_tag):
            return existing_tag
    return min(existing_tag, candidate_tag)


def extract_versions_from_tags(
    tags: Iterable[str], patterns: Iterable[re.Pattern], scheme: str
) -> dict[str, str]:
    """
    Return mapping: normalized_version -> chosen_tag
    """
    out: dict[str, str] = {}
    for tag in tags:
        tag = (tag or "").strip()
        if not tag:
            continue
        ver_raw = None
        for pat in patterns:
            m = pat.match(tag)
            if not m:
                continue
            ver_raw = m.group("version")
            break
        if not ver_raw:
            continue
        ver_norm = normalize_version(ver_raw, scheme)
        # Ensure it's parseable for ordering/major token selection
        try:
            _ = parse_version(ver_norm, scheme)
        except Exception:
            continue
        out[ver_norm] = choose_tag_for_version(out.get(ver_norm), tag)
    return out


def sanitize_component(value: str) -> str:
    """Make a safe directory component for previous versions."""
    v = (value or "").strip()
    return re.sub(r"[^A-Za-z0-9._-]+", "_", v) or "unknown"

