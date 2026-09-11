import asyncio
import html
import logging
import os
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatMemberStatus, ChatType
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
from studio import FONTS, MARKS, ORNAMENTS, PREFIXES, SUFFIXES, bios, catalog, compose

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
log = logging.getLogger("stylish-bot")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_URL = os.getenv("OWNER_URL", "https://t.me/SANATANI_BACCHA")
SUPPORT_URL = os.getenv("SUPPORT_URL", "https://t.me/HARRYASHU")
STYLE_URL = os.getenv("STYLE_URL", "https://t.me/TG_BIO_STYLE")
MUSIC_URL = os.getenv("MUSIC_URL", "https://t.me/PRAGYA_ROBOT")
FORCE_CHANNEL = os.getenv("FORCE_CHANNEL", "TG_BIO_STYLE").lstrip("@").replace("https://t.me/", "")
ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").replace(" ", "").split(",") if x.isdigit()}
BOT_TITLE = "Stylish Name Maker Bot"
PROMO_HOURS = float(os.getenv("PROMO_HOURS", "1"))
PAGE_SIZE = 10

EMOJI_IDS = ["6057848605601963652", "6124902618574625426", "6124898345082165755", "6125399112499075549", "6197330889765033702"]
FB = ["\U0001F44D", "\u2728", "\U0001F525", "\U0001F48E", "\U0001F451"]
CATS = (
    ("premium", "\U0001F451 PREMIUM DESIGN (156 Styles)"),
    ("aesthetic", "\u2728 Aesthetic Art Styles (107 Styles)"),
    ("live", "\U0001F3AC Live Design (15 Styles)"),
    ("hindi", "\U0001F1EE\U0001F1F3 Hindi Live Design"),
)

def pe(i: int) -> str:
    return f'<tg-emoji emoji-id="{EMOJI_IDS[i % 5]}">{FB[i % 5]}</tg-emoji>'

def ejoin(*xs: int) -> str:
    return "".join(pe(i) for i in xs)

def default_edit() -> dict:
    return {"prefix": PREFIXES[5], "suffix": SUFFIXES[5], "title": "", "font": "bold", "underline": False, "spacing": "compact", "separator": " ", "ornament": "", "marks": "", "crown": False}

def session(context: ContextTypes.DEFAULT_TYPE) -> dict:
    d = context.user_data
    d.setdefault("mode", "menu")
    d.setdefault("name", "Harry")
    d.setdefault("category", "premium")
    d.setdefault("page", 0)
    d.setdefault("rows", [])
    d.setdefault("picked", "")
    d.setdefault("edit", default_edit())
    d.setdefault("bulk_n", 3)
    d.setdefault("bulk_names", [])
    d.setdefault("bulk_mode", "diff")
    return d

def menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("\u270f\ufe0f \U0001d40c\U0001d41a\U0001d424\U0001d41e \U0001d40c\U0001d432 \U0001d40d\U0001d41a\U0001d426\U0001d41e", callback_data="menu|name"), InlineKeyboardButton("\U0001F4DD \U0001d401\U0001d408\U0001d40e", callback_data="menu|bio")],
        [InlineKeyboardButton("\U0001F680 \U0001d401\U0001d42e\U0001d425\U0001d424 \U0001d40d\U0001d41a\U0001d426\U0001d41e\U0001d42c", callback_data="menu|bulk"), InlineKeyboardButton("? \U0001d407\U0001d41e\U0001d425\U0001d429", callback_data="menu|help")],
        [InlineKeyboardButton("\U0001F3B5 Music Bot", url=MUSIC_URL), InlineKeyboardButton("\U0001F3A8 Bio Style", url=STYLE_URL)],
        [InlineKeyboardButton("\U0001F451 Owner", url=OWNER_URL), InlineKeyboardButton("\U0001F496 Channel", url=SUPPORT_URL)],
    ])

