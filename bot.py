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
    ApplicationBuilder,
    CallbackQueryHandler,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
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

def ejoin(*xs: int) -> str:
    return "".join(pe(i) for i in xs)

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

def cat_kb() -> InlineKeyboardMarkup: return fancy_cat_kb()
def styles_kb(rows: list[str], page: int) -> InlineKeyboardMarkup: return fancy_styles_kb(rows, page)

def live_kb(parts: dict, rows: list[str], page: int) -> InlineKeyboardMarkup:
    def flag(key: str) -> str: return "ON" if parts.get(key) else "OFF"
    base = list(styles_kb(rows, page).inline_keyboard)
    controls = [
        [btn(f"Prefix: {flag('prefix_on')}", callback_data="live|prefix", style="primary", icon=EMOJI_IDS[0]), btn(f"Suffix: {flag('suffix_on')}", callback_data="live|suffix", style="success", icon=EMOJI_IDS[1])],
        [btn(f"Underline: {flag('underline')}", callback_data="live|underline", style="primary", icon=EMOJI_IDS[2]), btn(f"Emoji: {flag('emoji')}", callback_data="live|emoji", style="success", icon=EMOJI_IDS[3])],
        [btn(f"Font: {parts.get('font', 'bold')}", callback_data="live|font", style="primary", icon=EMOJI_IDS[4]), btn("🔥 Full Stylish", callback_data="live|full", style="success", icon=EMOJI_IDS[2])],
    ]
    return InlineKeyboardMarkup(list(controls) + base)

def picked_kb():
    return InlineKeyboardMarkup([[btn("Copy Code", callback_data="act|copy", style="primary", icon=EMOJI_IDS[3]), btn("Edit Components", callback_data="act|edit", style="success", icon=EMOJI_IDS[1])], [btn("Try Another", callback_data="act|another", style="primary", icon=EMOJI_IDS[2]), btn("New Name", callback_data="menu|name", style="success", icon=EMOJI_IDS[4])], [btn("< Back", callback_data="page|stay", style="primary", icon=EMOJI_IDS[0]), btn("Main Menu", callback_data="menu|home", style="danger", icon=EMOJI_IDS[2])]])

def editor_kb(parts):
    flag=lambda v:"ON" if v else "OFF"
    return InlineKeyboardMarkup([[btn("Prefix",callback_data="ed|prefix",style="primary",icon=EMOJI_IDS[0]),btn("Title",callback_data="ed|title",style="success",icon=EMOJI_IDS[1])],[btn(f"Font: {parts.get('font')}",callback_data="ed|font",style="primary",icon=EMOJI_IDS[3]),btn(f"Underline: {flag(parts.get('underline'))}",callback_data="ed|under",style="success",icon=EMOJI_IDS[2])],[btn(f"Spacing: {parts.get('spacing')}",callback_data="ed|space",style="primary",icon=EMOJI_IDS[4]),btn("Suffix",callback_data="ed|suffix",style="success",icon=EMOJI_IDS[0])],[btn("Ornament",callback_data="ed|orn",style="primary",icon=EMOJI_IDS[1]),btn("Marks",callback_data="ed|marks",style="success",icon=EMOJI_IDS[2])],[btn(f"Crown: {flag(parts.get('crown'))}",callback_data="ed|crown",style="primary",icon=EMOJI_IDS[4]),btn("Copy Final",callback_data="act|copy",style="success",icon=EMOJI_IDS[3])],[btn("Change Design",callback_data="act|another",style="primary",icon=EMOJI_IDS[2])],[btn("Done / Save",callback_data="act|done",style="success",icon=EMOJI_IDS[1])],[btn("< Styles",callback_data="page|stay",style="primary",icon=EMOJI_IDS[0]),btn("Main Menu",callback_data="menu|home",style="danger",icon=EMOJI_IDS[2])]])

