from __future__ import annotations
import random
from typing import Callable

CATEGORIES = ("all", "cute", "royal", "dark", "gaming", "aesthetic", "nature")

FRAMES = {
    "none": ("", ""),
    "royal": ("\u0d7d\u0f12 ", " \u0f12\u0d7e"),
    "star": ("\u2726 ", " \u2726"),
    "heart": ("\u2661 ", " \u2661"),
    "crown": ("\U0001F451 ", " \U0001F451"),
    "game": ("\u00d7\u035c\u00d7 ", " \u4e97"),
    "cute": ("\u2729 ", " \u2729"),
    "dark": ("\u2620 ", " \u2620"),
    "brack": ("\u3010", "\u3011"),
    "fire": ("\U0001F525 ", " \U0001F525"),
    "flower": ("\u2740 ", " \u2740"),
    "moon": ("\u263e ", " \u263d"),
    "wing": ("\u0f3a ", " \u0f3b"),
    "bolt": ("\u26a1 ", " \u26a1"),
    "leaf": ("\U0001F33F ", " \U0001F33F"),
    "music": ("\u266a ", " \u266b"),
}
# fix royal frame to intended glyphs
FRAMES["royal"] = ("\ua49d\u0f12 ", " \u0f12\ua49e")

CAT_STYLES = {
    "cute": ["script", "boldscript", "italic", "smallcaps", "circled", "tiny", "cursive2"],
    "royal": ["bold", "double", "script", "boldscript", "fraktur", "smallcaps", "fullwidth"],
    "dark": ["bold", "fraktur", "mono", "fullwidth", "striked", "inverted"],
    "gaming": ["mono", "fullwidth", "circled", "squared", "bold", "wide", "cjk"],
    "aesthetic": ["italic", "script", "smallcaps", "double", "tiny"],
    "nature": ["script", "italic", "smallcaps", "tiny", "cursive2"],
    "all": ["bold", "italic", "bolditalic", "sans", "sansbold", "script", "boldscript", "double", "mono", "fraktur", "smallcaps", "fullwidth", "circled", "squared", "tiny", "cjk", "striked", "wide", "cursive2", "inverted"],
}

def _math(low_a, up_a, digit_0=None):
    def conv(text):
        out = []
        for ch in text:
            if "a" <= ch <= "z":
                out.append(chr(low_a + ord(ch) - 97))
            elif "A" <= ch <= "Z":
                out.append(chr(up_a + ord(ch) - 65))
            elif digit_0 is not None and "0" <= ch <= "9":
                out.append(chr(digit_0 + ord(ch) - 48))
            else:
                out.append(ch)
        return "".join(out)
    return conv

def _map_font(mapping):
    def conv(text):
        return "".join(mapping.get(ch, mapping.get(ch.lower(), ch)) for ch in text)
    return conv

SMALL = {"a":"\u1d00","b":"\u0299","c":"\u1d04","d":"\u1d05","e":"\u1d07","f":"\u0493","g":"\u0262","h":"\u029c","i":"\u026a","j":"\u1d0a","k":"\u1d0b","l":"\u029f","m":"\u1d0d","n":"\u0274","o":"\u1d0f","p":"\u1d18","q":"\u01eb","r":"\u0280","s":"s","t":"\u1d1b","u":"\u1d1c","v":"\u1d20","w":"\u1d21","x":"x","y":"\u028f","z":"\u1d22"}
TINY = {"a":"\u1d43","b":"\u1d47","c":"\u1d9c","d":"\u1d48","e":"\u1d49","f":"\u1da0","g":"\u1d4d","h":"\u02b0","i":"\u2071","j":"\u02b2","k":"\u1d4f","l":"\u02e1","m":"\u1d50","n":"\u207f","o":"\u1d52","p":"\u1d56","q":"q","r":"\u02b3","s":"\u02e2","t":"\u1d57","u":"\u1d58","v":"\u1d5b","w":"\u02b7","x":"\u02e3","y":"\u02b8","z":"\u1dbb"}
CJK = {"a":"\uff71","b":"\u4e43","c":"\u110c","d":"\u308a","e":"\u4e47","f":"\uff77","g":"\u30e0","h":"\u3093","i":"\uff89","j":"\uff8c","k":"\u30ba","l":"\uff9a","m":"\uffb6","n":"\u5200","o":"\u306e","p":"\uff71","q":"\u3090","r":"\u5c3a","s":"\u4e02","t":"\uff72","u":"\u3072","v":"\u221a","w":"\uff92","x":"\uff92","y":"\uff98","z":"\u4e59"}
CURSIVE2 = {"a":"\U0001d4b6","b":"\U0001d4b7","c":"\U0001d4b8","d":"\U0001d4b9","e":"\u212f","f":"\U0001d4bb","g":"\u210a","h":"\U0001d4bd","i":"\U0001d4be","j":"\U0001d4bf","k":"\U0001d4c0","l":"\U0001d4c1","m":"\U0001d4c2","n":"\U0001d4c3","o":"\u2134","p":"\U0001d4c5","q":"\U0001d4c6","r":"\U0001d4c7","s":"\U0001d4c8","t":"\U0001d4c9","u":"\U0001d4ca","v":"\U0001d4cb","w":"\U0001d4cc","x":"\U0001d4cd","y":"\U0001d4ce","z":"\U0001d4cf"}
INVERTED = {"a":"\u0250","b":"q","c":"\u0254","d":"p","e":"\u01dd","f":"\u025f","g":"\u0183","h":"\u0265","i":"\u1d09","j":"\u027e","k":"\u029e","l":"l","m":"\u026f","n":"u","o":"o","p":"d","q":"b","r":"\u0279","s":"s","t":"\u0287","u":"n","v":"\u028c","w":"\u028d","x":"x","y":"\u028e","z":"z"}
CIRCLED = {**{chr(97+i): chr(0x24D0+i) for i in range(26)}, **{chr(65+i): chr(0x24B6+i) for i in range(26)}}
SQUARED = {chr(65+i): chr(0x1F130+i) for i in range(26)}
SQUARED.update({chr(97+i): chr(0x1F130+i) for i in range(26)})
FULL = {chr(i): chr(0xFF00+i-0x20) for i in range(0x21, 0x7F)}
SCRIPT_FIX = {"B":"\u212c","E":"\u2130","F":"\u2131","H":"\u210b","I":"\u2110","L":"\u2112","M":"\u2133","R":"\u211b","e":"\u212f","g":"\u210a","o":"\u2134"}
FRAK_FIX = {"C":"\u212d","H":"\u210c","I":"\u2111","R":"\u211c","Z":"\u2128"}