def fsub_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("\U0001F4E2 Join TG_BIO_STYLE", url=STYLE_URL)],
        [InlineKeyboardButton("\u2705 Verify / Try Again", callback_data="fsub|ok")],
        [InlineKeyboardButton("\U0001F3B5 Music Bot", url=MUSIC_URL), InlineKeyboardButton("\U0001F451 Owner", url=OWNER_URL)],
    ])

def cat_kb() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(label, callback_data=f"cat|{key}")] for key, label in CATS]
    rows.append([InlineKeyboardButton("New Name", callback_data="menu|name"), InlineKeyboardButton("Main Menu", callback_data="menu|home")])
    return InlineKeyboardMarkup(rows)

def styles_kb(rows: list[str], page: int) -> InlineKeyboardMarkup:
    start = page * PAGE_SIZE
    chunk = rows[start:start + PAGE_SIZE]
    buttons = []
    for i, item in enumerate(chunk):
        idx = start + i
        label = f"{i + 1}. {item}"
        if len(label) > 64:
            label = label[:61] + "..."
        buttons.append([InlineKeyboardButton(label, callback_data=f"pick|{idx}")])
    total_pages = max((len(rows) + PAGE_SIZE - 1) // PAGE_SIZE, 1)
    buttons.append([InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"), InlineKeyboardButton("Next >", callback_data="page|next")])
    buttons.append([InlineKeyboardButton("< Back", callback_data="page|back"), InlineKeyboardButton("New Name", callback_data="menu|name"), InlineKeyboardButton("Main Menu", callback_data="menu|home")])
    return InlineKeyboardMarkup(buttons)

def picked_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Copy Code", callback_data="act|copy"), InlineKeyboardButton("Edit Components", callback_data="act|edit")],
        [InlineKeyboardButton("Try Another", callback_data="act|another"), InlineKeyboardButton("New Name", callback_data="menu|name")],
        [InlineKeyboardButton("< Back", callback_data="page|stay"), InlineKeyboardButton("Main Menu", callback_data="menu|home")],
    ])

def editor_kb(parts: dict) -> InlineKeyboardMarkup:
    flag = lambda v: "ON" if v else "OFF"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Prefix", callback_data="ed|prefix"), InlineKeyboardButton("Title", callback_data="ed|title")],
        [InlineKeyboardButton(f"Font: {parts.get('font')}", callback_data="ed|font"), InlineKeyboardButton(f"Underline: {flag(parts.get('underline'))}", callback_data="ed|under")],
        [InlineKeyboardButton(f"Spacing: {parts.get('spacing')}", callback_data="ed|space"), InlineKeyboardButton("Suffix", callback_data="ed|suffix")],
        [InlineKeyboardButton("Ornament", callback_data="ed|orn"), InlineKeyboardButton("Marks", callback_data="ed|marks")],
        [InlineKeyboardButton(f"Crown: {flag(parts.get('crown'))}", callback_data="ed|crown"), InlineKeyboardButton("Copy Final", callback_data="act|copy")],
        [InlineKeyboardButton("Change Design", callback_data="act|another")],
        [InlineKeyboardButton("Done / Save", callback_data="act|done")],
        [InlineKeyboardButton("< Styles", callback_data="page|stay"), InlineKeyboardButton("Main Menu", callback_data="menu|home")],
    ])

def bulk_count_kb() -> InlineKeyboardMarkup:
    nums = [2, 3, 4, 5, 8, 10]
    row, rows = [], []
    for n in nums:
        row.append(InlineKeyboardButton(f"{n} Names", callback_data=f"bulk|{n}"))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton("Main Menu", callback_data="menu|home")])
    return InlineKeyboardMarkup(rows)

def bulk_result_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Next Styles", callback_data="bulkact|next"), InlineKeyboardButton("Category", callback_data="bulkact|cat")],
        [InlineKeyboardButton("Edit Components", callback_data="act|edit"), InlineKeyboardButton("Same Design", callback_data="bulkact|same")],
        [InlineKeyboardButton("Copy All", callback_data="bulkact|copy"), InlineKeyboardButton("New Batch", callback_data="menu|bulk")],
        [InlineKeyboardButton("Main Menu", callback_data="menu|home")],
    ])

