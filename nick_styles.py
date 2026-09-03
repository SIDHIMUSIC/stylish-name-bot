"""Stylish nicks: Unicode fonts + combining marks + frames from the fancy pack."""

from __future__ import annotations


def _math(low: int, up: int, d0: int | None = None):
    def conv(text: str) -> str:
        out = []
        for ch in text:
            if "a" <= ch <= "z":
                out.append(chr(low + ord(ch) - 97))
            elif "A" <= ch <= "Z":
                out.append(chr(up + ord(ch) - 65))
            elif d0 is not None and "0" <= ch <= "9":
                out.append(chr(d0 + ord(ch) - 48))
            else:
                out.append(ch)
        return "".join(out)

    return conv


def _map(mapping: dict[str, str]):
    def conv(text: str) -> str:
        out = []
        for ch in text:
            if ch in mapping:
                out.append(mapping[ch])
            elif ch.lower() in mapping and ch.isalpha():
                out.append(mapping[ch.lower()])
            else:
                out.append(ch)
        return "".join(out)

    return conv


def _combine(text: str, *marks: str) -> str:
    stacked = "".join(marks)
    out = []
    for ch in text:
        if ch.isalnum():
            out.append(ch + stacked)
        else:
            out.append(ch)
    return "".join(out)


SCRIPT_FIX = {
    "B": "\u212c",
    "E": "\u2130",
    "F": "\u2131",
    "H": "\u210b",
    "I": "\u2110",
    "L": "\u2112",
    "M": "\u2133",
    "R": "\u211b",
    "e": "\u212f",
    "g": "\u210a",
    "o": "\u2134",
}
FRAK_FIX = {
    "C": "\u212d",
    "H": "\u210c",
    "I": "\u2111",
    "R": "\u211c",
    "Z": "\u2128",
}
DOUBLE_FIX = {
    "C": "\u2102",
    "H": "\u210d",
    "N": "\u2115",
    "P": "\u2119",
    "Q": "\u211a",
    "R": "\u211d",
    "Z": "\u2124",
}

SMALL = {
    "a": "\u1d00", "b": "\u0299", "c": "\u1d04", "d": "\u1d05", "e": "\u1d07",
    "f": "\u0493", "g": "\u0262", "h": "\u029c", "i": "\u026a", "j": "\u1d0a",
    "k": "\u1d0b", "l": "\u029f", "m": "\u1d0d", "n": "\u0274", "o": "\u1d0f",
    "p": "\u1d18", "q": "\u01eb", "r": "\u0280", "s": "s", "t": "\u1d1b",
    "u": "\u1d1c", "v": "\u1d20", "w": "\u1d21", "x": "x", "y": "\u028f", "z": "\u1d22",
}
TINY = {
    "a": "\u1d43", "b": "\u1d47", "c": "\u1d9c", "d": "\u1d48", "e": "\u1d49",
    "f": "\u1da0", "g": "\u1d4d", "h": "\u02b0", "i": "\u2071", "j": "\u02b2",
    "k": "\u1d4f", "l": "\u02e1", "m": "\u1d50", "n": "\u207f", "o": "\u1d52",
    "p": "\u1d56", "q": "q", "r": "\u02b3", "s": "\u02e2", "t": "\u1d57",
    "u": "\u1d58", "v": "\u1d5b", "w": "\u02b7", "x": "\u02e3", "y": "\u02b8", "z": "\u1dbb",
}
CJK = {
    "a": "\uff71", "b": "\u4e43", "c": "\u110c", "d": "\u308a", "e": "\u4e47",
    "f": "\uff77", "g": "\u30e0", "h": "\u3093", "i": "\uff89", "j": "\uff8c",
    "k": "\u30ba", "l": "\uff9a", "m": "\uffb6", "n": "\u5200", "o": "\u306e",
    "p": "\uff71", "q": "\u3090", "r": "\u5c3a", "s": "\u4e02", "t": "\uff72",
    "u": "\u3072", "v": "\u221a", "w": "\uff92", "x": "\uff92", "y": "\uff98", "z": "\u4e59",
}
INVERTED = {
    "a": "\u0250", "b": "q", "c": "\u0254", "d": "p", "e": "\u01dd",
    "f": "\u025f", "g": "\u0183", "h": "\u0265", "i": "\u1d09", "j": "\u027e",
    "k": "\u029e", "l": "l", "m": "\u026f", "n": "u", "o": "o",
    "p": "d", "q": "b", "r": "\u0279", "s": "s", "t": "\u0287",
    "u": "n", "v": "\u028c", "w": "\u028d", "x": "x", "y": "\u028e", "z": "z",
}
CIRCLED = {
    **{chr(97 + i): chr(0x24D0 + i) for i in range(26)},
    **{chr(65 + i): chr(0x24B6 + i) for i in range(26)},
}
BLACK_CIRCLED = {chr(65 + i): chr(0x1F150 + i) for i in range(26)}
BLACK_CIRCLED.update({chr(97 + i): chr(0x1F150 + i) for i in range(26)})
SQUARED = {chr(65 + i): chr(0x1F130 + i) for i in range(26)}
SQUARED.update({chr(97 + i): chr(0x1F130 + i) for i in range(26)})
FULL = {chr(i): chr(0xFF00 + i - 0x20) for i in range(0x21, 0x7F)}


