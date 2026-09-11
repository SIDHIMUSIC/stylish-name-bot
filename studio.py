"""Local Unicode name studio: fonts, handcrafted formats and light ornaments."""
from __future__ import annotations

try:
    from fonts import ENGINES, style_text
except ImportError:
    ENGINES = {}
    def style_text(text, style): return text or ""

try:
    from nick_styles import build_all as pack_build
except ImportError:
    pack_build = None

try:
    from extra_styles import EXTRA_WRAPS, PREFIXES as XPRE, SUFFIXES as XSUF, lookalike_fonts
except ImportError:
    EXTRA_WRAPS, XPRE, XSUF = [], [], []
    def lookalike_fonts(name): return []

try:
    from name_formats import apply_formats
except ImportError:
    def apply_formats(name): return []

MEITEI = "\uABED"
CIRCLE = "\u20DD"
L, R = "\U000131A9", "\U000131AA"
FONTS = ["bold", "italic", "script", "boldscript", "smallcaps", "mono", "double", "fraktur"]
MARKS = ["", "★", "✦", "✨", "⃝"]
ORNAMENTS = ["", "♡", "✧", "❀", "⚡", "🌸", "🌿", "🦋", "🤍", "👑"]
EMOJI_DECOR = ["🔥", "💎", "👑", "✨", "💖", "🌸", "🦋", "🤍", "🌙", "⚡", "🌹", "🎀"]
PREFIXES = ["", L, "◄⸻", "✯", "⸻", "꧁", "❥", "『", "【", "❖", "➳", "♛", "👑", "🔥"] + list(XPRE)
SUFFIXES = ["", R, "⸻►", "✯", "⸻", "꧂", "❥", "』", "】", "🌸", "🤍", "🦋", "👑", "🔥"] + list(XSUF)
PREMIUM_WRAPS = [L + " {n} " + R, L + "{n}" + R, "◄⸻ {n} ⸻►", "✯ ⸻꯭ {n} ⸻꯭ ✯", "꧁ {n} ꧂", "『 {n} 』", "【 {n} 】", "❖ {n} ❖", "➳ {n} ➳", "♛ {n} ♛", "👑 {n} 👑", "💎 {n} 💎", "🔥 {n} 🔥"]
AESTHETIC_WRAPS = [L + " {n} " + R, "❥ {n} ❥", "『 {n} 』", "♡ {n} ♡", "🎀 {n} 🎀", "🦋 {n} 🦋", "🤍 {n} 🤍", "❀ {n} ❀", "🌿 {n} 🌿"]
LIVE_WRAPS = [L + "{n}" + R, "『{n}』", "【{n}】", "✦{n}✦", "⚡{n}⚡", "🔥{n}🔥"]
HINDI_WRAPS = [L + " {n} " + R, "जय {n} 🚩", "ॐ {n} ॐ", "🙏 {n} 🙏", "👑 राजा {n}"]

def apply_font(name: str, font: str) -> str:
    return style_text(name, font) if font in ENGINES else name

def strike(name: str) -> str:
    return "".join(ch + MEITEI if ch.strip() else ch for ch in name)

def circled(name: str) -> str:
    return name if not name else name[:-1] + name[-1] + CIRCLE

def _unique(items, limit=None):
    out, seen = [], set()
    for item in items:
        item = str(item).strip()
        if not item or item in seen: continue
        seen.add(item); out.append(item)
        if limit and len(out) >= limit: break
    return out

