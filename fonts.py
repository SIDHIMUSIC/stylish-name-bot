"""Unicode style maps + frames."""

LATIN = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

STYLES = {
    "bold": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀѕᴛᴜᴠᴡʏʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀѕᴛᴜᴠᴡʏʏᴢ0123456789",
    "boldserif": "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    "italic": "𝑎𝑏𝑐𝑑𝑒𝑓𝑔𝑕𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍0123456789",
    "bolditalic": "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁0123456789",
    "script": "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜𝒝𝒞𝒟𝒠𝒡𝒢𝒣𝒤𝒥𝒦𝒧𝒨𝒩𝒪𝒫𝒬𝒭𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵0123456789",
    "double": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙ𝕈ℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    "mono": "𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    "bubble": "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ⓪①②③④⑤⑥⑦⑧⑨",
    "square": "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉0123456789",
    "tiny": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀѕᴛᴜᴠᴡʏʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀѕᴛᴜᴠᴡʏʏᴢ₀₁₂₃₄₅₆₇₈₉",
}

# fallback simple maps that are reliable
SIMPLE = {
    "smallcaps": {
        "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ꜰ",
        "g": "ɢ", "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ",
        "m": "ᴍ", "n": "ɴ", "o": "ᴏ", "p": "ᴘ", "q": "ǫ", "r": "ʀ",
        "s": "ѕ", "t": "ᴛ", "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "ʏ",
        "y": "ʏ", "z": "ᴢ",
    },
    "fullwidth": {c: chr(0xFF00 + ord(c) - 0x20) for c in "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"},
    "circled": {
        **{chr(97+i): chr(0x24D0+i) for i in range(26)},
        **{chr(65+i): chr(0x24B6+i) for i in range(26)},
        **{str(i): chr(0x2460+i-1) if i else "⓪" for i in range(10)},
    },
}

FRAMES = {
    "royal": ("꧁྄", "྄꧂"),
    "dark": ("☠", "☠"),
    "star": ("✦ ", " ✦"),
    "heart": ("♡ ", " ♡"),
    "fire": ("🔥", "🔥"),
    "crown": ("👑 ", " 👑"),
    "wave": ("「", "」"),
    "brack": ("【", "】"),
    "game": ("▸ ", " ◂"),
    "cute": ("✧･", "･✧"),
    "ice": ("❄️ ", " ❄️"),
    "none": ("", ""),
}

CATEGORIES = {
    "cute": ["script", "smallcaps", "circled"],
    "royal": ["boldserif", "double", "script"],
    "dark": ["bold", "mono", "square"],
    "gaming": ["square", "mono", "fullwidth"],
    "aesthetic": ["italic", "script", "smallcaps"],
    "all": list(dict.fromkeys(list(STYLES) + list(SIMPLE))),
}


def apply_map(text, mapping):
    if isinstance(mapping, str):
        table = {}
        # pairing by index is fragile for surrogate pairs; use SIMPLE instead when needed
        return text
    return "".join(mapping.get(ch, mapping.get(ch.lower(), ch)) for ch in text)


def style_text(text, style):
    text = (text or "")[:32]
    if style in SIMPLE:
        return apply_map(text, SIMPLE[style])
    # mathematical styles via str.translate on BMP-safe maps only
    if style == "smallcaps":
        return apply_map(text, SIMPLE["smallcaps"])
    if style == "fullwidth":
        return apply_map(text, SIMPLE["fullwidth"])
    if style == "circled":
        return apply_map(text, SIMPLE["circled"])
    # use unicodedata-free explicit maps for common fancy
    FANCY = {
        "bold": _math(0x1D41A, 0x1D400, 0x1D7CE),
        "italic": _math(0x1D44E, 0x1D434, None),
        "bolditalic": _math(0x1D482, 0x1D468, None),
        "script": _math(0x1D4B6, 0x1D49C, None),
        "double": _math(0x1D552, 0x1D538, 0x1D7D8),
        "mono": _math(0x1D68A, 0x1D670, 0x1D7F6),
        "bubble": SIMPLE["circled"],
        "square": None,
    }
    fn = FANCY.get(style)
    if callable(fn):
        return fn(text)
    if style == "bubble":
        return apply_map(text, SIMPLE["circled"])
    if style == "square":
        return apply_map(text, SIMPLE["circled"]).join("") or apply_map(text, SIMPLE["fullwidth"])
    return apply_map(text, SIMPLE["smallcaps"])


def _math(low_a, up_a, digit_0):
    def conv(text):
        out = []
        for ch in text:
            if "a" <= ch <= "z":
                out.append(chr(low_a + (ord(ch) - 97)))
            elif "A" <= ch <= "Z":
                out.append(chr(up_a + (ord(ch) - 65)))
            elif digit_0 is not None and "0" <= ch <= "9":
                out.append(chr(digit_0 + (ord(ch) - 48)))
            else:
                out.append(ch)
        return "".join(out)
    return conv


def framed(text, frame):
    left, right = FRAMES.get(frame, ("", ""))
    return f"{left}{text}{right}"


def generate_all(name, category="all", frame="none"):
    styles = CATEGORIES.get(category, CATEGORIES["all"])
    items = []
    for style in styles:
        styled = style_text(name, style)
        items.append((style, framed(styled, frame)))
        if frame == "none":
            for fk in ("royal", "star", "heart", "crown", "game", "cute"):
                items.append((f"{style}+{fk}", framed(styled, fk)))
    # unique keep order
    seen = set()
    uniq = []
    for k, v in items:
        if v in seen:
            continue
        seen.add(v)
        uniq.append((k, v))
    return uniq