def _fixed_math(low: int, up: int, fixes: dict[str, str], d0: int | None = None):
    base = _math(low, up, d0)

    def conv(text: str) -> str:
        raw = base(text)
        out = []
        for src, ch in zip(text, raw):
            out.append(fixes.get(src, ch))
        return "".join(out)

    return conv


ITALIC_FIX = {"h": "\u210e"}


def _wide(text: str) -> str:
    t = text.strip()
    return " ".join(t) if t else text


FONTS = [
    ("plain", lambda t: t),
    ("bold", _math(0x1D41A, 0x1D400, 0x1D7CE)),
    ("sansbold", _math(0x1D5EE, 0x1D5D4, 0x1D7EC)),
    ("italic", _fixed_math(0x1D44E, 0x1D434, ITALIC_FIX)),
    ("bolditalic", _math(0x1D482, 0x1D468)),
    ("sans", _math(0x1D5BA, 0x1D5A0, 0x1D7E2)),
    ("sansitalic", _math(0x1D622, 0x1D608)),
    ("sansbolditalic", _math(0x1D656, 0x1D63C)),
    ("mono", _math(0x1D68A, 0x1D670, 0x1D7F6)),
    ("double", _fixed_math(0x1D552, 0x1D538, DOUBLE_FIX, 0x1D7D8)),
    ("fraktur", _fixed_math(0x1D51E, 0x1D504, FRAK_FIX)),
    ("boldfraktur", _math(0x1D586, 0x1D56C)),
    ("script", _fixed_math(0x1D4B6, 0x1D49C, SCRIPT_FIX)),
    ("boldscript", _math(0x1D4EA, 0x1D4D0)),
    ("small", _map(SMALL)),
    ("tiny", _map(TINY)),
    ("cjk", _map(CJK)),
    ("inverted", _map(INVERTED)),
    ("circled", _map(CIRCLED)),
    ("blackcircled", _map(BLACK_CIRCLED)),
    ("squared", _map(SQUARED)),
    ("full", lambda t: "".join(FULL.get(ch, ch) for ch in t)),
    ("wide", _wide),
    ("under", lambda t: _combine(t, "\u0332")),
    ("dunder", lambda t: _combine(t, "\u0333")),
    ("thickunder", lambda t: _combine(t, "\u035f")),
    ("over", lambda t: _combine(t, "\u0305")),
    ("dover", lambda t: _combine(t, "\u033f")),
    ("strike", lambda t: _combine(t, "\u0336")),
    ("slash", lambda t: _combine(t, "\u0338")),
    ("meetei", lambda t: _combine(t, "\uabed")),
    ("stack", lambda t: _combine(t, "\uabed", "\u035f")),
    ("arrow", lambda t: _combine(t, "\u0362")),
    ("tie", lambda t: _combine(t, "\u035c")),
    ("circlemark", lambda t: _combine(t, "\u20dd")),
    ("boxmark", lambda t: _combine(t, "\u20de")),
]

_bold_sans = _math(0x1D5EE, 0x1D5D4, 0x1D7EC)
_bold = _math(0x1D41A, 0x1D400, 0x1D7CE)
_script = _fixed_math(0x1D4B6, 0x1D49C, SCRIPT_FIX)
_frak_bold = _math(0x1D586, 0x1D56C)


def _u_bold_sans(t: str) -> str:
    return _combine(_bold_sans(t), "\u035f")


def _u_bold(t: str) -> str:
    return _combine(_bold(t), "\u035f")


