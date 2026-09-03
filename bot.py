import os
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    filters,
)
from fonts import generate_all, generate_random

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PER_PAGE = 8


def session(context):
    d = context.user_data
    d.setdefault("name", "Harry")
    d.setdefault("cat", "all")
    d.setdefault("frame", "none")
    d.setdefault("page", 0)
    d.setdefault("mode", "list")
    return d


def items_for(data):
    if data.get("mode") == "random":
        return generate_random(data["name"], 24)
    return generate_all(data["name"], data["cat"], data["frame"])


def _esc(text):
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def page_text(data):
    rows = items_for(data)
    page = data["page"]
    start = page * PER_PAGE
    chunk = rows[start:start + PER_PAGE]
    total = max(1, (len(rows) + PER_PAGE - 1) // PER_PAGE)
    lines = [
        "\u2728 <b>STYLISH NAME</b>",
        f"\U0001F4DD <b>{_esc(data['name'])}</b>",
        f"\U0001F39B {_esc(data['cat'])}  \u00b7  \U0001F5BC {_esc(data['frame'])}  \u00b7  {len(rows)} styles",
        f"\U0001F4C4 {page + 1}/{total}",
        "",
    ]
    for i, (style, val) in enumerate(chunk, start + 1):
        lines.append(f"<b>{i}.</b> <code>{_esc(val)}</code>")
        lines.append(f"    <i>{_esc(style)}</i>")
    lines.append("\nTap number \u2192 copy-ready message")
    return "\n".join(lines), start, chunk, total


def keyboard(data, start, chunk, total):
    buttons, row = [], []
    for i, _ in enumerate(chunk):
        row.append(InlineKeyboardButton(str(start + i + 1), callback_data="p:%s" % (start + i)))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    nav = []
    if data["page"] > 0:
        nav.append(InlineKeyboardButton("\u25c0 Prev", callback_data="nav:prev"))
    nav.append(InlineKeyboardButton("\U0001F3B2 Random", callback_data="act:rand"))
    if data["page"] + 1 < total:
        nav.append(InlineKeyboardButton("Next \u25b6", callback_data="nav:next"))
    buttons.append(nav)
    buttons.append([
        InlineKeyboardButton("Cute", callback_data="cat:cute"),
        InlineKeyboardButton("Royal", callback_data="cat:royal"),
        InlineKeyboardButton("Dark", callback_data="cat:dark"),
    ])
    buttons.append([
        InlineKeyboardButton("Gaming", callback_data="cat:gaming"),
        InlineKeyboardButton("Aesthetic", callback_data="cat:aesthetic"),
        InlineKeyboardButton("Nature", callback_data="cat:nature"),
        InlineKeyboardButton("All", callback_data="cat:all"),
    ])
    buttons.append([
        InlineKeyboardButton("Star", callback_data="fr:star"),
        InlineKeyboardButton("Heart", callback_data="fr:heart"),
        InlineKeyboardButton("Crown", callback_data="fr:crown"),
        InlineKeyboardButton("Royal", callback_data="fr:royal"),
    ])
    buttons.append([
        InlineKeyboardButton("Game", callback_data="fr:game"),
        InlineKeyboardButton("Flower", callback_data="fr:flower"),
        InlineKeyboardButton("Bolt", callback_data="fr:bolt"),
        InlineKeyboardButton("Plain", callback_data="fr:none"),
    ])
    return InlineKeyboardMarkup(buttons)


async def start(update, context):
    await update.message.reply_text(
        "\u2728 <b>Stylish Name Generator</b>\n\n"
        "Naam bhejo \u2014 20+ Unicode fonts + frames.\n\n"
        "\u2022 <code>/font Harry</code>\n"
        "\u2022 <code>/random Harry</code>\n"
        "\u2022 Inline: <code>@YourBot Harry</code>",
        parse_mode=ParseMode.HTML,
    )


async def help_cmd(update, context):
    await update.message.reply_text(
        "<b>Commands</b>\n/start /font /random /style\nYa seedha naam type karo.",
        parse_mode=ParseMode.HTML,
    )


async def font_cmd(update, context):
    data = session(context)
    data["mode"] = "list"
    if context.args:
        data["name"] = " ".join(context.args)[:32]
        data["page"] = 0
    await _send_page(update.message, data)


async def random_cmd(update, context):
    data = session(context)
    data["mode"] = "random"
    if context.args:
        data["name"] = " ".join(context.args)[:32]
    data["page"] = 0
    await _send_page(update.message, data)


async def on_text(update, context):
    data = session(context)
    data["name"] = update.message.text.strip()[:32]
    data["page"] = 0
    data["mode"] = "list"
    await _send_page(update.message, data)


async def _send_page(message, data):
    text, start, chunk, total = page_text(data)
    await message.reply_text(text, reply_markup=keyboard(data, start, chunk, total), parse_mode=ParseMode.HTML)


async def callback(update, context):
    query = update.callback_query
    data = session(context)
    raw = query.data or ""
    if raw.startswith("nav:prev"):
        data["page"] = max(0, data["page"] - 1)
        await query.answer()
    elif raw.startswith("nav:next"):
        data["page"] += 1
        await query.answer()
    elif raw.startswith("cat:"):
        data["cat"] = raw.split(":", 1)[1]
        data["page"] = 0
        data["mode"] = "list"
        await query.answer(data["cat"])
    elif raw.startswith("fr:"):
        data["frame"] = raw.split(":", 1)[1]
        data["page"] = 0
        data["mode"] = "list"
        await query.answer(data["frame"])
    elif raw.startswith("act:rand"):
        data["mode"] = "random"
        data["page"] = 0
        await query.answer("random mix")
    elif raw.startswith("p:"):
        idx = int(raw.split(":", 1)[1])
        rows = items_for(data)
        if 0 <= idx < len(rows):
            style, val = rows[idx]
            await query.answer("ok")
            return await query.message.reply_text(
                f"<b>{_esc(style)}</b>\n\n<code>{_esc(val)}</code>\n\nLong press to copy.",
                parse_mode=ParseMode.HTML,
            )
        await query.answer()
        return
    else:
        await query.answer()
    text, start, chunk, total = page_text(data)
    try:
        await query.edit_message_text(text, reply_markup=keyboard(data, start, chunk, total), parse_mode=ParseMode.HTML)
    except Exception:
        pass


async def inline(update, context):
    q = (update.inline_query.query or "Harry").strip()[:32] or "Harry"
    rows = generate_all(q, "all", "none")[:25]
    extra = generate_random(q, 8)
    seen = {v for _, v in rows}
    for item in extra:
        if item[1] not in seen:
            rows.append(item)
            seen.add(item[1])
    results = [
        InlineQueryResultArticle(
            id=str(i), title=style, description=val,
            input_message_content=InputTextMessageContent(val),
        )
        for i, (style, val) in enumerate(rows[:40])
    ]
    await update.inline_query.answer(results, cache_time=8)


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN missing")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("font", font_cmd))
    app.add_handler(CommandHandler("style", font_cmd))
    app.add_handler(CommandHandler("random", random_cmd))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(InlineQueryHandler(inline))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    print("Stylish Name Bot online")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