def welcome_html() -> str:
    return (
        f"{ejoin(1, 3, 4)}\n"
        f"<b>Welcome to {html.escape(BOT_TITLE)}!</b>\n\n"
        f"{pe(4)} <b>VIP Premium and Aesthetic Name Studio</b>\n"
        f"================\n"
        f"{pe(2)} 145+ Handcrafted Signature Styles\n"
        f"Aesthetic, Hindi and Religious Bio Maker\n"
        f"================\n\n"
        f"{pe(0)} Niche diye gaye buttons se option select karein:"
    )

def help_html() -> str:
    return (
        f"{pe(2)} <b>1. Name Design Steps</b>\n"
        f"01 Start \u2014 Make My Name\n02 Send \u2014 apna naam bhejo\n03 Category \u2014 Premium / Aesthetic\n04 Choose \u2014 styles browse\n05 Copy \u2014 button dabao\n06 Edit \u2014 prefix suffix font\n\n"
        f"{pe(3)} <b>2. VIP Bio Design</b>\n01 BIO button\n02 Vibe choose\n03 Custom text\n04 Refresh\n05 Copy"
    )

async def is_member(bot, user_id: int) -> bool:
    if not storage.fsub_enabled() or not FORCE_CHANNEL:
        return True
    if user_id in ADMIN_IDS:
        return True
    try:
        member = await bot.get_chat_member(f"@{FORCE_CHANNEL}", user_id)
        return member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except TelegramError as err:
        log.info("fsub check failed: %s", err)
        return False

async def ask_fsub(target) -> None:
    await target.reply_text(
        f"{pe(4)} <b>Pehle channel join karo</b>\n{pe(0)} Join ke baad Verify dabao, tab start khulega.\n{pe(2)} Channel: @{html.escape(FORCE_CHANNEL)}",
        parse_mode="HTML",
        reply_markup=fsub_kb(),
    )

async def play_boot(msg) -> None:
    frames = [
        f"{ejoin(3, 4)} <b>{html.escape(BOT_TITLE)}</b>\n\n[          ] 10%\n{pe(4)} Loading VIP styles...",
        f"{ejoin(3, 4)} <b>{html.escape(BOT_TITLE)}</b>\n\n[=====     ] 50%\n{pe(4)} Loading 145+ VIP Custom Styles...",
        f"{ejoin(1, 2)} <b>INITIALIZING ART ENGINE</b>\n\n[========  ] 80%\nPreparing Bio and Name Studio...",
        f"{ejoin(4, 1)} <b>READY TO DESIGN</b>\n\n[==========] 100%\nLaunching Interactive Studio...",
    ]
    sent = await msg.reply_text(frames[0], parse_mode="HTML")
    for text in frames[1:]:
        await asyncio.sleep(0.28)
        try:
            await sent.edit_text(text, parse_mode="HTML")
        except TelegramError:
            break
    await asyncio.sleep(0.2)
    try:
        await sent.delete()
    except TelegramError:
        pass

async def send_home(target) -> None:
    await target.reply_text(welcome_html(), parse_mode="HTML", reply_markup=menu_kb())

async def gated_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user = update.effective_user
    if not user:
        return False
    chat = update.effective_chat
    if chat and chat.type != ChatType.PRIVATE:
        return True
    if await is_member(context.bot, user.id):
        return True
    await ask_fsub(update.effective_message)
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if chat and chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        storage.add_group(chat.id)
        await update.message.reply_text(f"{pe(2)} Group mein sirf <code>/style naam</code>", parse_mode="HTML")
        return
    if not await gated_start(update, context):
        return
    await play_boot(update.message)
    session(context)["mode"] = "menu"
    await send_home(update.message)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await gated_start(update, context):
        return
    await update.message.reply_text(help_html(), parse_mode="HTML", reply_markup=menu_kb())