WRAPS = [
    "{n}",
    "\ua9c1\u0f3a {n} \u0f3b\ua9c2",
    "\ua9c1 {n} \ua9c2",
    "\ua9c1\u2620\u20dd\U000132a9 {n} \U000132aa\u2620\u20dd\ua9c2",
    "\ua9c1\u09dd\u09df\u262c\u271e {n} \u271e\u262c\u09dd\u09df\ua9c2",
    "\U000132a9\u2661\U000132aa {n} \U000132a9\u2661\U000132aa",
    "\U000132a9 {n} \U000132aa",
    "\U000132a9\u336c\u336d\u20db {n} \u2661\u00bb\U000132aa",
    "\u272f \u23af\uabed\u033d {n} \u2665\ufe0f\u20dd\u035f\u035f \uabed\u23af\uabed\u033d",
    "\u272f \u23af\uabed {n} \u23af\uabed\u033d \u272f",
    "\u2501\u2501\u2501\u2726 {n} \u2726\u2501\u2501\u2501",
    "\u2501\u2501\u2501\u2661 {n} \u2661\u2501\u2501\u2501",
    "\u256d\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u256e\n       {n}\n\u2570\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u256f",
    "\u2605\u00b8.\u2022\u00b4\u00af`\u2022.\u00b8\u2605 {n} \u2605\u00b8.\u2022\u00b4\u00af`\u2022.\u2605",
    ".\u2022\u266b\u2022\u266c\u2022 {n} \u2022\u266c\u2022\u266b\u2022.",
    "\u2570\u2606\u2606 {n} \u2606\u2606\u256e",
    "\u2661 {n} \u2661",
    "\u273f {n} \u273f",
    "\u2764 {n} \u2764",
    "\u265b {n} \u265b",
    "\U0001f451 {n} \U0001f451",
    "\u300e {n} \u300f",
    "\u300c {n} \u300d",
    "\u3010 {n} \u3011",
    "\u3016 {n} \u3017",
    "\u300a {n} \u300b",
    "\u3014 {n} \u3015",
    "\u3018 {n} \u3019",
    "\u301a {n} \u301b",
    "\u27e6 {n} \u27e7",
    "\u27e8 {n} \u27e9",
    "\u276e {n} \u276f",
    "\u2770 {n} \u2771",
    "\u0f3a {n} \u0f3b",
    "\u0f3c {n} \u0f3d",
    "\u4ed7 \u300e {n} \u300f \u4ed7",
    "\U0001164d \u2500\u2501 {n} \u2501\u2500 \U0001164d",
    "\U00011910 {n} \U00011910",
    "\u26a1 {n} \u26a1",
    "\u2620 {n} \u2620",
    "\u2694 {n} \u2694",
    "\u2726 {n} \u2726",
    "\u2727 {n} \u2727",
    "\u2605 {n} \u2605",
    "\u2606 {n} \u2606",
    "\u272a {n} \u272a",
    "\u00d7\u035c\u00d7 {n} \u4e77",
    "\u30c4 {n} \u30c4",
    "\u23af {n} \u23af",
    "\u1bd3\u2605 {n} \u2605\u1bd3",
    "\u26e7 {n} \u26e7",
    "\u271e {n} \u271e",
    "\U0001fae7 {n} \U0001fae7",
    "\U0001f43c {n} \U0001f43c",
    "\u25c4\u23e4 {n} \u23e4\u25ba",
    "I'M \u2192 {n} \u2764 \u00d7 \u2192",
    "only {n} \U0001f497",
    "my {n} \U0001f49e",
    "{n} jaan",
    "jaanu {n}",
    "pagal {n}",
    "dil {n}",
    "raja {n}",
    "{n} bhai",
    "king {n}",
    "desi {n}",
    "swag {n}",
    "\u22c6\uabed {n} \u22c6\uabed",
    "\u23af\uabed {n} \u23af\uabed",
    "\u279b {n} \u279b",
]


def _unique(seq: list[str], collapse: bool = True) -> list[str]:
    out, seen = [], set()
    for x in seq:
        x = str(x)
        if collapse and "\n" not in x:
            x = " ".join(x.split())
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def styled_fonts(name: str) -> list[str]:
    items = []
    for _, fn in FONTS:
        try:
            items.append(fn(name))
        except Exception:
            items.append(name)
    items.append(_u_bold_sans(name))
    items.append(_u_bold(name))
    items.append(_combine(_script(name), "\u035f"))
    items.append(_combine(_frak_bold(name), "\u035f"))
    return _unique(items)


def build_all(name: str) -> list[str]:
    name = (name or "").strip()[:24] or "Name"
    fonts = styled_fonts(name)
    wrap_inners = fonts[:12]
    items: list[str] = []

    for wrap in WRAPS:
        if "\n" in wrap:
            items.append(wrap.replace("{n}", wrap_inners[1] if len(wrap_inners) > 1 else name))
            continue
        for inner in wrap_inners[:4]:
            items.append(wrap.replace("{n}", inner))

    hero = [_bold_sans(name), _u_bold_sans(name), _bold(name), fonts[0]]
    extra_frames = [
        "\ua9c1\u0f3a {n} \u0f3b\ua9c2",
        "\U000132a9\u2661\U000132aa {n} \U000132a9\u2661\U000132aa",
        "\u272f \u23af\uabed\u033d {n} \u23af\uabed\u033d \u272f",
        "\u2501\u2501\u2501\u2726 {n} \u2726\u2501\u2501\u2501",
        "\u4ed7 \u300e {n} \u300f \u4ed7",
        "\U0001164d \u2500\u2501 {n} \u2501\u2500 \U0001164d",
        "\ua9c1\u09dd\u09df\u262c\u271e {n} \u271e\u262c\u09dd\u09df\ua9c2",
        "\U000132a9 {n} \u2661\u00bb \U000132aa",
        "\u22c6\uabed {n} \u22c6\uabed\U00013083\u033d",
        "\u25c0 {n} \u25b6",
    ]
    for frame in extra_frames:
        for inner in hero:
            items.append(frame.replace("{n}", inner))

    if " " not in name and len(name) <= 16:
        items += [
            " ".join(name),
            "\u00b7".join(name),
            "_".join(name),
            _combine(" ".join(name), "\u0332"),
            _combine(" ".join(name), "\u035f"),
        ]

    boxed = []
    rest = []
    for x in items:
        if "\n" in str(x):
            boxed.append(str(x))
        else:
            rest.append(x)
    return _unique(boxed + rest)
