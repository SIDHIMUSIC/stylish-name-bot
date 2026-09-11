import asyncio
import html
import logging
import os
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatType
from telegram.error import Forbidden, RetryAfter, TelegramError
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import storage
from styles import CATEGORIES, build_catalog

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("stylish-bot")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_URL = os.getenv("OWNER_URL", "https://t.me/SANATANI_BACHA")
SUPPORT_URL = os.getenv("SUPPORT_URL", "https://t.me/HARRYASHU")
STYLE_URL = os.getenv("STYLE_URL", "https://t.me/TG_BIO_STYLE")
PROMO_HOURS = float(os.getenv("PROMO_HOURS", "1"))

BATCH = 10
COOLDOWN = 2.0
NAME_LIMIT = 24

EMOJI_IDS = [
    "6057848605601963652",
    "6124902618574625426",
    "6124898345082165755",
    "6125399112499075549",
    "6197330889765033702",
]
FALLBACKS = ["\U0001F44D", "\u2728", "\U0001F525", "\U0001F48E", "\U0001F451"]

CAT_BTN = {
    "all": "\U0001F90D All",
    "cute": "\U0001FA77 Cute",
    "royal": "\U0001F9E1 Royal",
    "dark": "\U0001F5A4 Dark",
    "gaming": "\U0001F49A Gaming",
    "aesthetic": "\U0001F499 Aesthetic",
    "nature": "\U0001F49C Nature",
}


def pe(index: int) -> str:
    eid = EMOJI_IDS[index % len(EMOJI_IDS)]
    fb = FALLBACKS[index % len(FALLBACKS)]
    return f'<tg-emoji emoji-id="{eid}">{fb}</tg-emoji>'


def ejoin(*indexes: int) -> str:
    return "".join(pe(i) for i in indexes)


def session(context: ContextTypes.DEFAULT_TYPE) -> dict:
    data = context.user_data
    data.setdefault("name", "Ashu")
    data.setdefault("category", "all")
    data.setdefault("offset", 0)
    data.setdefault("rows", [])
    data.setdefault("last_gen", 0.0)
    return data


def start_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("\U0001F496 Support", url=SUPPORT_URL),
                InlineKeyboardButton("\U0001F451 Owner", url=OWNER_URL),
            ],
            [
                InlineKeyboardButton("\U0001F338 Bio Style", url=STYLE_URL),
                InlineKeyboardButton("\U0001F525 Channel", url=STYLE_URL),
            ],
        ]
    )


def page_kb(offset: int, total: int, category: str) -> InlineKeyboardMarkup:
    nav = []
    if offset > 0:
        nav.append(InlineKeyboardButton("\u2B05\uFE0F Back", callback_data="nav|back"))
    if offset + BATCH < total:
        nav.append(InlineKeyboardButton("\u27A1\uFE0F Next 10", callback_data="nav|more"))
    rows = []
    if nav:
        rows.append(nav)
    rows.append(
        [
            InlineKeyboardButton(("\u2705 " if category == "cute" else "") + "\U0001FA77 Cute", callback_data="cat|cute"),
            InlineKeyboardButton(("\u2705 " if category == "royal" else "") + "\U0001F9E1 Royal", callback_data="cat|royal"),
            InlineKeyboardButton(("\u2705 " if category == "dark" else "") + "\U0001F5A4 Dark", callback_data="cat|dark"),
        ]
    )
    rows.append(
        [
            InlineKeyboardButton(("\u2705 " if category == "gaming" else "") + "\U0001F49A Game", callback_data="cat|gaming"),
            InlineKeyboardButton(("\u2705 " if category == "aesthetic" else "") + "\U0001F499 Aesthetic", callback_data="cat|aesthetic"),
            InlineKeyboardButton(("\u2705 " if category == "nature" else "") + "\U0001F49C Nature", callback_data="cat|nature"),
        ]
    )
    rows.append(
        [
            InlineKeyboardButton("\U0001F90D All Styles", callback_data="cat|all"),
            InlineKeyboardButton("\U0001F504 New Name", callback_data="nav|new"),
        ]
    )
    return InlineKeyboardMarkup(rows)