def bulk_count_kb():
    nums=[2,3,4,5,8,10]; rows=[]; row=[]
    for n in nums:
        row.append(btn(f"{n} Names",callback_data=f"bulk|{n}",style="primary" if n%2 else "success",icon=EMOJI_IDS[n%len(EMOJI_IDS)]))
        if len(row)==3: rows.append(row); row=[]
    if row: rows.append(row)
    rows.append([btn("Main Menu",callback_data="menu|home",style="danger",icon=EMOJI_IDS[2])]); return InlineKeyboardMarkup(rows)

def bulk_result_kb():
    return InlineKeyboardMarkup([[btn("Next Styles",callback_data="bulkact|next",style="primary",icon=EMOJI_IDS[2]),btn("Category",callback_data="bulkact|cat",style="success",icon=EMOJI_IDS[1])],[btn("Edit Components",callback_data="act|edit",style="primary",icon=EMOJI_IDS[3]),btn("Same Design",callback_data="bulkact|same",style="success",icon=EMOJI_IDS[4])],[btn("Copy All",callback_data="bulkact|copy",style="primary",icon=EMOJI_IDS[0]),btn("New Batch",callback_data="menu|bulk",style="success",icon=EMOJI_IDS[2])],[btn("Main Menu",callback_data="menu|home",style="danger",icon=EMOJI_IDS[2])]])

def welcome_html(): return f"{ejoin(1,3,4)}\n<b>Welcome to {html.escape(BOT_TITLE)}!</b>\n\n{pe(4)} <b>VIP Premium and Aesthetic Name Studio</b>\n================\n{pe(2)} 156+ Handcrafted Signature Styles\nAesthetic, Hindi and Bio Name Maker\n================\n\n{pe(0)} Niche diye gaye buttons se option select karein:"
def help_html(): return f"{pe(2)} <b>1. Name Design Steps</b>\n01 Start — Make My Name\n02 Send — apna naam bhejo\n03 Category — Premium / Aesthetic / Live\n04 Choose — styles browse\n05 Copy — button dabao\n06 Edit — prefix suffix font\n\n{pe(3)} <b>2. Live Design</b>\nPrefix / Suffix ON-OFF\nUnderline ON-OFF\nEmoji ON-OFF\nFont cycle + Full Stylish\n\n{pe(3)} <b>3. VIP Bio Design</b>\nBIO button → custom text → browse → copy"

async def is_member(bot,user_id):
    if not storage.fsub_enabled() or not FORCE_CHANNEL or user_id in ADMIN_IDS or user_id==OWNER_ID: return True
    try:
        member=await bot.get_chat_member(f"@{FORCE_CHANNEL}",user_id); return member.status in (ChatMemberStatus.MEMBER,ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER)
    except TelegramError as err: log.info("fsub check failed: %s",err); return False
async def ask_fsub(target): await target.reply_text(f"{pe(4)} <b>Pehle channel join karo</b>\n{pe(0)} Join ke baad Verify dabao, tab start khulega.\n{pe(2)} Channel: @{html.escape(FORCE_CHANNEL)}",parse_mode="HTML",reply_markup=fsub_kb())
async def play_boot(msg):
    frames=[f"{ejoin(3,4)} <b>{html.escape(BOT_TITLE)}</b>\n\n[          ] 10%\n{pe(4)} Loading VIP styles...",f"{ejoin(3,4)} <b>{html.escape(BOT_TITLE)}</b>\n\n[=====     ] 50%\n{pe(4)} Loading 156+ VIP Custom Styles...",f"{ejoin(1,2)} <b>INITIALIZING ART ENGINE</b>\n\n[========  ] 80%\nPreparing Bio and Name Studio...",f"{ejoin(4,1)} <b>READY TO DESIGN</b>\n\n[==========] 100%\nLaunching Interactive Studio..."]
    sent=await msg.reply_text(frames[0],parse_mode="HTML")
    for text in frames[1:]:
        await asyncio.sleep(.28)
        try: await sent.edit_text(text,parse_mode="HTML")
        except TelegramError: break
    await asyncio.sleep(.2)
    try: await sent.delete()
    except TelegramError: pass
