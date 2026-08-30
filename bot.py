import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, filters
from fonts import generate_all, CATEGORIES, FRAMES

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PER_PAGE = 8


def session(context):
    d = context.user_data
    d.setdefault("name", "Harry")
    d.setdefault("cat", "all")
    d.setdefault("frame", "none")
    d.setdefault("page", 0)
    return d


def items_for(data):
    return generate_all(data["name"], data["cat"], data["frame"])


def page_text(data):
    rows = items_for(data)
    page = data["page"]
    start = page * PER_PAGE
    chunk = rows[start:start + PER_PAGE]
    total = max(1, (len(rows) + PER_PAGE - 1) // PER_PAGE)
    lines = [
        "STYLISH NAME",
        "name: " + data["name"],
        "cat: " + data["cat"] + " | frame: " + data["frame"],
        "page %s/%s | %s fonts" % (page + 1, total, len(rows)),
        "", 
    ]
    for i, (style, val) in enumerate(chunk, start + 1):
        lines.append("%s. %s" % (i, val))
    lines.append("\nTap a number to copy.")
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
        nav.append(InlineKeyboardButton("Prev", callback_data="nav:prev"))
    if data["page"] + 1 < total:
        nav.append(InlineKeyboardButton("Next", callback_data="nav:next"))
    if nav:
        buttons.append(nav)
    buttons.append([
        InlineKeyboardButton("cute", callback_data="cat:cute"),
        InlineKeyboardButton("royal", callback_data="cat:royal"),
        InlineKeyboardButton("dark", callback_data="cat:dark"),
    ])
    buttons.append([
        InlineKeyboardButton("gaming", callback_data="cat:gaming"),
        InlineKeyboardButton("aesthetic", callback_data="cat:aesthetic"),
        InlineKeyboardButton("all", callback_data="cat:all"),
    ])
    buttons.append([
        InlineKeyboardButton("star", callback_data="fr:star"),
        InlineKeyboardButton("heart", callback_data="fr:heart"),
        InlineKeyboardButton("crown", callback_data="fr:crown"),
    ])
    buttons.append([
        InlineKeyboardButton("royal frame", callback_data="fr:royal"),
        InlineKeyboardButton("game", callback_data="fr:game"),
        InlineKeyboardButton("plain", callback_data="fr:none"),
    ])
    return InlineKeyboardMarkup(buttons)


async def start(update, context):
    await update.message.reply_text(
        "STYLISH NAME GENERATOR\n\n"
        "Apna naam bhejo.\n"
        "/font Harry\n"
        "Inline: @YourBot Harry"
    )


async def font_cmd(update, context):
    data = session(context)
    if context.args:
        data["name"] = " ".join(context.args)[:32]
        data["page"] = 0
    text, start, chunk, total = page_text(data)
    await update.message.reply_text(text, reply_markup=keyboard(data, start, chunk, total))


async def on_text(update, context):
    data = session(context)
    data["name"] = update.message.text.strip()[:32]
    data["page"] = 0
    text, start, chunk, total = page_text(data)
    await update.message.reply_text(text, reply_markup=keyboard(data, start, chunk, total))


async def callback(update, context):
    query = update.callback_query
    await query.answer()
    data = session(context)
    raw = query.data or ""
    if raw.startswith("nav:prev"):
        data["page"] = max(0, data["page"] - 1)
    elif raw.startswith("nav:next"):
        data["page"] += 1
    elif raw.startswith("cat:"):
        data["cat"] = raw.split(":", 1)[1]
        data["page"] = 0
    elif raw.startswith("fr:"):
        data["frame"] = raw.split(":", 1)[1]
        data["page"] = 0
    elif raw.startswith("p:"):
        idx = int(raw.split(":", 1)[1])
        rows = items_for(data)
        if 0 <= idx < len(rows):
            style, val = rows[idx]
            return await query.message.reply_text("%s\n%s\n\nLong press to copy" % (style, val))
    text, start, chunk, total = page_text(data)
    try:
        await query.edit_message_text(text, reply_markup=keyboard(data, start, chunk, total))
    except Exception:
        pass


async def inline(update, context):
    q = (update.inline_query.query or "Harry").strip()[:32] or "Harry"
    rows = generate_all(q, "all", "none")[:20]
    results = [
        InlineQueryResultArticle(
            id=str(i),
            title=style,
            description=val,
            input_message_content=InputTextMessageContent(val),
        )
        for i, (style, val) in enumerate(rows)
    ]
    await update.inline_query.answer(results, cache_time=5)


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN missing")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("font", font_cmd))
    app.add_handler(CommandHandler("style", font_cmd))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(InlineQueryHandler(inline))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    print("Stylish Name Bot online")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
