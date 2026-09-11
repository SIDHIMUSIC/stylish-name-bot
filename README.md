# Stylish Name Bot

Telegram stylish name generator — Unicode fonts, frames, categories, pagination, inline mode.

## Behaviour

- **Private chat:** send any name, bot replies with styles.
- **Groups:** plain text is ignored. Use `/style Harry` or `/font Harry`.
- **Inline:** `@yourbot Harry`
- **Hourly promo** in groups where the bot is added (premium custom emoji).

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# set TELEGRAM_BOT_TOKEN
python bot.py
```

BotFather: enable **Inline mode**. Privacy mode can stay ON because groups only use commands.

## Env

```
TELEGRAM_BOT_TOKEN=
OWNER_URL=https://t.me/SANATANI_BACHA
SUPPORT_URL=https://t.me/HARRYASHU
STYLE_URL=https://t.me/TG_BIO_STYLE
PROMO_HOURS=1
DATA_PATH=data/chats.json
```

Custom emoji IDs used in start + hourly promo:

- `6057848605601963652`
- `6124902618574625426`
- `6124898345082165755`
- `6125399112499075549`
- `6197330889765033702`
