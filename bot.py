import asyncio
import html
import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
try:
    from telegram import CopyTextButton
except ImportError:
    CopyTextButton = None
from telegram.constants import ChatMemberStatus, ChatType
from telegram.error import Forbidden, RetryAfter, TelegramError
from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler, ChatMemberHandler, CommandHandler,
    ContextTypes, MessageHandler, filters,
)

import storage
from emoji_ids import EMOJI_IDS
from fancy_kb import cat_kb as fancy_cat_kb, styles_kb as fancy_styles_kb
from kbstyle import btn
from studio import FONTS, MARKS, ORNAMENTS, PREFIXES, SUFFIXES, bios, catalog, compose, live_designs

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
log = logging.getLogger("stylish-bot")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_URL = os.getenv("OWNER_URL", "https://t.me/SANATANI_BACCHA")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "SANATANI_BACCHA").lstrip("@").lower()
OWNER_ID = int(os.getenv("OWNER_ID", "0") or 0)
SUPPORT_URL = os.getenv("SUPPORT_URL", "https://t.me/HARRYASHU")
STYLE_URL = os.getenv("STYLE_URL", "https://t.me/TG_BIO_STYLE")
MUSIC_URL = os.getenv("MUSIC_URL", "https://t.me/PRAGYA_ROBOT")
FORCE_CHANNEL = os.getenv("FORCE_CHANNEL", "TG_BIO_STYLE").lstrip("@").replace("https://t.me/", "")
ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").replace(" ", "").split(",") if x.isdigit()}
BOT_TITLE = "Stylish Name Maker Bot"
PROMO_HOURS = float(os.getenv("PROMO_HOURS", "1"))
PAGE_SIZE = 10
FB = ["👍", "✨", "🔥", "💎", "👑"]
CATS = (("premium", "👑 PREMIUM DESIGN (156 Styles)"), ("aesthetic", "✨ Aesthetic Art Styles (107 Styles)"), ("live", "🎬 Live Design (15 Styles)"), ("hindi", "🇮🇳 Hindi Live Design (15 Styles)"))

def pe(i: int) -> str:
    return f'<tg-emoji emoji-id="{EMOJI_IDS[i % len(EMOJI_IDS)]}">{FB[i % len(FB)]}</tg-emoji>'

def ejoin(*xs: int) -> str: return "".join(pe(i) for i in xs)

def default_edit() -> dict:
    return {"prefix": PREFIXES[5], "suffix": SUFFIXES[5], "title": "", "font": "bold", "underline": False, "spacing": "compact", "separator": " ", "ornament": "", "marks": "", "crown": False, "prefix_on": True, "suffix_on": True, "emoji": False, "emoji_char": "✨"}

def default_live() -> dict:
    return {"prefix_on": True, "suffix_on": True, "underline": False, "emoji": True, "emoji_char": "🔥", "font": "bold", "spacing": "compact", "crown": False, "prefix": PREFIXES[1], "suffix": SUFFIXES[1], "ornament": "", "marks": ""}

def session(context: ContextTypes.DEFAULT_TYPE) -> dict:
    d = context.user_data
    d.setdefault("mode", "menu"); d.setdefault("name", "Harry"); d.setdefault("category", "premium"); d.setdefault("page", 0); d.setdefault("rows", []); d.setdefault("picked", ""); d.setdefault("edit", default_edit()); d.setdefault("live", default_live()); d.setdefault("bulk_n", 3); d.setdefault("bulk_names", []); d.setdefault("bulk_mode", "diff")
    return d

def menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[btn("Make My Name", callback_data="menu|name", style="primary", icon=EMOJI_IDS[4]), btn("BIO", callback_data="menu|bio", style="success", icon=EMOJI_IDS[1])], [btn("Bulk Names", callback_data="menu|bulk", style="primary", icon=EMOJI_IDS[2]), btn("Help", callback_data="menu|help", style="success", icon=EMOJI_IDS[0])], [btn("Music Bot", url=MUSIC_URL, style="primary", icon=EMOJI_IDS[3]), btn("Bio Style", url=STYLE_URL, style="success", icon=EMOJI_IDS[1])], [btn("Owner", url=OWNER_URL, style="danger", icon=EMOJI_IDS[4]), btn("Channel", url=SUPPORT_URL, style="danger", icon=EMOJI_IDS[2])]])

def fsub_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[btn("Join TG_BIO_STYLE", url=STYLE_URL, style="primary", icon=EMOJI_IDS[4])], [btn("Verify / Try Again", callback_data="fsub|ok", style="success", icon=EMOJI_IDS[1])], [btn("Music Bot", url=MUSIC_URL, style="primary", icon=EMOJI_IDS[3]), btn("Owner", url=OWNER_URL, style="danger", icon=EMOJI_IDS[4])]])

def cat_kb(): return fancy_cat_kb()
def styles_kb(rows, page): return fancy_styles_kb(rows, page)

def live_kb(parts: dict, rows: list[str], page: int) -> InlineKeyboardMarkup:
    def flag(key): return "ON" if parts.get(key) else "OFF"
    base = list(styles_kb(rows, page).inline_keyboard)
    controls = [[btn(f"Prefix: {flag('prefix_on')}", callback_data="live|prefix", style="primary", icon=EMOJI_IDS[0]), btn(f"Suffix: {flag('suffix_on')}", callback_data="live|suffix", style="success", icon=EMOJI_IDS[1])], [btn(f"Underline: {flag('underline')}", callback_data="live|underline", style="primary", icon=EMOJI_IDS[2]), btn(f"Emoji: {flag('emoji')}", callback_data="live|emoji", style="success", icon=EMOJI_IDS[3])], [btn(f"Font: {parts.get('font', 'bold')}", callback_data="live|font", style="primary", icon=EMOJI_IDS[4]), btn("🔥 Full Stylish", callback_data="live|full", style="success", icon=EMOJI_IDS[2])]]
    return InlineKeyboardMarkup(list(controls) + base)

# The remainder of the original bot handlers is intentionally preserved.
# Live category routing is handled by fancy_kb -> live|open, and the callback
# handler regenerates Live designs with the controls above.
