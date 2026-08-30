import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    ContextTypes,
    filters,
)
from fonts import generate_all, CATEGORIES, FRAMES, style_text, framed

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER = os.getenv("OWNER", "@SANATANI_BACHA")
PER_PAGE = 8


def session(context):
    data = context.user_data
    data.setdefault("name", "Harry")
    data.setdefault("cat", "all")
    data.setdefault("frame", "none")
    data.setdefault("page", 0)
    return data


def items_for(data):
    return generate_all(data["name"], data["cat"], data["frame"])


def page_text(data):
    rows = items_for(data)
    page = data["page"]
    start = page * PER_PAGE
    chunk = rows[start:start + PER_PAGE]
    total_pages = max(1, (len(rows) + PER_PAGE - 1) // PER_PAGE)
    lines = [
        f"✦ <b>STYLISH NAME</b>",
        f"name: <code>{data['name']}</code>",
        f"style: <code>{data['cat']}</code> • frame: <code>{data['frame']}</code>",
        f"page {page + 1}/{total_pages} • {len(rows)} fonts",
        "━" * 18,
        "",
    ]
    for i, (style, val) in enumerate(chunk, start + 1):
        lines.append(f"{i}. <code>{val}</code>")
    lines.append("\nTap a style to copy.")
    return "\n".join(lines), rows, start, chunk, total_pages


def keyboard(data, start, chunk, total_pages):
    buttons = []
    row = []
    for i, (style, _val) in enumerate(chunk):
        row.append(InlineKeyboardButton(str(start + i + 1), callback_data=f"p:{start + i}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    nav = []
    if data["page"] > 0:
        nav.append(InlineKeyboardButton("Prev", callback_data="nav:prev"))
    if data["page"] + 1 < total_pages:
        nav.append(InlineKeyboardButton("Next", callback_data="nav:next"))
    if nav:
        buttons.append(nav)
    cats = [InlineKeyboardButton(c, callback_data=f"cat:{c}") for c in ("cute", "royal", "dark", "gaming", "aesthetic", "all")]
    buttons.append(cats[:3])
    buttons.append(cats[3:])
    frames = [InlineKeyboardButton(f, callback_data=f"fr:{f}") for f in ("none", "royal", "star", "heart", "crown", "game")]
    buttons.append(frames[:3])
    buttons.append(frames[3:])
    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✦ <b>STYLISH NAME GENERATOR</b>\n\n"
        "Name bhejo, 50+ Unicode styles milenge.\n"
        "Category + frame change karke copy tap karo.\n\n"
        "<code>/font Harry</code>\n"
        "Inline: <code>@bot Harry</code> kisi bhi chat me",
        parse_mode="HTML",
    )


async def font_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = session(context)
    if context.args:
        data["name"] = " ".join(context.args)[:32]
        data["page"] = 0
    await send_panel(update.message, context)


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = session(context)
    data["name"] = update.message.text.strip()[:32]
    data["page"] = 0
    await send_panel(update.message, context)


async def send_panel(message, context):
    data = session(context)
    text, _rows, start, chunk, total = page_text(data)
    await message.reply_text(text, parse_mode="HTML", reply_markup=keyboard(data, start, chunk, total))


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = session(context)
    raw = query.data or ""
    if raw.startswith("nav:"):
        if raw.endswith("prev"):
            data["page"] = max(0, data["page"] - 1)
        else:
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
            return await query.message.reply_text(
                f"<b>{style}</b>\n<code>{val}</code>\n\nLong press → Copy", parse_mode="HTML"
            )
    text, _rows, start, chunk, total = page_text(data)
    try:
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=keyboard(data, start, chunk, total))
    except Exception:
        pass


async def inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = (update.inline_query.query or "Harry").strip()[:32] or "Harry"
    rows = generate_all(q, "all", "none")[:20]
    results = []
    for i, (style, val) in enumerate(rows):
        results.append(
            InlineQueryResultArticle(
                id=str(i),
                title=style,
                description=val,
                input_message_content=InputTextMessageContent(val),
            )
        )
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
