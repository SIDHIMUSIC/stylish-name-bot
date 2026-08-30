CATEGORIES = ("all", "cute", "royal", "dark", "gaming", "aesthetic")

FRAMES = {
    "none": ("", ""),
    "royal": ("꧁྄ ", " ྄꧂"),
    "star": ("* ", " *"),
    "heart": ("<3 ", " <3"),
    "crown": ("~ ", " ~"),
    "game": ("> ", " <"),
    "cute": (". ", " ."),
    "dark": ("x ", " x"),
    "brack": ("[", "]"),
}

# nicer unicode frames
FRAMES["star"] = ("\u2726 ", " \u2726")
FRAMES["heart"] = ("\u2661 ", " \u2661")
FRAMES["crown"] = ("\U0001F451 ", " \U0001F451")
FRAMES["game"] = ("\u25b8 ", " \u25c2")
FRAMES["cute"] = ("\u2727\uff65", "\uff65\u2727")
FRAMES["dark"] = ("\u2620 ", " \u2620")
FRAMES["brack"] = ("\u3010", "\u3011")

CAT_STYLES = {
    "cute": ["script", "smallcaps", "circled", "italic"],
    "royal": ["bold", "double", "script", "smallcaps"],
    "dark": ["bold", "mono", "fullwidth"],
    "gaming": ["mono", "fullwidth", "circled", "bold"],
    "aesthetic": ["italic", "script", "smallcaps", "double"],
    "all": ["bold", "italic", "bolditalic", "script", "double", "mono", "smallcaps", "fullwidth", "circled"],
}

SMALL = {
    "a": "\u1d00", "b": "\u0299", "c": "\u1d04", "d": "\u1d05", "e": "\u1d07", "f": "\ua730",
    "g": "\u0262", "h": "\u029c", "i": "\u026a", "j": "\u1d0a", "k": "\u1d0b", "l": "\u029f",
    "m": "\u1d0d", "n": "\u0274", "o": "\u1d0f", "p": "\u1d18", "q": "\u01eb", "r": "\u0280",
    "s": "\u0455", "t": "\u1d1b", "u": "\u1d1c", "v": "\u1d20", "w": "\u1d21", "x": "\u028f",
    "y": "\u028f", "z": "\u1d22",
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
