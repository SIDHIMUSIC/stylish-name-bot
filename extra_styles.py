"""Lookalike alphabets + extra frames from fsymbols / gypu / fancy generators."""
from __future__ import annotations


def _az(upper: str, lower: str | None = None):
    u = [c for c in upper if c != " "]
    mapping = {}
    if len(u) >= 26:
        for i, ch in enumerate(u[:26]):
            mapping[chr(65 + i)] = ch
            mapping[chr(97 + i)] = ch
    if lower:
        lo = [c for c in lower if c != " "]
        if len(lo) >= 26:
            for i, ch in enumerate(lo[:26]):
                mapping[chr(97 + i)] = ch
    return mapping


def apply_map(text: str, mapping: dict[str, str]) -> str:
    return "".join(mapping.get(ch, mapping.get(ch.lower(), ch)) for ch in text)


LOOKS = {}
LOOKS["tiny2"] = {
    **{chr(97 + i): "\u1d43\u1d47\u1d9c\u1d48\u1d49\u1da0\u1d4d\u02b0\u2071\u02b2\u1d4f\u02e1\u1d50\u207f\u1d52\u1d56q\u02b3\u02e2\u1d57\u1d58\u1d5b\u02b7\u02e3\u02b8\u1dbb"[i] for i in range(26)},
}
LOOKS["flip"] = {
    **{chr(97 + i): "\u0250q\u0254p\u01dd\u025f\u0183\u0265\u1d09\u027e\u029el\u026fuodb\u0279s\u0287n\u028c\u028dx\u028ez"[i] for i in range(26)},
}
LOOKS["paren"] = {**{chr(97 + i): chr(0x249C + i) for i in range(26)}, **{chr(65 + i): chr(0x249C + i) for i in range(26)}}
LOOKS["darksq"] = {**{chr(65 + i): chr(0x1F170 + i) for i in range(26)}, **{chr(97 + i): chr(0x1F170 + i) for i in range(26)}}
LOOKS["currency"] = _az("\u20b3\u0e3f\u20b5\u0110\u0246\u20a3\u20b2\u0126\u0142J\u20ad\u2c60\u20a5\u20a6\u00d8\u20b1Q\u2c64\u20b4\u20ae\u0244V\u20a9\u04ae\u024e\u01b5")


def lookalike_fonts(name: str) -> list[str]:
    out = []
    for mapping in LOOKS.values():
        out.append(apply_map(name, mapping))
    flipped = apply_map(name, LOOKS.get("flip", {}))
    out.append(flipped[::-1])
    if name.strip():
        chars = list(name.strip())
        out.append("\u00b7".join(chars))
        out.append("\u22c6".join(chars))
        out.append("\u223f".join(chars))
        out.append(" ".join(chars))
        out.append("\u3010" + "\u3011\u3010".join(chars) + "\u3011")
        out.append("[" + "][".join(chars) + "]")
    return out


EXTRA_WRAPS = [
    "\u272f \u23af\uabed {n} \u23af\uabed\u033d \u272f",
    "\ua9c1\u2620\u20dd {n} \u2620\u20dd\ua9c2",
    "\u1b61 {n} \u2661\u00bb",
    "\u2d7f {n} \u2cff",
    "\u22c6\uabed {n} \u22c6\uabed",
    "\u25c4\u23e4 {n} \u23e4\u25ba",
    "\u300c {n} \u300d",
    "\u300e {n} \u300f",
    "\u3010 {n} \u3011",
    "\u16ed {n} \u16ed",
    "\u2318 {n} \u2318",
    "\u2713 {n} \u2713",
    "\u2744 {n} \u2744",
    "\u270e {n} \u270e",
    "\u272a {n} \u272a",
    "\u262f {n} \u262f",
]

PREFIXES = ["\u272f", "\u23af\uabed", "\u279b\uabed", "\u25c4\u23e4", "\ua9c1", "\u26e7", "\u2620\u20dd", "\u2605", "\u2726", "\u26a1", "\u265b"]
SUFFIXES = ["\u272f", "\u23af\uabed", "\ua9c2", "\u1fae7", "\u2cff", "\u2d7f", "\u2605", "\u2726", "\u265b", "\u26a1"]
