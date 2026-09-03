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


LOOKS = {
    "greekish": _az("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "αв¢∂єƒgнιנкℓмησρqяѕтυνωχуz"),
    "currency": _az("₳฿₵ĐɆ₣₲ĦłJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ҮɎƵ"),
    "frozen": _az("ΛBCDΣFGHIJKLMNӨPQRƧƬUVWXYZ", "λbcdεfghijklмnθpqrƨƭuvwxyz"),
}
LOOKS["tiny2"] = {
    **{chr(97 + i): "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖqʳˢᵗᵘᵛʷˣʸᶻ"[i] for i in range(26)},
    **{chr(65 + i): "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻ"[i] for i in range(26)},
}
LOOKS["flip"] = {
    **{chr(97 + i): "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"[i] for i in range(26)},
}
LOOKS["paren"] = {**{chr(97 + i): chr(0x249C + i) for i in range(26)}, **{chr(65 + i): chr(0x249C + i) for i in range(26)}}
LOOKS["darksq"] = {**{chr(65 + i): chr(0x1F170 + i) for i in range(26)}, **{chr(97 + i): chr(0x1F170 + i) for i in range(26)}}


def lookalike_fonts(name: str) -> list[str]:
    out = []
    for mapping in LOOKS.values():
        out.append(apply_map(name, mapping))
    flipped = apply_map(name, LOOKS.get("flip", {}))
    out.append(flipped[::-1])
    if name.strip():
        chars = list(name.strip())
        out.append("·".join(chars))
        out.append("⋆".join(chars))
        out.append("∿".join(chars))
        out.append(" ".join(chars))
        out.append("【" + "】【".join(chars) + "】")
    return out


EXTRA_WRAPS = [
    "✯ ⎯꯭ {n} ⎯꯭̽ ✯",
    "꧁☠⃝ጪ9 {n} ጪa☠⃝꧂",
    "᭡ {n} ♡»",
    "⵿ {n} ⳿",
    "⋆꯭ {n} ⋆꯭",
    "◄⏤ {n} ⏤►",
    "「 {n} 」",
    "『 {n} 』",
    "【 {n} 】",
    "  {n} ᚁ",
    "᛭ {n} ᛭",
    "⌘ {n} ⌘",
    "✓ {n} ✓",
    "❄ {n} ❄",
    "✈ {n} ✈",
    "✎ {n} ✎",
    "✪ {n} ✪",
    "☯ {n} ☯",
]

PREFIXES = ["✯", "⎯꯭", "➛꯭", "◄⏤", "꧁", "ጪ9", "⛧", "☠⃝", "★", "✦", "⚡", "♛"]
SUFFIXES = ["✯", "⎯꯭", "ጪa", "꧂", "ᾮ7", "⳿", "⵿", "★", "✦", "♛", "⚡"]
