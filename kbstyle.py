"""Colored inline buttons for Bot API 9.4 / PTB 22.7+."""
from telegram import InlineKeyboardButton

EMOJI_IDS = [
    "6057848605601963652",
    "6124902618574625426",
    "6124898345082165755",
    "6125399112499075549",
    "6197330889765033702",
]

def btn(text, style=None, icon=None, **kwargs):
    kw = dict(kwargs)
    if style:
        kw["style"] = style
    if icon:
        kw["icon_custom_emoji_id"] = str(icon)
    try:
        return InlineKeyboardButton(text, **kw)
    except TypeError:
        kw.pop("style", None)
        kw.pop("icon_custom_emoji_id", None)
        return InlineKeyboardButton(text, **kw)

def blue(text, **kwargs):
    return btn(text, style="primary", icon=kwargs.pop("icon", EMOJI_IDS[4]), **kwargs)

def green(text, **kwargs):
    return btn(text, style="success", icon=kwargs.pop("icon", EMOJI_IDS[1]), **kwargs)

def red(text, **kwargs):
    return btn(text, style="danger", icon=kwargs.pop("icon", EMOJI_IDS[2]), **kwargs)