def _targeted(name, category):
    raw = (name or "Name").strip()[:24] or "Name"
    wraps = {"premium": PREMIUM_WRAPS, "aesthetic": AESTHETIC_WRAPS, "live": LIVE_WRAPS, "hindi": HINDI_WRAPS}.get(category, PREMIUM_WRAPS)
    items = list(apply_formats(raw))
    for font in FONTS:
        core = apply_font(raw, font)
        items += [core, f"{L} {core} {R}", f"꧁ {core} ꧂", f"『 {core} 』", f"【 {core} 】"]
    for wrap in wraps:
        for font in FONTS[:6]:
            items.append(wrap.replace("{n}", apply_font(raw, font)))
    bold = apply_font(raw, "bold")
    items += [f"{L} {strike(bold)} {R}", f"{L} {circled(bold)} {R}"]
    for pre, suf in zip(PREFIXES[1:10], SUFFIXES[1:10]): items.append(f"{pre} {bold} {suf}")
    for ornament in ORNAMENTS[1:]: items.append(f"{ornament} {bold} {ornament}")
    if pack_build and category in ("premium", "aesthetic", "live"):
        try: items.extend(pack_build(raw))
        except Exception: pass
    try: items.extend(lookalike_fonts(raw))
    except Exception: pass
    for wrap in EXTRA_WRAPS: items.append(str(wrap).replace("{n}", bold))
    return _unique(items)

def catalog(name: str, category: str) -> list[str]:
    targets = {"premium": 156, "aesthetic": 107, "live": 15, "hindi": 15}
    target = targets.get(category, 156)
    raw = (name or "Name").strip()[:24] or "Name"
    items = _targeted(raw, category)
    if len(items) < target:
        for font in FONTS:
            core = apply_font(raw, font)
            for pre in PREFIXES:
                for suf in SUFFIXES:
                    if pre or suf: items.append(f"{pre} {core} {suf}")
                    if len(items) >= target: break
                if len(items) >= target: break
            if len(items) >= target: break
    return _unique(items, target)

def compose(name: str, parts: dict) -> str:
    core = apply_font(name, parts.get("font") or "bold")
    if parts.get("spacing") == "wide": core = " ".join(core)
    if parts.get("underline"): core = strike(core)
    if parts.get("crown"): core = f"👑 {core} 👑"
    prefix = parts.get("prefix", "") if parts.get("prefix_on", True) else ""
    suffix = parts.get("suffix", "") if parts.get("suffix_on", True) else ""
    emoji = parts.get("emoji_char", "✨") if parts.get("emoji") else ""
    chunks = [prefix, parts.get("title", ""), emoji, core, suffix, parts.get("ornament", ""), parts.get("marks", "")]
    return " ".join(str(x).strip() for x in chunks if str(x).strip()).strip()

def live_designs(name: str, parts: dict) -> list[str]:
    """Build 15 deterministic live designs from the current ON/OFF controls."""
    raw = (name or "Name").strip()[:24] or "Name"
    fonts = [parts.get("font") or "bold", "boldscript", "script", "double", "mono", "fraktur", "italic", "smallcaps"]
    prefixes = PREFIXES[1:] or [""]
    suffixes = SUFFIXES[1:] or [""]
    out = []
    for i in range(15):
        p = dict(parts)
        p["font"] = fonts[i % len(fonts)]
        p["prefix"] = prefixes[i % len(prefixes)] if parts.get("prefix_on", True) else ""
        p["suffix"] = suffixes[(i + 2) % len(suffixes)] if parts.get("suffix_on", True) else ""
        p["emoji_char"] = EMOJI_DECOR[i % len(EMOJI_DECOR)]
        if i % 3 == 1: p["underline"] = True
        if i % 5 == 4: p["marks"] = "✦"
        if i % 7 == 6: p["ornament"] = "♡"
        out.append(compose(raw, p))
    return _unique(out, 15)

def bios(name: str) -> list[str]:
    n = (name or "Me").strip()[:28] or "Me"
    fancy, bold = apply_font(n, "script"), apply_font(n, "bold")
    return [f"{L} {n} {R} | aesthetic", f"✨ {fancy} | dreamer ✨", f"👑 VIP • {bold}", f"🤍 nobody asked but {n} is everything", f"sunsets and self-love | {fancy}", f"🌸 sirf {fancy}", f"🇮🇳 {n} | desi soul", f"🎵 {fancy} x music", f"🧿 {strike(n)} | nazar", f"➳ {circled(bold)} hustle"]