async def send_home(target): await target.reply_text(welcome_html(),parse_mode="HTML",reply_markup=menu_kb())
async def gated_start(update,context):
    user=update.effective_user
    if not user:return False
    chat=update.effective_chat
    if chat and chat.type!=ChatType.PRIVATE:return True
    if await is_member(context.bot,user.id):return True
    await ask_fsub(update.effective_message);return False
async def start(update,context):
    chat=update.effective_chat
    if chat and chat.type in (ChatType.GROUP,ChatType.SUPERGROUP):
        storage.add_group(chat.id);await update.message.reply_text(f"{pe(2)} Group mein sirf <code>/style naam</code>",parse_mode="HTML");return
    if not await gated_start(update,context):return
    await play_boot(update.message);session(context)["mode"]="menu";await send_home(update.message)
async def help_cmd(update,context):
    if not await gated_start(update,context):return
    await update.message.reply_text(help_html(),parse_mode="HTML",reply_markup=menu_kb())
async def open_rows(target,data,rows,category,edit=False):
    data["rows"],data["category"]=rows,category; max_page=max((len(rows)-1)//PAGE_SIZE,0);data["page"]=min(max(data.get("page",0),0),max_page);pages=max_page+1
    text=f"<b>Name:</b> {html.escape(data['name'])}\n<b>Category:</b> {html.escape(category.title())}\n<b>Page:</b> {data['page']+1}/{pages}\n\n{pe(0)} Click on any style below to copy it:";kb=styles_kb(rows,data["page"])
    if edit:await target.edit_text(text,parse_mode="HTML",reply_markup=kb)
    else:await target.reply_text(text,parse_mode="HTML",reply_markup=kb)
async def open_live(target,data,edit=False):
    parts=data["live"];rows=live_designs(data["name"],parts);data["rows"],data["category"]=rows,"live";data["page"]=min(max(data.get("page",0),0),max((len(rows)-1)//PAGE_SIZE,0));pages=max((len(rows)+PAGE_SIZE-1)//PAGE_SIZE,1);flag=lambda k:"ON" if parts.get(k) else "OFF"
    text=f"<b>🎬 LIVE DESIGN STUDIO</b>\n<b>Name:</b> {html.escape(data['name'])}\n<b>Page:</b> {data['page']+1}/{pages}\n\nPrefix <b>{flag('prefix_on')}</b> • Suffix <b>{flag('suffix_on')}</b> • Underline <b>{flag('underline')}</b> • Emoji <b>{flag('emoji')}</b>\nFont <b>{html.escape(parts.get('font','bold'))}</b>\n\n{pe(0)} <b>Controls upar se change karo — designs live update honge:</b>"
    kb=live_kb(parts,rows,data["page"])
    if edit:await target.edit_text(text,parse_mode="HTML",reply_markup=kb)
    else:await target.reply_text(text,parse_mode="HTML",reply_markup=kb)
async def open_styles(target,data,edit=False):
    if data.get("category")=="live":await open_live(target,data,edit=edit);return
    await open_rows(target,data,catalog(data["name"],data["category"]),data["category"],edit)
async def font_cmd(update,context):
    chat,data=update.effective_chat,session(context)
    if not context.args:
        if chat and chat.type!=ChatType.PRIVATE:await update.message.reply_text("Group: <code>/style Harry</code>",parse_mode="HTML");return
        data["mode"]="wait_name";await update.message.reply_text("Kripya wo name enter karein jo aap design karwana chahte hain:");return
    data["name"],data["category"],data["page"],data["mode"]=" ".join(context.args)[:24],"premium",0,"styles"
    if chat and chat.type in (ChatType.GROUP,ChatType.SUPERGROUP):storage.add_group(chat.id)
    await open_styles(update.message,data)
async def send_bulk(target,data):
    names=data.get("bulk_names") or [data["name"]];same=data.get("bulk_mode")=="same";lines=[f"{pe(2)} <b>BULK NAMES STUDIO ({len(names)} Names)</b>",""];data["rows"]=[];page=data.get("page",0)
    for i,nm in enumerate(names):
        pack=catalog(nm,data.get("category","premium"));style=pack[0] if same else pack[page%max(len(pack),1)];data["rows"].append(style);lines.append(f"<b>{i+1}. {html.escape(nm.upper())}</b>\n<code>{html.escape(style)}</code>")
    lines.append(f"\n{pe(0)} Copy All / Next Styles");await target.reply_text("\n".join(lines),parse_mode="HTML",reply_markup=bulk_result_kb())
async def on_private_text(update,context):
    if not await gated_start(update,context):return
    data=session(context);text=(update.message.text or "").strip()
    if not text:return
    mode=data.get("mode")
    if mode=="wait_bio":data["name"],data["page"],data["mode"]=text[:28],0,"styles";await open_rows(update.message,data,bios(data["name"]),"bio");return
    if mode=="wait_bulk":
        names=[p.strip()[:18] for p in text.replace(","," ").split() if p.strip()];data["bulk_names"]=names[:data.get("bulk_n",3)];await send_bulk(update.message,data);return
    data["name"],data["mode"]=text[:24],"pick_cat";await update.message.reply_text(f"<b>Name:</b> {html.escape(data['name'])}\n{pe(0)} Kripya niche 4 category se select karein:",parse_mode="HTML",reply_markup=cat_kb())
def cycle(seq,cur):
    if cur in seq:return seq[(seq.index(cur)+1)%len(seq)]
    return seq[1] if len(seq)>1 else seq[0]
async def on_callback(update,context):
    query,data,payload,user=update.callback_query,session(context),update.callback_query.data or "",update.effective_user
    if payload.startswith("fsub|"):
        if user and await is_member(context.bot,user.id):
            await query.answer("Verified")
            try:await query.message.delete()
            except TelegramError:pass
            await play_boot(query.message);await send_home(query.message)
        else:await query.answer("Pehle channel join karo",show_alert=True)
        return
    if user and update.effective_chat and update.effective_chat.type==ChatType.PRIVATE and not await is_member(context.bot,user.id):await query.answer("Channel join required",show_alert=True);await ask_fsub(query.message);return
    await query.answer()
    if payload=="noop":return
    if payload=="menu|home":data["mode"]="menu";await query.message.reply_text(welcome_html(),parse_mode="HTML",reply_markup=menu_kb());return
    if payload=="menu|name":data["mode"]="wait_name";await query.message.reply_text("Kripya wo name enter karein jo aap design karwana chahte hain:");return
    if payload=="menu|bio":data["mode"]="wait_bio";await query.message.reply_text("Bio ke liye naam / text bhejo:");return
    if payload=="menu|bulk":data["mode"]="bulk_n";await query.message.reply_text("Ek saath multiple names stylish bana sakte ho.\nKitne names? (2-10)",reply_markup=bulk_count_kb());return
    if payload=="menu|help":await query.message.reply_text(help_html(),parse_mode="HTML",reply_markup=menu_kb());return
    if payload.startswith("bulk|"):data["bulk_n"],data["mode"]=int(payload.split("|")[1]),"wait_bulk";await query.message.reply_text(f"{data['bulk_n']} names bhejo space ya comma se.\nExample: <code>Whey Ashy Rahi</code>",parse_mode="HTML");return
    if payload=="live|open":
        data["category"],data["page"],data["mode"]="live",0,"styles";await open_live(query.message,data,edit=True);return
    if payload.startswith("cat|"):data["category"],data["page"],data["mode"]=payload.split("|",1)[1],0,"styles";await open_styles(query.message,data,edit=True);return
    if payload.startswith("live|"):
        key=payload.split("|",1)[1];parts=data["live"]
        if key=="prefix":parts["prefix_on"]=not parts.get("prefix_on")
        elif key=="suffix":parts["suffix_on"]=not parts.get("suffix_on")
        elif key=="underline":parts["underline"]=not parts.get("underline")
        elif key=="emoji":parts["emoji"]=not parts.get("emoji")
        elif key=="font":parts["font"]=cycle(FONTS,parts.get("font","bold"))
        elif key=="full":parts.update({"prefix_on":True,"suffix_on":True,"underline":True,"emoji":True,"emoji_char":"🔥","font":"boldscript","spacing":"wide","crown":True,"prefix":PREFIXES[11] if len(PREFIXES)>11 else PREFIXES[1],"suffix":SUFFIXES[11] if len(SUFFIXES)>11 else SUFFIXES[1],"ornament":"♡","marks":"✦"})
        data["category"],data["page"]="live",0;await open_live(query.message,data,edit=True);return
    if payload.startswith("page|"):
        act=payload.split("|",1)[1];pages=max((len(data["rows"])+PAGE_SIZE-1)//PAGE_SIZE,1)
        if act=="next":data["page"]=min(data["page"]+1,pages-1)
        elif act=="back":
            if data.get("page",0)<=0:data["mode"]="pick_cat";await query.message.edit_text(f"<b>Name:</b> {html.escape(data['name'])}\n{pe(0)} Category select karo:",parse_mode="HTML",reply_markup=cat_kb());return
            data["page"]=max(data["page"]-1,0)
        await open_styles(query.message,data,edit=True);return
    if payload.startswith("pick|"):
        idx=int(payload.split("|",1)[1])
        if 0<=idx<len(data["rows"]):data["picked"]=data["rows"][idx];await query.message.reply_text(f"<b>Design Ready!</b> {pe(1)}\n\n<code>{html.escape(data['picked'])}</code>",parse_mode="HTML",reply_markup=picked_kb())
        return
    if payload=="act|copy":
        text=data.get("picked") or (data["rows"][0] if data["rows"] else "")
        if text:
            if CopyTextButton is None:await query.message.reply_text(f"{pe(3)} Done! Final design:\n<code>{html.escape(text)}</code>",parse_mode="HTML")
            else:await query.message.reply_text(f"{pe(3)} <b>Copy your final design</b>",parse_mode="HTML",reply_markup=InlineKeyboardMarkup([[btn("Copy Final Design",copy_text=CopyTextButton(text=text),style="success",icon=EMOJI_IDS[3])]]))
        return
    if payload=="act|edit":parts=data["edit"];preview=compose(data["name"],parts);data["picked"]=preview;await query.message.reply_text(f"<b>DESIGN EDITOR</b>\n\nPreview:\n<code>{html.escape(preview)}</code>\n\n{pe(0)} Component click karke edit karo:",parse_mode="HTML",reply_markup=editor_kb(parts));return
    if payload=="act|another":pages=max((len(data["rows"])+PAGE_SIZE-1)//PAGE_SIZE,1);data["page"]=(data["page"]+1)%pages;await open_styles(query.message,data,edit=True);return
    if payload=="act|done":preview=compose(data["name"],data["edit"]);data["picked"]=preview;await query.message.reply_text(f"Done! Aapka final design:\n<code>{html.escape(preview)}</code>",parse_mode="HTML",reply_markup=picked_kb());return
    if payload.startswith("ed|"):
        key=payload.split("|",1)[1];parts=data["edit"]
        if key=="prefix":parts["prefix"]=cycle(PREFIXES,parts.get("prefix") or "")
        elif key=="suffix":parts["suffix"]=cycle(SUFFIXES,parts.get("suffix") or "")
        elif key=="font":parts["font"]=cycle(FONTS,parts.get("font") or "bold")
        elif key=="under":parts["underline"]=not parts.get("underline")
        elif key=="space":parts["spacing"]="wide" if parts.get("spacing")!="wide" else "compact"
        elif key=="orn":parts["ornament"]=cycle(ORNAMENTS,parts.get("ornament") or "")
        elif key=="marks":parts["marks"]=cycle(MARKS,parts.get("marks") or "")
        elif key=="crown":parts["crown"]=not parts.get("crown")
        elif key=="title":parts["title"]="" if parts.get("title") else "VIP"
        preview=compose(data["name"],parts);data["picked"]=preview
        try:await query.message.edit_text(f"<b>DESIGN EDITOR</b>\n\nPreview:\n<code>{html.escape(preview)}</code>\n\n{pe(0)} Component click karke edit karo:",parse_mode="HTML",reply_markup=editor_kb(parts))
        except TelegramError:pass
        return
    if payload.startswith("bulkact|"):
        act=payload.split("|",1)[1]
        if act=="next":data["page"]=data.get("page",0)+1;await send_bulk(query.message,data)
        elif act=="cat":await query.message.reply_text("Category choose karo:",reply_markup=cat_kb())
        elif act=="same":data["bulk_mode"]="same" if data.get("bulk_mode")!="same" else "diff";await send_bulk(query.message,data)
        elif act=="copy":
            blob="\n".join(data.get("rows") or [])
            if CopyTextButton is None:await query.message.reply_text(f"<code>{html.escape(blob)}</code>",parse_mode="HTML")
            else:await query.message.reply_text(f"{pe(3)} <b>Bulk designs ready</b>",parse_mode="HTML",reply_markup=InlineKeyboardMarkup([[btn("Copy All Designs",copy_text=CopyTextButton(text=blob),style="success",icon=EMOJI_IDS[3])]]))
        return
async def on_chat_member(update,context):
    member=update.my_chat_member
    if not member or member.chat.type not in (ChatType.GROUP,ChatType.SUPERGROUP):return
    status=member.new_chat_member.status
    if status in ("member","administrator"):storage.add_group(member.chat.id)
    elif status in ("left","kicked"):storage.remove_group(member.chat.id)
async def hourly_promo(context):
    text=welcome_html()+f"\n\n{pe(4)} Group: <code>/style naam</code>"
    for chat_id in storage.list_groups():
        try:await context.bot.send_message(chat_id,text,parse_mode="HTML",reply_markup=menu_kb());await asyncio.sleep(.2)
        except Forbidden:storage.remove_group(chat_id)
        except RetryAfter as err:await asyncio.sleep(err.retry_after+1)
        except TelegramError as err:log.info("promo skip %s: %s",chat_id,err)
async def on_error(update,context):log.exception("update failed: %s",context.error)
def is_admin(user):
    if not user:return False
    return user.id in ADMIN_IDS or user.id==OWNER_ID or (user.username or "").lower()==OWNER_USERNAME
async def fsub_cmd(update,context):
    user=update.effective_user
    if not is_admin(user):await update.message.reply_text("Ye command sirf owner/admin ke liye hai.");return
    arg=context.args[0].lower() if context.args else ""
    if arg in ("on","1","true","enable"):storage.set_fsub(True);await update.message.reply_text(f"{pe(4)} Force join <b>ON</b>\nChannel: @{html.escape(FORCE_CHANNEL)}",parse_mode="HTML");return
    if arg in ("off","0","false","disable"):storage.set_fsub(False);await update.message.reply_text(f"{pe(2)} Force join <b>OFF</b>",parse_mode="HTML");return
    state="ON" if storage.fsub_enabled() else "OFF";await update.message.reply_text(f"Force join abhi <b>{state}</b>\n/fsub on\n/fsub off",parse_mode="HTML")
async def post_init(app):
    global BOT_TITLE
    me=await app.bot.get_me();BOT_TITLE=me.first_name or me.username or BOT_TITLE;log.info("bot title = %s",BOT_TITLE)
def main():
    if not TOKEN:raise RuntimeError("TELEGRAM_BOT_TOKEN missing")
    app=ApplicationBuilder().token(TOKEN).post_init(post_init).build();app.add_handler(CommandHandler("start",start));app.add_handler(CommandHandler("help",help_cmd));app.add_handler(CommandHandler("fsub",fsub_cmd));app.add_handler(CommandHandler("font",font_cmd));app.add_handler(CommandHandler("style",font_cmd));app.add_handler(CallbackQueryHandler(on_callback));app.add_handler(ChatMemberHandler(on_chat_member,ChatMemberHandler.MY_CHAT_MEMBER));app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,on_private_text));app.add_error_handler(on_error);jq=app.job_queue
    if jq:jq.run_repeating(hourly_promo,interval=max(PROMO_HOURS,.25)*3600,first=60,name="hourly-promo")
    log.info("Stylish Name Bot online");app.run_polling(drop_pending_updates=True,allowed_updates=Update.ALL_TYPES)
if __name__=="__main__":main()
