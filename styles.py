"""Font engines, frames, lookalikes, and catalog builder."""
from __future__ import annotations

from extra_styles import EXTRA_WRAPS, PREFIXES, SUFFIXES, lookalike_fonts
from fonts import CAT_STYLES, FRAMES, framed, style_text
from nick_styles import build_all as pack_build

CATEGORIES = ("all", "cute", "royal", "dark", "gaming", "aesthetic", "nature")

CAT_LABELS = {
    "all": "All",
    "cute": "Cute",
    "royal": "Royal",
    "dark": "Dark",
    "gaming": "Gaming",
    "aesthetic": "Aesthetic",
    "nature": "Nature",
}


def _clean(name: str, limit: int = 24) -> str:
    return (name or "").strip()[:limit] or "Name"


def _unique(seq: list[str]) -> list[str]:
    out, seen = [], set()
    for raw in seq:
        text = str(raw)
        if "\n" not in text:
            text = " ".join(text.split())
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def build_catalog(name: str, category: str = "all") -> list[str]:
    name = _clean(name)
    category = category if category in CAT_STYLES else "all"
    items: list[str] = []

    if category == "all":
        items.extend(pack_build(name))
        for extra in lookalike_fonts(name):
            items.append(extra)
            items.append(f"\u2605 {extra} \u2605")
        core = items[:8] or [name]
        for wrap in EXTRA_WRAPS:
            if "{n}" not in wrap:
                continue
            for inner in core[:3]:
                items.append(wrap.replace("{n}", inner))
        for i, pre in enumerate(PREFIXES):
            suf = SUFFIXES[i % len(SUFFIXES)]
            items.append(f"{pre} {core[i % len(core)]} {suf}")
    else:
        styles = CAT_STYLES.get(category, CAT_STYLES["all"])
        frames = list(FRAMES)
        for style in styles:
            styled = style_text(name, style)
            items.append(styled)
            for frame in frames:
                items.append(framed(styled, frame))
        for extra in lookalike_fonts(name)[:6]:
            items.append(extra)

    boxed = [x for x in items if "\n" in x]
    rest = [x for x in items if "\n" not in x]
    return _unique(boxed + rest)


def build_preview(name: str, limit: int = 50) -> list[str]:
    return build_catalog(name, "all")[:limit]
