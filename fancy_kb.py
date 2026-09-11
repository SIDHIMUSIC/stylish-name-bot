"""Colored + copy keyboards. bot.py can import these later."""
from telegram import InlineKeyboardMarkup

try:
    from telegram import CopyTextButton
except ImportError:
    CopyTextButton = None

try:
    from emoji_ids import EMOJI_IDS
except ImportError:
    EMOJI_IDS = ["6057848605601963652"]

from kbstyle import btn

PAGE_SIZE = 10
CATS = (
    ("premium", "PREMIUM DESIGN"),
    ("aesthetic", "Aesthetic Art Styles"),
    ("live", "Live Design"),
    ("hindi", "Hindi Live Design"),
)


def cat_kb():
    pal = ["primary", "success", "primary", "success"]
    rows = []
    for i, (key, label) in enumerate(CATS):
        rows.append([btn(label, callback_data=f"cat|{key}", style=pal[i % 4], icon=EMOJI_IDS[i % len(EMOJI_IDS)])])
    rows.append([
        btn("New Name", callback_data="menu|name", style="success", icon=EMOJI_IDS[1 % len(EMOJI_IDS)]),
        btn("Main Menu", callback_data="menu|home", style="danger", icon=EMOJI_IDS[2 % len(EMOJI_IDS)]),
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
        extra = {"style": "primary" if i % 2 == 0 else "success", "icon": EMOJI_IDS[i % len(EMOJI_IDS)]}
        if CopyTextButton is not None:
            extra["copy_text"] = CopyTextButton(text=item)
        else:
            extra["callback_data"] = f"pick|{idx}"
        buttons.append([btn(label, **extra)])
    total_pages = max((len(rows) + PAGE_SIZE - 1) // PAGE_SIZE, 1)
    buttons.append([
        btn(f"{page + 1}/{total_pages}", callback_data="noop", style="primary", icon=EMOJI_IDS[0]),
        btn("Next >", callback_data="page|next", style="success", icon=EMOJI_IDS[1 % len(EMOJI_IDS)]),
    ])
    buttons.append([
        btn("< Back", callback_data="page|back", style="primary", icon=EMOJI_IDS[0]),
        btn("New Name", callback_data="menu|name", style="success", icon=EMOJI_IDS[1 % len(EMOJI_IDS)]),
        btn("Main Menu", callback_data="menu|home", style="danger", icon=EMOJI_IDS[2 % len(EMOJI_IDS)]),
    ])
    return InlineKeyboardMarkup(buttons)
