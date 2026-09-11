"""Local premium wraps. No third-party style API."""
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

MEITEI = "\uA9BF"
CIRCLE = "\u20DD"

def apply_font(name: str, font: str) -> str:
    if font in ENGINES:
        return style_text(name, font)
    return name

def strike(name: str) -> str:
    return "".join(ch + MEITEI for ch in name if ch.strip())

def circled(name: str) -> str:
    if not name:
        return name
    return name[:-1] + name[-1] + CIRCLE

PREMIUM_WRAPS = [
    "\u256d\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u256e\n       {n}\n\u2570\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u256f",
    "\u256d\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256e\n   {n}\n\u2570\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256f",
    "\U000131aa {n} \U000131a9",
    "\U000131aa {n} \U0001F33E \U000131a9",
    "\U000131aa{n}\U000131a9",
    "\u300e {n} \u300f",
    "\u2756 {n} \u2756",
    "\u27bb {n} \u27bb",
    "\U00013209 {n} \U00013209",
    "\U00013370 {n} \U00013370",
    "\u265b {n} \u265b",
    "\u2629{n}\U0001F525",
    "\u3010 {n} \u3011",
    "\u2726 {n} \u2726",
    "\U0001F451 {n} \U0001F451",
    "\U0001F48E {n} \U0001F48E",
    "\U0001F525 {n} \U0001F525",
    "\U0001F338 {n} \U0001F338",
]
AESTHETIC_WRAPS = [
    "\U000131aa {n} \U000131a9",
    "\U000131aa {n} \U0001F33E \U000131a9",
    "\u300e {n} \u300f",
    "\u2756 {n} \u2756",
    "\u27bb {n} \u27bb",
    "\u2661 {n} \u2661",
    "\U0001F380 {n} \U0001F380",
    "\U0001F319 {n} \u2728",
    "\u02da {n} \u02da",
    "\u22c6 {n} \u22c6",
    "\u273f {n} \u273f",
    "\U0001FAE7 {n} \U0001FAE7",
    "\U0001F90D {n} \U0001F90D",
    "\u2740 {n} \u2740",
    "\u2027\u208a {n} \u208a\u2027",
]
LIVE_WRAPS = [
    "\u300e{n}\u300f", "\u3010{n}\u3011", "\u2726{n}\u2726", "\u26a1{n}\u26a1",
    "\U0001F525{n}\U0001F525", "\u265b{n}\u265b", "\U000131aa{n}\U000131a9",
    "\u27bb{n}\u27bb", "\u2756{n}\u2756", "\u2605{n}\u2605",
]
HINDI_WRAPS = [
    "\u091c\u092f {n} \U0001F6A9", "\u0950 {n} \u0950", "\U0001F64F {n} \U0001F64F",
    "\u2726 {n} \u092d\u0915\u094d\u0924 \u2726", "\u2740 {n} \u0930\u093e\u0927\u0947 \u2740",
    "\u2694\ufe0f {n} \u0938\u093f\u0902\u0939", "\U0001F451 \u0930\u093e\u091c\u093e {n}",
    "\U0001F338 {n} \u091c\u0940", "\U0001F1EE\U0001F1F3 {n} \U0001F1EE\U0001F1F3",
    "\U000131aa {n} \U000131a9",
]
PREFIXES = ["", "\u2629", "\u2605", "\u265b", "\u300e", "\U000131aa", "\u2756", "\u27bb", "\u2726", "\U0001F525", "\U0001F451"]
SUFFIXES = ["", "\U0001F525", "\u2605", "\u265b", "\u300f", "\U000131a9", "\U0001F33E", "\u2756", "\U0001F497", "\U0001F48E", "\U0001F451"]
ORNAMENTS = ["", "\u2661", "\u2726", "\u2740", "\u26a1", "\U0001F338", "\U0001F33E", "\u2756", "\U00013209"]
MARKS = ["", "\u2605", "\u2728", "\U0001F4AB"]
SEPARATORS = ["", " ", " \u2022 ", " | ", " \u2726 "]
FONTS = ["bold", "italic", "script", "boldscript", "smallcaps", "mono", "double", "fraktur"]

def compose(name: str, parts: dict) -> str:
    core = apply_font(name, parts.get("font") or "bold")
    if parts.get("spacing") == "wide":
        core = " ".join(core)
    if parts.get("underline"):
        core = strike(core)
    if parts.get("crown"):
        core = f"\U0001F451 {core} \U0001F451"
    chunks = [x for x in (parts.get("prefix") or "", parts.get("title") or "", core, parts.get("suffix") or "", parts.get("ornament") or "", parts.get("marks") or "") if x]
    return " ".join(chunks).replace("  ", " ").strip()

def catalog(name: str, category: str) -> list[str]:
    raw = (name or "Name").strip()[:24] or "Name"
    wraps = {"premium": PREMIUM_WRAPS, "aesthetic": AESTHETIC_WRAPS, "live": LIVE_WRAPS, "hindi": HINDI_WRAPS}.get(category, PREMIUM_WRAPS)
    fonts = list(ENGINES)
    items = []
    for i, wrap in enumerate(wraps):
        styled = apply_font(raw, fonts[i % len(fonts)])
        items.append(wrap.replace("{n}", styled))
    items.append("\U000131aa " + strike(apply_font(raw, "bold")) + " \U000131a9")
    items.append("\U000131aa " + circled(apply_font(raw, "bold")) + " \U000131a9")
    items.append("\u300e " + strike(raw) + " \u300f")
    items.append("\u2756 " + circled(apply_font(raw, "script")) + " \u2756")
    items.append("\u27bb " + strike(apply_font(raw, "italic")) + " \U0001F33E")
    items.append("\U00013209 " + apply_font(raw, "fraktur") + " \U00013209")
    for font in fonts:
        items.append(apply_font(raw, font))
    out, seen = [], set()
    for x in items:
        x = str(x).strip()
        if "\n" not in x:
            x = " ".join(x.split())
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def bios(name: str) -> list[str]:
    n = (name or "Me").strip()[:28] or "Me"
    fancy = apply_font(n, "script")
    bold = apply_font(n, "bold")
    return [
        f"\u2728 {fancy} | dreamer \u2728",
        f"\U0001F451 VIP \u2022 {bold} \U0001F451",
        f"\U000131aa {n} \U000131a9 | aesthetic",
        f"\U0001F338 sirf {fancy} \U0001F338",
        f"\U0001F525 {bold} on fire \U0001F525",
        f"\U0001F1EE\U0001F1F3 {n} | desi soul",
        f"\U0001F48E premium {fancy}",
        f"\U0001F319 late night {n}",
        f"\U0001F64F {n} | sanatan",
        f"\U0001F3B5 {fancy} x music",
        f"\U0001F9FF {strike(n)} | nazar",
        f"\u27bb {circled(bold)} hustle",
    ]
