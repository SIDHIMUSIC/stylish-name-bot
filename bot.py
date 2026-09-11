import asyncio
import html
import logging
import os
import time
from uuid import uuid4

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.constants import ChatType
from telegram.error import Forbidden, RetryAfter, TelegramError
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
    MessageHandler,
    filters,
)

import storage
from styles import CAT_LABELS, CATEGORIES, build_catalog, build_preview

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

BATCH = 8
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
                InlineKeyboardButton("Support", url=SUPPORT_URL),
                InlineKeyboardButton("Owner", url=OWNER_URL),
            ],
            [InlineKeyboardButton("Bio Style", url=STYLE_URL)],
            [InlineKeyboardButton("Try inline", switch_inline_query_current_chat="")],
        ]
    )


def category_kb(current: str = "all") -> InlineKeyboardMarkup:
    row = []
    rows = []
    for key in CATEGORIES:
        mark = "\u2022 " if key == current else ""
        row.append(
            InlineKeyboardButton(
                f"{mark}{CAT_LABELS[key]}",
                callback_data=f"cat|{key}",
            )
        )
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def page_kb(offset: int, total: int, category: str) -> InlineKeyboardMarkup:
    buttons = []
    nav = []
    if offset > 0:
        nav.append(InlineKeyboardButton("\u25c0 Back", callback_data="nav|back"))
    if offset + BATCH < total:
        nav.append(InlineKeyboardButton("CONTINUE \u25b6", callback_data="nav|more"))
    if nav:
        buttons.append(nav)
    buttons.append(
        [
            InlineKeyboardButton("Categories", callback_data="nav|cats"),
            InlineKeyboardButton("New name", callback_data="nav|new"),
        ]
    )
    return InlineKeyboardMarkup(buttons)


def start_text(who: str, private: bool = True) -> str:
    safe = html.escape(who)
    crown = ejoin(0, 1, 2)
    tail = ejoin(0, 0, 0, 0)
    body = (
        f"{crown}\n"
        f"<b>\U0001F44D \U0001D407\U0001D404\U0001D418 I AM PREMIUM NAME MAKER BOT {tail}</b>\n\n"
        f"{pe(3)} Welcome, <b>{safe}</b>\n\n"
        f"{pe(4)} Fancy Unicode \u00b7 VIP underlines \u00b7 frames\n"
        f"{pe(1)} Categories + inline search + easy copy\n"
    )
    if private:
        body += (
            f"\n{pe(2)} <i>PM me a name</i>\n"
            f"{pe(0)} or use <code>/style Harry</code>"
        )
    else:
        body += (
            f"\n{pe(2)} Group mein sirf command chalti hai:\n"
            f"<code>/style naam</code>\n"
            f"{pe(0)} Seedha naam likhne se reply nahi aayega."
        )
    return body


def promo_text() -> str:
    tail = ejoin(0, 0, 0, 0)
    return (
        f"{ejoin(0, 1, 2)}\n"
        f"<b>\U0001F44D \U0001D407\U0001D404\U0001D418 I AM PREMIUM NAME MAKER BOT {tail}</b>\n\n"
        f"{pe(3)} Stylish name chahiye?\n"
        f"{pe(4)} Group: <code>/style yourname</code>\n"
        f"{pe(1)} Private: seedha naam bhejo\n"
        f"{pe(2)} Inline: type <code>@bot naam</code>\n\n"
        f"{pe(0)} Fast \u00b7 Free \u00b7 Premium emoji pack"
    )


def format_page(rows: list[str], offset: int, total: int) -> str:
    chunk = rows[offset : offset + BATCH]
    lines = [f"{pe(offset % 5)} <code>{html.escape(item)}</code>" for item in chunk]
    left = max(total - offset - len(chunk), 0)
    head = f"{pe(1)} <b>{len(chunk)}</b> styles \u00b7 {left} more \u00b7 {total} total\n"
    return head + "\n".join(lines)


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
    text = format_page(rows, offset, len(rows))
    markup = page_kb(offset, len(rows), data.get("category", "all"))
    if edit:
        await target.edit_text(text, reply_markup=markup, parse_mode="HTML")
        return
    await target.reply_text(text, reply_markup=markup, parse_mode="HTML")


def rebuild(data: dict) -> None:
    data["rows"] = build_catalog(data["name"], data.get("category", "all"))
    data["offset"] = 0


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
        f"{pe(0)} <b>Commands</b>\n"
        f"/start \u2014 intro\n"
        f"/style naam \u2014 generate\n"
        f"/font naam \u2014 same as /style\n"
        f"/random \u2014 random name pack\n\n"
        f"{pe(1)} <b>PM</b>: seedha naam likho.\n"
        f"{pe(2)} <b>Group</b>: sirf <code>/style naam</code>.\n"
        f"{pe(3)} Inline: <code>@bot naam</code>"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def generate_for(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str) -> None:
    data = session(context)
    if too_fast(data):
        await update.effective_message.reply_text("Ruko 2 sec, phir try karo.")
        return
    data["name"] = _clean_name(name)
    rebuild(data)
    await send_page(update.effective_message, data)
    chat = update.effective_chat
    if chat and chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        storage.add_group(chat.id)


def _clean_name(name: str) -> str:
    return (name or "").strip()[:NAME_LIMIT] or "Ashu"


async def font_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = session(context)
    if context.args:
        name = " ".join(context.args)
    else:
        name = data.get("name", "Ashu")
        if update.effective_chat and update.effective_chat.type != ChatType.PRIVATE:
            await update.message.reply_text(
                "Group mein aise use karo:\n<code>/style Harry</code>",
                parse_mode="HTML",
            )
            return
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

    if payload == "nav|cats":
        await query.message.reply_text(
            f"{pe(1)} Category choose karo",
            reply_markup=category_kb(data.get("category", "all")),
            parse_mode="HTML",
        )
        return

    if payload == "nav|new":
        await query.message.reply_text("Naya naam bhejo (PM) ya /style naam")
        return

    if payload == "nav|more":
        data["offset"] = min(data.get("offset", 0) + BATCH, max(len(data.get("rows", [])) - 1, 0))
        await send_page(query.message, data, edit=True)
        return

    if payload == "nav|back":
        data["offset"] = max(data.get("offset", 0) - BATCH, 0)
        await send_page(query.message, data, edit=True)


async def on_inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query
    name = _clean_name(query.query or "Ashu")
    rows = build_preview(name, 40)
    results = []
    for item in rows[:40]:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=item[:60],
                input_message_content=InputTextMessageContent(item),
                description=f"Style for {name}",
            )
        )
    await query.answer(results, cache_time=10, is_personal=True)


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
            await context.bot.send_message(
                chat_id,
                text,
                reply_markup=markup,
                parse_mode="HTML",
            )
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
    app.add_handler(InlineQueryHandler(on_inline))
    app.add_handler(ChatMemberHandler(on_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
            on_private_name,
        )
    )
    app.add_error_handler(on_error)

    job_queue = app.job_queue
    if job_queue:
        job_queue.run_repeating(
            hourly_promo,
            interval=max(PROMO_HOURS, 0.25) * 3600,
            first=60,
            name="hourly-promo",
        )
    else:
        log.warning("JobQueue missing. Install python-telegram-bot[job-queue]")

    log.info("Stylish Name Bot online")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