async def open_styles(target, data: dict, edit: bool = False) -> None:
    data["rows"] = catalog(data["name"], data["category"])
    max_page = max((len(data["rows"]) - 1) // PAGE_SIZE, 0)
    data["page"] = min(max(data["page"], 0), max_page)
    pages = max_page + 1
    text = f"<b>Name:</b> {html.escape(data['name'])}\n<b>Category:</b> {data['category'].title()}\n<b>Page:</b> {data['page'] + 1}/{pages}\n\n{pe(0)} Click on any style below to copy it:"
    kb = styles_kb(data["rows"], data["page"])
    if edit:
        await target.edit_text(text, parse_mode="HTML", reply_markup=kb)
        return
    await target.reply_text(text, parse_mode="HTML", reply_markup=kb)

async def font_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    data = session(context)
    if not context.args:
        if chat and chat.type != ChatType.PRIVATE:
            await update.message.reply_text("Group: <code>/style Harry</code>", parse_mode="HTML")
            return
        data["mode"] = "wait_name"
        await update.message.reply_text("Kripya wo name enter karein jo aap design karwana chahte hain:")
        return
    data["name"] = " ".join(context.args)[:24]
    data["category"] = "premium"
    data["page"] = 0
    data["mode"] = "styles"
    if chat and chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        storage.add_group(chat.id)
    await open_styles(update.message, data)

async def send_bulk(target, data: dict) -> None:
    names = data.get("bulk_names") or [data["name"]]
    same = data.get("bulk_mode") == "same"
    lines = [f"{pe(2)} <b>BULK NAMES STUDIO ({len(names)} Names)</b>", ""]
    data["rows"] = []
    page = data.get("page", 0)
    for i, nm in enumerate(names):
        pack = catalog(nm, data.get("category", "premium"))
        style = pack[0] if same else pack[page % max(len(pack), 1)]
        data["rows"].append(style)
        lines.append(f"<b>{i + 1}. {html.escape(nm.upper())}</b>\n<code>{html.escape(style)}</code>")
    lines.append(f"\n{pe(0)} Copy All / Next Styles")
    await target.reply_text("\n".join(lines), parse_mode="HTML", reply_markup=bulk_result_kb())

async def on_private_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await gated_start(update, context):
        return
    data = session(context)
    text = (update.message.text or "").strip()
    if not text:
        return
    mode = data.get("mode")
    if mode == "wait_bio":
        data["name"] = text[:28]
        data["rows"] = bios(data["name"])
        data["page"] = 0
        data["mode"] = "styles"
        data["category"] = "aesthetic"
        await open_styles(update.message, data)
        return
    if mode == "wait_bulk":
        names = [p.strip()[:18] for p in text.replace(",", " ").split() if p.strip()]
        data["bulk_names"] = names[: data.get("bulk_n", 3)]
        await send_bulk(update.message, data)
        return
    data["name"] = text[:24]
    data["mode"] = "pick_cat"
    await update.message.reply_text(f"<b>Name:</b> {html.escape(data['name'])}\n{pe(0)} Kripya niche 4 category se select karein:", parse_mode="HTML", reply_markup=cat_kb())

def cycle(seq, cur):
    if cur in seq:
        return seq[(seq.index(cur) + 1) % len(seq)]
    return seq[1] if len(seq) > 1 else seq[0]

async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = session(context)
    payload = query.data or ""
    user = update.effective_user
    if payload.startswith("fsub|"):
        if user and await is_member(context.bot, user.id):
            await query.answer("Verified")
            try:
                await query.message.delete()
            except TelegramError:
                pass
            await play_boot(query.message)
            await send_home(query.message)
        else:
            await query.answer("Pehle channel join karo", show_alert=True)
        return
    if user and update.effective_chat and update.effective_chat.type == ChatType.PRIVATE:
        if not await is_member(context.bot, user.id):
            await query.answer("Channel join required", show_alert=True)
            await ask_fsub(query.message)
            return
    await query.answer()
    if payload == "noop":
        return
    if payload == "menu|home":
        data["mode"] = "menu"
        await query.message.reply_text(welcome_html(), parse_mode="HTML", reply_markup=menu_kb())
        return
    if payload == "menu|name":
        data["mode"] = "wait_name"
        await query.message.reply_text("Kripya wo name enter karein jo aap design karwana chahte hain:")
        return
    if payload == "menu|bio":
        data["mode"] = "wait_bio"
        await query.message.reply_text("Bio ke liye naam / text bhejo:")
        return
    if payload == "menu|bulk":
        data["mode"] = "bulk_n"
        await query.message.reply_text("Ek saath multiple names stylish bana sakte ho.\nKitne names? (2-10)", reply_markup=bulk_count_kb())
        return
    if payload == "menu|help":
        await query.message.reply_text(help_html(), parse_mode="HTML", reply_markup=menu_kb())
        return
    if payload.startswith("bulk|"):
        data["bulk_n"] = int(payload.split("|")[1])
        data["mode"] = "wait_bulk"
        await query.message.reply_text(f"{data['bulk_n']} names bhejo space ya comma se.\nExample: <code>Whey Ashy Rahi</code>", parse_mode="HTML")
        return
    if payload.startswith("cat|"):
        data["category"] = payload.split("|", 1)[1]
        data["page"] = 0
        data["mode"] = "styles"
        await open_styles(query.message, data, edit=True)
        return
    if payload.startswith("page|"):
        act = payload.split("|", 1)[1]
        pages = max((len(data["rows"]) + PAGE_SIZE - 1) // PAGE_SIZE, 1)
        if act == "next":
            data["page"] = min(data["page"] + 1, pages - 1)
        elif act == "back":
            data["page"] = max(data["page"] - 1, 0)
        await open_styles(query.message, data, edit=True)
        return
    if payload.startswith("pick|"):
        idx = int(payload.split("|", 1)[1])
        if 0 <= idx < len(data["rows"]):
            data["picked"] = data["rows"][idx]
            await query.message.reply_text(f"<b>Design Ready!</b> {pe(1)}\n\n<code>{html.escape(data['picked'])}</code>", parse_mode="HTML", reply_markup=picked_kb())
        return
    if payload == "act|copy":
        text = data.get("picked") or (data["rows"][0] if data["rows"] else "")
        if text:
            await query.message.reply_text(f"{pe(3)} Done! Final design:\n<code>{html.escape(text)}</code>", parse_mode="HTML")
        return
    if payload == "act|edit":
        parts = data["edit"]
        preview = compose(data["name"], parts)
        data["picked"] = preview
        await query.message.reply_text(f"<b>DESIGN EDITOR</b>\n\nPreview:\n<code>{html.escape(preview)}</code>\n\n{pe(0)} Component click karke edit karo:", parse_mode="HTML", reply_markup=editor_kb(parts))
        return
    if payload == "act|another":
        pages = max((len(data["rows"]) + PAGE_SIZE - 1) // PAGE_SIZE, 1)
        data["page"] = (data["page"] + 1) % pages
        await open_styles(query.message, data, edit=True)
        return
    if payload == "act|done":
        preview = compose(data["name"], data["edit"])
        data["picked"] = preview
        await query.message.reply_text(f"Done! Aapka final design:\n<code>{html.escape(preview)}</code>", parse_mode="HTML", reply_markup=picked_kb())
        return
    if payload.startswith("ed|"):
        key = payload.split("|", 1)[1]
        parts = data["edit"]
        if key == "prefix":
            parts["prefix"] = cycle(PREFIXES, parts.get("prefix") or "")
        elif key == "suffix":
            parts["suffix"] = cycle(SUFFIXES, parts.get("suffix") or "")
        elif key == "font":
            parts["font"] = cycle(FONTS, parts.get("font") or "bold")
        elif key == "under":
            parts["underline"] = not parts.get("underline")
        elif key == "space":
            parts["spacing"] = "wide" if parts.get("spacing") != "wide" else "compact"
        elif key == "orn":
            parts["ornament"] = cycle(ORNAMENTS, parts.get("ornament") or "")
        elif key == "marks":
            parts["marks"] = cycle(MARKS, parts.get("marks") or "")
        elif key == "crown":
            parts["crown"] = not parts.get("crown")
        elif key == "title":
            parts["title"] = "" if parts.get("title") else "VIP"
        preview = compose(data["name"], parts)
        data["picked"] = preview
        try:
            await query.message.edit_text(f"<b>DESIGN EDITOR</b>\n\nPreview:\n<code>{html.escape(preview)}</code>\n\n{pe(0)} Component click karke edit karo:", parse_mode="HTML", reply_markup=editor_kb(parts))
        except TelegramError:
            pass
        return
    if payload.startswith("bulkact|"):
        act = payload.split("|", 1)[1]
        if act == "next":
            data["page"] = data.get("page", 0) + 1
            await send_bulk(query.message, data)
        elif act == "cat":
            await query.message.reply_text("Category choose karo:", reply_markup=cat_kb())
        elif act == "same":
            data["bulk_mode"] = "same" if data.get("bulk_mode") != "same" else "diff"
            await send_bulk(query.message, data)
        elif act == "copy":
            blob = "\n".join(data.get("rows") or [])
            await query.message.reply_text(f"<code>{html.escape(blob)}</code>", parse_mode="HTML")

async def on_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    member = update.my_chat_member
    if not member or member.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return
    status = member.new_chat_member.status
    if status in ("member", "administrator"):
        storage.add_group(member.chat.id)
    elif status in ("left", "kicked"):
        storage.remove_group(member.chat.id)

async def hourly_promo(context: ContextTypes.DEFAULT_TYPE) -> None:
    text = welcome_html() + f"\n\n{pe(4)} Group: <code>/style naam</code>"
    for chat_id in storage.list_groups():
        try:
            await context.bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=menu_kb())
            await asyncio.sleep(0.2)
        except Forbidden:
            storage.remove_group(chat_id)
        except RetryAfter as err:
            await asyncio.sleep(err.retry_after + 1)
        except TelegramError as err:
            log.info("promo skip %s: %s", chat_id, err)

async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.exception("update failed: %s", context.error)

def is_admin(user) -> bool:
    return bool(user and user.id in ADMIN_IDS)

async def fsub_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("Ye command sirf owner ke liye hai.")
        return
    arg = (context.args[0].lower() if context.args else "")
    if arg in ("on", "1", "true", "enable"):
        storage.set_fsub(True)
        await update.message.reply_text(f"{pe(4)} Force join <b>ON</b>\nChannel: @{html.escape(FORCE_CHANNEL)}", parse_mode="HTML")
        return
    if arg in ("off", "0", "false", "disable"):
        storage.set_fsub(False)
        await update.message.reply_text(f"{pe(2)} Force join <b>OFF</b>", parse_mode="HTML")
        return
    state = "ON" if storage.fsub_enabled() else "OFF"
    await update.message.reply_text(f"Force join abhi <b>{state}</b>\n/fsub on\n/fsub off", parse_mode="HTML")

async def post_init(app) -> None:
    global BOT_TITLE
    me = await app.bot.get_me()
    BOT_TITLE = me.first_name or me.username or BOT_TITLE
    log.info("bot title = %s", BOT_TITLE)

def main() -> None:
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN missing")
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("fsub", fsub_cmd))
    app.add_handler(CommandHandler("font", font_cmd))
    app.add_handler(CommandHandler("style", font_cmd))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(ChatMemberHandler(on_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, on_private_text))
    app.add_error_handler(on_error)
    jq = app.job_queue
    if jq:
        jq.run_repeating(hourly_promo, interval=max(PROMO_HOURS, 0.25) * 3600, first=60, name="hourly-promo")
    log.info("Stylish Name Bot online")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
