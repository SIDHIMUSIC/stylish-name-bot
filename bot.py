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
from nick_styles import build_all as base_build
from extra_styles import lookalike_fonts, EXTRA_WRAPS, PREFIXES, SUFFIXES

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BATCH = 12
PER_MSG = 8

OWNER_URL = os.getenv("OWNER_URL", "https://t.me/SANATANI_BACCHA")
SUPPORT_URL = os.getenv("SUPPORT_URL", "https://t.me/HARRYASHU")
STYLE_URL = os.getenv("STYLE_URL", "https://t.me/TG_BIO_STYLE")


def build_all(name):
    name = (name or "").strip()[:24] or "Name"
    items = list(base_build(name))
    seen = set(items)

    def add(x):
        x = " ".join(str(x).split()) if "\n" not in str(x) else str(x)
        if x and x not in seen:
            seen.add(x)
            items.append(x)

    for extra in lookalike_fonts(name):
        add(extra)
        add(f"\u2605 {extra} \u2605")
        add(f"\ua9c1 {extra} \ua9c2")
        add(f"\U000132a9 {extra} \U000132aa")
    core = items[:8] or [name]
    for wrap in EXTRA_WRAPS:
        if "{n}" not in wrap:
            continue
        for inner in core[:4]:
            add(wrap.replace("{n}", inner))
    for i, pre in enumerate(PREFIXES):
        suf = SUFFIXES[i % len(SUFFIXES)]
        add(f"{pre} {core[i % len(core)]} {suf}")
    return items


def session(context):
    d = context.user_data
    d.setdefault("name", "Ashu")
    d.setdefault("offset", 0)
    return d


def continue_kb():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("\u25b6 CONTINUE", callback_data="more")]]
    )


def start_kb():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("\U0001f48c Support", url=SUPPORT_URL),
                InlineKeyboardButton("\U0001f451 Owner", url=OWNER_URL),
            ],
            [InlineKeyboardButton("\u2728 Bio Style", url=STYLE_URL)],
        ]
    )


def start_text(who: str) -> str:
    return (
        "\u2728\u2728\u2728  \U0001d407\U0001d404\U0001d418 I AM PREMIUM NAME MAKER BOT  \u2705\u2705\u2705\n"
        "\U0001f48e \U0001f451 \U0001f525 \u26a1 \U0001f48c \U0001f496 \U0001f31f \U0001f680\n\n"
        f"\U0001f44b Welcome, {who}! \U0001f49e\n\n"
        "\U0001f48c Send me your name\n"
        "To make it stylish \u2728\n\n"
        "\u26a1 Generate 3500+ Premium Styles\n"
        "\U0001f3ad Fancy Unicode & VIP Underlines\n"
        "\U0001f48e Aesthetic Emoji Decorations\n"
        "\U0001f680 Fast & Free \u2014 click below to start\n\n"
        "\U0001f451 Owner \u2014 @SANATANI_BACCHA\n"
        "\U0001f4ac Support \u2014 @HARRYASHU\n"
        "\u2728 Style \u2014 @TG_BIO_STYLE"
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
    user = update.effective_user
    who = (user.first_name if user else "Dear")[:24]
    await update.message.reply_text(
        start_text(who),
        reply_markup=start_kb(),
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
