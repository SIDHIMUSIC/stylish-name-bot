CATEGORIES = ("all", "cute", "royal", "dark", "gaming", "aesthetic")

FRAMES = {
    "none": ("", ""),
    "royal": ("꧁྄ ", " ྄꧂"),
    "star": ("✦ ", " ✦"),
    "heart": ("♡ ", " ♡"),
    "crown": ("👑 ", " 👑"),
    "game": ("▸ ", " ◂"),
    "cute": ("✧･", "･✧"),
    "dark": ("☠ ", " ☠"),
    "brack": ("【", "】"),
}

CAT_STYLES = {
    "cute": ["script", "smallcaps", "circled", "italic"],
    "royal": ["boldserif", "double", "script", "smallcaps"],
    "dark": ["bold", "mono", "fullwidth"],
    "gaming": ["mono", "fullwidth", "circled", "bold"],
    "aesthetic": ["italic", "script", "smallcaps", "double"],
    "all": ["bold", "italic", "bolditalic", "script", "double", "mono", "smallcaps", "fullwidth", "circled"],
}

SMALL = {
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ꜰ",
    "g": "ɢ", "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ",
    "m": "ᴍ", "n": "ɴ", "o": "ᴏ", "p": "ᴘ", "q": "ǫ", "r": "ʀ",
    "s": "ѕ", "t": "ᴛ", "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "ʏ",
    "y": "ʏ", "z": "ᴢ",
}
CIRCLED = {
    **{chr(97 + i): chr(0x24D0 + i) for i in range(26)},
    **{chr(65 + i): chr(0x24B6 + i) for i in range(26)},
}
FULL = {chr(i): chr(0xFF00 + i - 0x20) for i in range(0x21, 0x7F)}


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


ENGINES = {
    "bold": _math(0x1D41A, 0x1D400, 0x1D7CE),
    "italic": _math(0x1D44E, 0x1D434),
    "bolditalic": _math(0x1D482, 0x1D468),
    "script": _math(0x1D4B6, 0x1D49C),
    "boldserif": _math(0x1D41A, 0x1D400, 0x1D7CE),
    "double": _math(0x1D552, 0x1D538, 0x1D7D8),
    "mono": _math(0x1D68A, 0x1D670, 0x1D7F6),
    "smallcaps": lambda t: "".join(SMALL.get(ch.lower(), ch) if ch.isalpha() else ch for ch in t),
    "fullwidth": lambda t: "".join(FULL.get(ch, ch) for ch in t),
    "circled": lambda t: "".join(CIRCLED.get(ch, ch) for ch in t),
}


def style_text(text, style):
    text = (text or "")[:32]
    fn = ENGINES.get(style, ENGINES["smallcaps"])
    return fn(text)


def framed(text, frame):
    left, right = FRAMES.get(frame, ("", ""))
    return f"{left}{text}{right}"


def generate_all(name, category="all", frame="none"):
    name = (name or "").strip()[:32] or "Harry"
    items = []
    seen = set()
    for style in CAT_STYLES.get(category, CAT_STYLES["all"]):
        val = framed(style_text(name, style), frame)
        if val in seen:
            continue
        seen.add(val)
        items.append((style, val))
    return items