def title_line() -> str:
    tail = ejoin(0, 0, 0, 0)
    return (
        f"{ejoin(0, 1, 2)}\n"
        f"<b>\U0001F44D HEY I AM PREMIUM NAME MAKER BOT {tail}</b>"
    )


def start_text(who: str, private: bool = True) -> str:
    safe = html.escape(who)
    body = (
        f"{title_line()}\n\n"
        f"{pe(3)} Welcome, <b>{safe}</b>\n"
        f"{pe(4)} 1000+ Unicode fonts \u00b7 frames \u00b7 VIP lines\n"
        f"{pe(1)} Copy any style and paste on Telegram name / bio\n"
    )
    if private:
        body += (
            f"\n{pe(2)} <b>Apna naam bhejo</b>\n"
            f"{pe(0)} ya <code>/style Harry</code>"
        )
    else:
        body += (
            f"\n{pe(2)} Group mein sirf command:\n"
            f"<code>/style naam</code>\n"
            f"{pe(0)} Normal message pe reply nahi aayega."
        )
    return body


def promo_text() -> str:
    return (
        f"{title_line()}\n\n"
        f"{pe(3)} Stylish name chahiye?\n"
        f"{pe(4)} Group: <code>/style yourname</code>\n"
        f"{pe(1)} Private: seedha naam bhejo\n"
        f"{pe(2)} Cute \u00b7 Royal \u00b7 Dark \u00b7 Gaming packs\n"
        f"{pe(0)} Fast \u00b7 Free \u00b7 Premium look"
    )


def format_page(name: str, rows: list[str], offset: int, total: int) -> str:
    chunk = rows[offset : offset + BATCH]
    bits = [
        title_line(),
        "",
        f"{pe(1)} Name: <b>{html.escape(name)}</b>",
        f"{pe(4)} {offset + 1}\u2013{offset + len(chunk)} / {total}",
        "",
    ]
    for i, item in enumerate(chunk, start=offset + 1):
        bits.append(f"<b>{i}.</b> <code>{html.escape(item)}</code>")
    bits.append("")
    bits.append(f"{pe(2)} Tap style \u2192 copy \u2192 Telegram name pe paste")
    return "\n".join(bits)


def too_fast(data: dict) -> bool:
    now = time.monotonic()
    if now - data["last_gen"] < COOLDOWN:
        return True
    data["last_gen"] = now
    return False


async def send_page(target, data: dict, edit: bool = False) -> None:
    rows = data.get("rows") or []
    offset = max(int(data.get("offset", 0)), 0)
    if not rows:
        await target.reply_text("Koi style nahi bani. Naya naam bhejo.")
        return
    text = format_page(data.get("name", "Ashu"), rows, offset, len(rows))
    markup = page_kb(offset, len(rows), data.get("category", "all"))
    if edit:
        await target.edit_text(text, reply_markup=markup, parse_mode="HTML")
        return
    await target.reply_text(text, reply_markup=markup, parse_mode="HTML")


def rebuild(data: dict) -> None:
    data["rows"] = build_catalog(data["name"], data.get("category", "all"))
    data["offset"] = 0


def _clean_name(name: str) -> str:
    return (name or "").strip()[:NAME_LIMIT] or "Ashu"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    user = update.effective_user
    who = (user.first_name if user else "Dear")[:24]
    private = bool(chat and chat.type == ChatType.PRIVATE)
    if chat and chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        storage.add_group(chat.id)
    await update.message.reply_text(
        start_text(who, private=private),
        reply_markup=start_kb(),
        parse_mode="HTML",
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        f"{pe(0)} <b>Kaise use karein</b>\n"
        f"PM: naam bhejo\n"
        f"Group: <code>/style Harry</code>\n\n"
        f"{pe(1)} Buttons se category badlo\n"
        f"{pe(2)} Next 10 se aur styles\n"
        f"{pe(3)} Style pe tap karke copy"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=start_kb())