def _script(text):
    out = []
    for ch in text:
        if ch in SCRIPT_FIX:
            out.append(SCRIPT_FIX[ch])
        elif "a" <= ch <= "z":
            out.append(chr(0x1D4B6 + ord(ch) - 97))
        elif "A" <= ch <= "Z":
            out.append(chr(0x1D49C + ord(ch) - 65))
        else:
            out.append(ch)
    return "".join(SCRIPT_FIX.get(src, ch) for src, ch in zip(text, out))

def _fraktur(text):
    out = []
    for ch in text:
        if ch in FRAK_FIX:
            out.append(FRAK_FIX[ch])
        elif "a" <= ch <= "z":
            out.append(chr(0x1D51E + ord(ch) - 97))
        elif "A" <= ch <= "Z":
            out.append(chr(0x1D504 + ord(ch) - 65))
        else:
            out.append(ch)
    return "".join(out)

def _striked(text):
    return "".join(ch + "\u0336" for ch in text)

def _wide(text):
    return " ".join(list(text.strip())) if text.strip() else text

ENGINES = {
    "bold": _math(0x1D41A, 0x1D400, 0x1D7CE),
    "italic": _math(0x1D44E, 0x1D434),
    "bolditalic": _math(0x1D482, 0x1D468),
    "sans": _math(0x1D5BA, 0x1D5A0, 0x1D7E2),
    "sansbold": _math(0x1D5EE, 0x1D5D4, 0x1D7EC),
    "script": _script,
    "boldscript": _math(0x1D4EA, 0x1D4D0),
    "double": _math(0x1D552, 0x1D538, 0x1D7D8),
    "mono": _math(0x1D68A, 0x1D670, 0x1D7F6),
    "fraktur": _fraktur,
    "smallcaps": _map_font(SMALL),
    "fullwidth": lambda t: "".join(FULL.get(ch, ch) for ch in t),
    "circled": _map_font(CIRCLED),
    "squared": _map_font(SQUARED),
    "tiny": _map_font(TINY),
    "cjk": _map_font(CJK),
    "striked": _striked,
    "wide": _wide,
    "cursive2": _map_font(CURSIVE2),
    "inverted": _map_font(INVERTED),
}

STYLE_LABELS = {k: k.replace("bolditalic","Bold Italic").replace("boldscript","Bold Script").replace("smallcaps","Small Caps").replace("cursive2","Cursive").title() for k in ENGINES}

def style_text(text, style):
    text = (text or "")[:32]
    return ENGINES.get(style, ENGINES["smallcaps"])(text)

def framed(text, frame):
    left, right = FRAMES.get(frame, ("", ""))
    return f"{left}{text}{right}"

def generate_all(name, category="all", frame="none"):
    name = (name or "").strip()[:32] or "Harry"
    items, seen = [], set()
    for style in CAT_STYLES.get(category, CAT_STYLES["all"]):
        val = framed(style_text(name, style), frame)
        if val in seen:
            continue
        seen.add(val)
        items.append((STYLE_LABELS.get(style, style), val))
    if category in ("all", "royal", "cute"):
        for label, val in [
            ("Royal Seal", framed(style_text(name, "script"), "royal")),
            ("Crown Bold", framed(style_text(name, "bold"), "crown")),
            ("Star Script", framed(style_text(name, "boldscript"), "star")),
            ("Wing Caps", framed(style_text(name, "smallcaps"), "wing")),
        ]:
            if val not in seen:
                seen.add(val)
                items.append((label, val))
    return items

def generate_random(name, n=12):
    name = (name or "").strip()[:32] or "Harry"
    items, seen, tries = [], set(), 0
    styles, frames = list(ENGINES), list(FRAMES)
    while len(items) < n and tries < n * 8:
        tries += 1
        style, frame = random.choice(styles), random.choice(frames)
        val = framed(style_text(name, style), frame)
        if val in seen:
            continue
        seen.add(val)
        items.append((STYLE_LABELS.get(style, style) + " \u00b7 " + frame, val))
    return items

def available_fonts():
    return list(ENGINES)
