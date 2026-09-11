"""Central Telegram inline-button factory for Bot API 9.4 / PTB 22.8."""
from telegram import InlineKeyboardButton
from emoji_ids import EMOJI_IDS


def btn(text, style=None, icon=None, **kwargs):
    """Create a button with the supported Telegram palette and custom emoji icon."""
    kw = dict(kwargs)
    if style in {"primary", "success", "danger"}:
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
    return btn(text, style="primary", icon=kwargs.pop("icon", EMOJI_IDS[4 % len(EMOJI_IDS)]), **kwargs)


def green(text, **kwargs):
    return btn(text, style="success", icon=kwargs.pop("icon", EMOJI_IDS[1 % len(EMOJI_IDS)]), **kwargs)


def red(text, **kwargs):
    return btn(text, style="danger", icon=kwargs.pop("icon", EMOJI_IDS[2 % len(EMOJI_IDS)]), **kwargs)
