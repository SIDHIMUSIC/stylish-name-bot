def _math(low, up, d0=None):
    def conv(text):
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


def _combine(text, mark):
    return "".join((ch + mark) if ch.isalnum() else ch for ch in text)


SMALL = {"a":"\u1d00","b":"\u0299","c":"\u1d04","d":"\u1d05","e":"\u1d07","f":"\u0493","g":"\u0262","h":"\u029c","i":"\u026a","j":"\u1d0a","k":"\u1d0b","l":"\u029f","m":"\u1d0d","n":"\u0274","o":"\u1d0f","p":"\u1d18","q":"\u01eb","r":"\u0280","s":"s","t":"\u1d1b","u":"\u1d1c","v":"\u1d20","w":"\u1d21","x":"x","y":"\u028f","z":"\u1d22"}
CJK = {"a":"\uff71","b":"\u4e43","c":"\u110c","d":"\u308a","e":"\u4e47","f":"\uff77","g":"\u30e0","h":"\u3093","i":"\uff89","j":"\uff8c","k":"\u30ba","l":"\uff9a","m":"\uffb6","n":"\u5200","o":"\u306e","p":"\uff71","q":"\u3090","r":"\u5c3a","s":"\u4e02","t":"\uff72","u":"\u3072","v":"\u221a","w":"\uff92","x":"\uff92","y":"\uff98","z":"\u4e59"}


def _map(m):
    return lambda t: "".join(m.get(ch.lower(), ch) if ch.isalpha() else ch for ch in t)


FONTS = [
    ("plain", lambda t: t),
    ("bold", _math(0x1D41A, 0x1D400, 0x1D7CE)),
    ("italic", _math(0x1D44E, 0x1D434)),
    ("bolditalic", _math(0x1D482, 0x1D468)),
    ("script", _math(0x1D4B6, 0x1D49C)),
    ("boldscript", _math(0x1D4EA, 0x1D4D0)),
    ("double", _math(0x1D552, 0x1D538, 0x1D7D8)),
    ("mono", _math(0x1D68A, 0x1D670, 0x1D7F6)),
    ("sansbold", _math(0x1D5EE, 0x1D5D4, 0x1D7EC)),
    ("fraktur", _math(0x1D51E, 0x1D504)),
    ("small", _map(SMALL)),
    ("cjk", _map(CJK)),
    ("full", lambda t: "".join(chr(0xFF00 + ord(ch) - 0x20) if 33 <= ord(ch) <= 126 else ch for ch in t)),
    ("strike", lambda t: _combine(t, "\u0336")),
    ("under", lambda t: _combine(t, "\u0332")),
    ("over", lambda t: _combine(t, "\u0305")),
    ("arrow", lambda t: _combine(t, "\u0362")),
]

WRAPS = [
    "{n}",
    "\u2605\u00b8.\u2022\u00b4\u00af`\u2022.\u00b8\u2605 {n} \u2605\u00b8.\u2022\u00b4\u00af`\u2022.\u2605",
    ".\u2022\u266b\u2022\u266c\u2022 {n} \u2022\u266c\u2022\u266b\u2022.",
    "\u2570\u2606\u2606 {n} \u2606\u2606\u256e",
    "\u2661 {n} \u2661",
    "\u273f {n} \u273f",
    "\u2764\ufe0f {n} \U0001F47B \u00d7",
    "\u2022 {n} \u2764\ufe0f",
    "I'M \u2192 {n} \u2764\ufe0f \u00d7 \u2192",
    "i am.. \u2605\u2605\u2605 {n} \u2605",
    "\u265B {n} \u265B",
    "\U0001F451 {n} \U0001F451",
    "\u300E {n} \u300F",
    "\u300C {n} \u300D",
    "\u3010 {n} \u3011",
    "\u2620 {n} \u2620",
    "\u00d7\u035c\u00d7 {n} \u4e97",
    "\u26A1 {n} \u26A1",
    "\U0001F525 {n} \U0001F525",
    "\u0d7d\u0f12 {n} \u0f12\u0d7e",
    "\u0f3a {n} \u0f3b",
    "\ua4f0 {n} \ua4f1",
    "\u2726 {n} \u2726",
    "\u2606 {n} \u2606",
    "\u30c4 {n} \u30c4",
    "\u23af {n} \u23af",
    "{n} jaan",
    "jaanu {n}",
    "pagal {n}",
    "dil {n}",
    "raja {n}",
    "{n} bhai",
    "only {n} \U0001F497",
    "my {n} \U0001F49E",
]

P = ["","\u2605 ","\u2606 ","\u2726 ","\u265B ","\U0001F451 ","\u2661 ","\u2764\ufe0f ","\U0001F338 ","\U0001F525 ","\u26A1 ","\u2620 ","\u2728 ","\u00d7\u035c\u00d7 ","\u4e97 ","\u30c4 ","\u0d7d ","\u0f3a ","\u300E ","\u300C ","\u3010 ","\u2022 ","Mr. ","only ","my ","king ","pagal ","dil ","jaanu ","raja ","desi ","swag "]
S = [""," \u2605"," \u2606"," \u2726"," \u265B"," \U0001F451"," \u2661"," \u2764\ufe0f"," \U0001F338"," \U0001F525"," \u26A1"," \u2620"," \u2728"," \U0001F47B"," \u00d7"," \u4e97"," \u30c4"," \u0d7e"," \u0f3b"," \u300F"," \u300D"," \u3011"," \u2022"," ji"," bhai"," jaan"," baby"," <3"]


def build_all(name):
    name = (name or "").strip()[:24] or "Name"
    styled = []
    for _, fn in FONTS:
        try:
            styled.append(fn(name))
        except Exception:
            styled.append(name)
    inners, seen_i = [], set()
    for s in styled:
        if s not in seen_i:
            seen_i.add(s); inners.append(s)
    items = []
    for wrap in WRAPS:
        for inner in inners[:8]:
            items.append(wrap.replace("{n}", inner))
    for i, pre in enumerate(P):
        for j, suf in enumerate(S):
            inner = inners[(i + j) % len(inners)]
            items.append(f"{pre}{inner}{suf}".strip())
    if " " not in name and len(name) <= 16:
        items += [" ".join(name), "\u00b7".join(name), "_".join(name), _combine(" ".join(name), "\u0332")]
    out, seen = [], set()
    for x in items:
        x = " ".join(str(x).split())
        if x and x not in seen:
            seen.add(x); out.append(x)
    return out