async def generate_for(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str) -> None:
    data = session(context)
    if too_fast(data):
        await update.effective_message.reply_text("2 sec ruko, phir try karo.")
        return
    data["name"] = _clean_name(name)
    rebuild(data)
    await send_page(update.effective_message, data)
    chat = update.effective_chat
    if chat and chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        storage.add_group(chat.id)


async def font_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = session(context)
    if context.args:
        name = " ".join(context.args)
    else:
        if update.effective_chat and update.effective_chat.type != ChatType.PRIVATE:
            await update.message.reply_text(
                "Group mein aise use karo:\n<code>/style Harry</code>",
                parse_mode="HTML",
            )
            return
        name = data.get("name", "Ashu")
    await generate_for(update, context, name)


async def random_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = session(context)
    name = " ".join(context.args) if context.args else data.get("name", "Ashu")
    data["category"] = "all"
    await generate_for(update, context, name)


async def on_private_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message.text or "").strip()
    if not text:
        return
    await generate_for(update, context, text)


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = session(context)
    payload = query.data or ""
    if payload.startswith("cat|"):
        cat = payload.split("|", 1)[1]
        if cat not in CATEGORIES:
            return
        data["category"] = cat
        rebuild(data)
        await send_page(query.message, data, edit=True)
        return
    if payload == "nav|new":
        await query.message.reply_text(
            f"{pe(1)} Naya naam bhejo\nGroup mein <code>/style naam</code>",
            parse_mode="HTML",
        )
        return
    if payload == "nav|more":
        data["offset"] = min(data.get("offset", 0) + BATCH, max(len(data.get("rows", [])) - 1, 0))
        await send_page(query.message, data, edit=True)
        return
    if payload == "nav|back":
        data["offset"] = max(data.get("offset", 0) - BATCH, 0)
        await send_page(query.message, data, edit=True)


async def on_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    member = update.my_chat_member
    if not member:
        return
    chat = member.chat
    if chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return
    status = member.new_chat_member.status
    if status in ("member", "administrator"):
        storage.add_group(chat.id)
        try:
            await context.bot.send_message(
                chat.id,
                start_text("fam", private=False),
                reply_markup=start_kb(),
                parse_mode="HTML",
            )
        except TelegramError:
            log.debug("welcome failed in %s", chat.id)
    elif status in ("left", "kicked"):
        storage.remove_group(chat.id)


async def hourly_promo(context: ContextTypes.DEFAULT_TYPE) -> None:
    text = promo_text()
    markup = start_kb()
    for chat_id in storage.list_groups():
        try:
            await context.bot.send_message(chat_id, text, reply_markup=markup, parse_mode="HTML")
            await asyncio.sleep(0.2)
        except Forbidden:
            storage.remove_group(chat_id)
        except RetryAfter as err:
            await asyncio.sleep(err.retry_after + 1)
        except TelegramError as err:
            log.info("promo skip %s: %s", chat_id, err)


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.exception("update failed: %s", context.error)


def main() -> None:
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN missing")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("font", font_cmd))
    app.add_handler(CommandHandler("style", font_cmd))
    app.add_handler(CommandHandler("random", random_cmd))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(ChatMemberHandler(on_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, on_private_name))
    app.add_error_handler(on_error)
    job_queue = app.job_queue
    if job_queue:
        job_queue.run_repeating(hourly_promo, interval=max(PROMO_HOURS, 0.25) * 3600, first=60, name="hourly-promo")
    else:
        log.warning("JobQueue missing. Install python-telegram-bot[job-queue]")
    log.info("Stylish Name Bot online")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
