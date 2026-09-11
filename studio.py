"""Local premium wraps + NAME_BOTGEN formats for the editor."""
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

try:
    from nick_styles import build_all as pack_build
except ImportError:
    pack_build = None

try:
    from extra_styles import EXTRA_WRAPS, PREFIXES as XPRE, SUFFIXES as XSUF, lookalike_fonts
except ImportError:
    EXTRA_WRAPS, XPRE, XSUF = [], [], []
    def lookalike_fonts(name):
        return []

try:
    from name_formats import apply_formats
except ImportError:
    def apply_formats(name):
        return []

MEITEI = "\uA9BF"
CIRCLE = "\u20DD"
L = "\U000131a9"
R = "\U000131aa"

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
    L + " {n} " + R,
    L + "{n}" + R,
    L + " {n} \U0001F33E " + R,
    "\u25c4\u23e4 {n} \u23e4\u25ba",
    "\u272f \u23af\uabed {n} \u23af\uabed \u272f",
    "\ua9c1 {n} \ua9c2",
    "\u300e {n} \u300f",
    "\u3010 {n} \u3011",
    "\u2756 {n} \u2756",
    "\u27bb {n} \u27bb",
    "\u265b {n} \u265b",
    "\U0001F451 {n} \U0001F451",
    "\U0001F48E {n} \U0001F48E",
    "\U0001F525 {n} \U0001F525",
]
AESTHETIC_WRAPS = [
    L + " {n} " + R,
    "\u2765 {n} \u2765",
    "\u300e {n} \u300f",
    "\u2661 {n} \u2661",
    "\U0001F380 {n} \U0001F380",
    "\U0001F98B {n} \U0001F98B",
    "\U0001F90D {n} \U0001F90D",
    "\u2740 {n} \u2740",
    "\U0001FAB7 {n} \U0001FAB7",
]
LIVE_WRAPS = [
    L + "{n}" + R, "\u300e{n}\u300f", "\u3010{n}\u3011",
    "\u2726{n}\u2726", "\u26a1{n}\u26a1", "\U0001F525{n}\U0001F525",
]
HINDI_WRAPS = [
    L + " {n} " + R,
    "\u091c\u092f {n} \U0001F6A9", "\u0950 {n} \u0950",
    "\U0001F64F {n} \U0001F64F", "\U0001F451 \u0930\u093e\u091c\u093e {n}",
]
PREFIXES = ["", L, "\u25c4\u23e4", "\u272f", "\u23af\uabed", "\ua9c1", "\u2765", "\u300e", "\u3010", "\u2756", "\u27bb", "\u265b", "\U0001F451", "\U0001F525"] + list(XPRE)
SUFFIXES = ["", R, "\u23e4\u25ba", "\u272f", "\u23af\uabed", "\ua9c2", "\u2765", "\u300f", "\u3011", "\U0001F33E", "\U0001F90D", "\U0001F98B", "\U0001FAB7", "\U0001F451"] + list(XSUF)
ORNAMENTS = ["", "\u2661", "\u2726", "\u2740", "\u26a1", "\U0001F338", "\U0001F33E", "\U0001F98B", "\U0001F90D", "\U0001FAB7"]
MARKS = ["", "\u2605", "\u2728", "\U0001F4AB", "\u20DD"]
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
    bold = apply_font(raw, "bold")
    script = apply_font(raw, "script")
    items = list(apply_formats(raw))
    items += [
        f"{L} {raw} {R}",
        f"{L} {bold} {R}",
        f"{L}{bold}{R}",
        f"{L} {strike(bold)} {R}",
        f"{L} {circled(bold)} {R}",
    ]
    wraps = {"premium": PREMIUM_WRAPS, "aesthetic": AESTHETIC_WRAPS, "live": LIVE_WRAPS, "hindi": HINDI_WRAPS}.get(category, PREMIUM_WRAPS)
    fonts = list(ENGINES)
    for i, wrap in enumerate(wraps):
        items.append(wrap.replace("{n}", apply_font(raw, fonts[i % len(fonts)])))
    for wrap in EXTRA_WRAPS:
        items.append(wrap.replace("{n}", bold))
    if pack_build and category in ("premium", "aesthetic", "live"):
        try:
            items.extend(pack_build(raw))
        except Exception:
            pass
    try:
        items.extend(lookalike_fonts(raw))
    except Exception:
        pass
    for pre, suf in zip(PREFIXES[1:8], SUFFIXES[1:8]):
        items.append(f"{pre} {bold} {suf}")
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
        f"{L} {n} {R} | aesthetic",
        f"\u2728 {fancy} | dreamer \u2728",
        f"\U0001F451 VIP \u2022 {bold}",
        f"\U0001F90D nobody asked but {n} is everything",
        f"sunsets and self-love | {fancy}",
        f"\U0001F338 sirf {fancy}",
        f"\U0001F1EE\U0001F1F3 {n} | desi soul",
        f"\U0001F3B5 {fancy} x music",
        f"\U0001F9FF {strike(n)} | nazar",
        f"\u27bb {circled(bold)} hustle",
    ]
