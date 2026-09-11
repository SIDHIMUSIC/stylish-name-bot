"""Premium colored inline keyboards with Telegram copy-text support."""
from telegram import InlineKeyboardMarkup

try:
    from telegram import CopyTextButton
except ImportError:
    CopyTextButton = None

from emoji_ids import EMOJI_IDS
from kbstyle import btn

PAGE_SIZE = 10
CATS = (
    ("premium", "👑 PREMIUM DESIGN (156 Styles)"),
    ("aesthetic", "✨ Aesthetic Art Styles (107 Styles)"),
    ("live", "🎬 LIVE DESIGN • Prefix/Suffix/Emoji/Underline"),
    ("hindi", "🇮🇳 Hindi Live Design (15 Styles)"),
)


def cat_kb():
    rows = []
    for i, (key, label) in enumerate(CATS):
        # Keep Live on the same category callback path as the proven flow.
        # bot.py's category handler then opens the dedicated Live Studio.
        rows.append([
            btn(
                label,
                callback_data=f"cat|{key}",
                style="primary" if i % 2 == 0 else "success",
                icon=EMOJI_IDS[i],
            )
        ])
    rows.append([
        btn("New Name", callback_data="menu|name", style="success", icon=EMOJI_IDS[1]),
        btn("Main Menu", callback_data="menu|home", style="danger", icon=EMOJI_IDS[2]),
    ])
    return InlineKeyboardMarkup(rows)


def styles_kb(rows, page):
    start = page * PAGE_SIZE
    chunk = rows[start:start + PAGE_SIZE]
    buttons = []
    for i, item in enumerate(chunk):
        idx = start + i
        label = f"{i + 1}. {item}"
        if len(label) > 64:
            label = label[:61] + "..."
        kwargs = {
            "style": "primary" if i % 2 == 0 else "success",
            "icon": EMOJI_IDS[i % len(EMOJI_IDS)],
        }
        if CopyTextButton is not None:
            kwargs["copy_text"] = CopyTextButton(text=item)
        else:
            kwargs["callback_data"] = f"pick|{idx}"
        buttons.append([btn(label, **kwargs)])

    total_pages = max((len(rows) + PAGE_SIZE - 1) // PAGE_SIZE, 1)
    buttons.append([
        btn(f"{page + 1}/{total_pages}", callback_data="noop", style="primary", icon=EMOJI_IDS[0]),
        btn("Next >", callback_data="page|next", style="success", icon=EMOJI_IDS[1]),
    ])
    buttons.append([
        btn("< Back", callback_data="page|back", style="primary", icon=EMOJI_IDS[0]),
        btn("New Name", callback_data="menu|name", style="success", icon=EMOJI_IDS[1]),
        btn("Main Menu", callback_data="menu|home", style="danger", icon=EMOJI_IDS[2]),
    ])
    return InlineKeyboardMarkup(buttons)
