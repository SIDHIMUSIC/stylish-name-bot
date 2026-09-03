import os
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from nick_styles import build_all

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BATCH = 12
PER_MSG = 8


def session(context):
    d = context.user_data
    d.setdefault("name", "Ashu")
    d.setdefault("offset", 0)
    return d


def continue_kb():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("\u25b6 CONTINUE", callback_data="more")]]
    )


async def send_batch(target, name, offset):
    rows = build_all(name)
    chunk = rows[offset : offset + BATCH]
    for i in range(0, len(chunk), PER_MSG):
        piece = chunk[i : i + PER_MSG]
        await target.reply_text("\n\n".join(piece))
        await asyncio.sleep(0.05)
    new_offset = offset + len(chunk)
    more = new_offset < len(rows)
    if more:
        left = len(rows) - new_offset
        await target.reply_text(
            f"\u25b6 CONTINUE  \u00b7  {left} more  \u00b7  {len(rows)} total",
            reply_markup=continue_kb(),
        )
    else:
        await target.reply_text("Khatam. Naya naam bhejo.")
    return new_offset


async def start(update, context):
    await update.message.reply_text(
        "Naam bhejo. Stylish nicks aa jayenge.\n"
        "/font Naam  \u00b7  /style Naam"
    )


async def on_name(update, context):
    data = session(context)
    data["name"] = (update.message.text or "").strip()[:28] or "Ashu"
    data["offset"] = 0
    data["offset"] = await send_batch(update.message, data["name"], 0)


async def font_cmd(update, context):
    data = session(context)
    if context.args:
        data["name"] = " ".join(context.args)[:28]
    data["offset"] = 0
    data["offset"] = await send_batch(update.message, data["name"], 0)


async def on_continue(update, context):
    query = update.callback_query
    await query.answer()
    data = session(context)
    try:
        await query.message.delete()
    except Exception:
        pass
    data["offset"] = await send_batch(
        query.message, data.get("name", "Ashu"), data.get("offset", 0)
    )


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN missing")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("font", font_cmd))
    app.add_handler(CommandHandler("style", font_cmd))
    app.add_handler(CallbackQueryHandler(on_continue, pattern="^more$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_name))
    print("Stylish Name Bot online")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
