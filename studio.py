"""Local premium wraps / prefixes / suffixes. No third-party API."""
from __future__ import annotations

try:
    from fonts import ENGINES, style_text
except ImportError:
    def _math(low_a, up_a):
        def conv(text):
            out = []
            for ch in text:
                if "a" <= ch <= "z":
                    out.append(chr(low_a + ord(ch) - 97))
                elif "A" <= ch <= "Z":
                    out.append(chr(up_a + ord(ch) - 65))
                else:
                    out.append(ch)
            return "".join(out)
        return conv
    ENGINES = {
        "bold": _math(0x1D41A, 0x1D400),
        "italic": _math(0x1D44E, 0x1D434),
        "script": _math(0x1D4B6, 0x1D49C),
        "boldscript": _math(0x1D4EA, 0x1D4D0),
        "mono": _math(0x1D68A, 0x1D670),
        "double": _math(0x1D552, 0x1D538),
        "smallcaps": lambda t: t,
        "fraktur": _math(0x1D51E, 0x1D504),
    }
    def style_text(text, style):
        return ENGINES.get(style, ENGINES["bold"])(text or "")

PREMIUM_WRAPS = [
    "\u2022 {n} \U0001F9FF",
    "\u2629{n}\U0001F525",
    "\u3010 {n} \u3011",
    "\u300e {n} \u300f",
    "\u2605 {n} \u2605",
    "\u2661 {n} \u2661",
    "\u265b {n} \u265b",
    "\U0001F525 {n} \U0001F525",
    "\U0001F48E {n} \U0001F48E",
    "\U0001F451 {n} \U0001F451",
    "\U0001F338 {n} \U0001F338",
    "\u2694 {n} \u2694",
    "\u263d {n} \u263e",
    "\u26a1 {n} \u26a1",
    "\U0001F98B {n} \U0001F98B",
]
AESTHETIC_WRAPS = [
    "\u02da {n} \u02da",
    "\u22c6 {n} \u22c6",
    "\u2661 {n} \u2661",
    "\u2601 {n} \u2601",
    "\u273f {n} \u273f",
    "\U0001F380 {n} \U0001F380",
    "\U0001F319 {n} \u2728",
]
LIVE_WRAPS = [
    "\u300e{n}\u300f",
    "\u3010{n}\u3011",
    "\u2726{n}\u2726",
    "\u26a1{n}\u26a1",
    "\U0001F525{n}\U0001F525",
    "\u265b{n}\u265b",
]
HINDI_WRAPS = [
    "\u091c\u092f {n} \U0001F6A9",
    "\u0950 {n} \u0950",
    "\U0001F64F {n} \U0001F64F",
    "\U0001F451 \u0930\u093e\u091c\u093e {n}",
    "\U0001F1EE\U0001F1F3 {n} \U0001F1EE\U0001F1F3",
]
PREFIXES = ["", "\u2629", "\u2605", "\u265b", "\u2726", "\U0001F525", "\U0001F48E", "\U0001F451"]
SUFFIXES = ["", "\U0001F525", "\u2605", "\u265b", "\U0001F9FF", "\U0001F497", "\U0001F48E", "\U0001F451"]
ORNAMENTS = ["", "\u2661", "\u2726", "\u273f", "\u26a1", "\U0001F338"]
MARKS = ["", "\u2605", "\u2728", "\U0001F4AB"]
SEPARATORS = ["", " ", " \u2022 ", " | "]
FONTS = ["bold", "italic", "script", "boldscript", "smallcaps", "mono", "double", "fraktur"]

def apply_font(name: str, font: str) -> str:
    if font in ENGINES:
        return style_text(name, font)
    return name

def compose(name: str, parts: dict) -> str:
    core = apply_font(name, parts.get("font") or "bold")
    if parts.get("spacing") == "wide":
        core = " ".join(core)
    if parts.get("underline"):
        core = "".join(ch + "\u0332" for ch in core)
    if parts.get("crown"):
        core = f"\U0001F451 {core} \U0001F451"
    chunks = [x for x in (parts.get("prefix") or "", parts.get("title") or "", core, parts.get("suffix") or "", parts.get("ornament") or "", parts.get("marks") or "") if x]
    return " ".join(chunks).replace("  ", " ").strip()

def catalog(name: str, category: str) -> list[str]:
    name = (name or "Name").strip()[:24] or "Name"
    wraps = {"premium": PREMIUM_WRAPS, "aesthetic": AESTHETIC_WRAPS, "live": LIVE_WRAPS, "hindi": HINDI_WRAPS}.get(category, PREMIUM_WRAPS)
    items = []
    fonts = list(ENGINES)[:8]
    for wrap in wraps:
        styled = apply_font(name, fonts[len(items) % len(fonts)])
        items.append(wrap.replace("{n}", styled))
    for font in fonts:
        items.append(apply_font(name, font))
    out, seen = [], set()
    for x in items:
        x = " ".join(str(x).split())
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def bios(name: str) -> list[str]:
    n = (name or "Me").strip()[:28] or "Me"
    return [f"\u2728 {n} | dreamer", f"\U0001F451 VIP \u2022 {n}", f"\U0001F338 sirf {n}", f"\U0001F525 {n} on fire", f"\U0001F1EE\U0001F1F3 {n} | desi soul", f"\U0001F48E premium {n}", f"\U0001F319 late night {n}", f"\u2694 {n} | no fear", f"\U0001F64F {n} | sanatan"]
