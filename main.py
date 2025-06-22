
# main.py
# This is your bot with inline buttons for 24/7 hosting

import os
import json
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_CHAT_ID = int(os.environ.get("OWNER_CHAT_ID", "7435632959"))
UID_MAP_FILE = "uids_button_map.txt"

if os.path.exists(UID_MAP_FILE):
    with open(UID_MAP_FILE, "r", encoding="utf-8") as f:
        pending_uids = json.load(f)
else:
    pending_uids = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=(
                    "🤖 AI SIGNAL গ্রুপে এড হতে আপনার কটেক্স অ্যাকাউন্ট এর আইডিটি পাঠান।\n\n"
                    "✅ অবশ্যই আপনার অ্যাকাউন্ট আমাদের লিংক থেকে হওয়া লাগবে এবং সেখানে ব্যালেন্স থাকা লাগবে।\n\n"
                    "অ্যাকাউন্ট না থাকলে @TraderFxOfficial আইডিতে মেসেজ দিন।"
                )
            )

async def handle_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == OWNER_CHAT_ID:
        return

    message_text = update.message.text.strip()
    user = update.message.from_user

    if re.fullmatch(r'\d{6,}', message_text):
        await update.message.reply_text(
            "✅ ধন্যবাদ আমরা আপনার UID টি পেয়েছি, সবকিছু ঠিক থাকলে আপনাকে গ্রুপের লিংক দিয়ে দেওয়া হবে।"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve:{user.id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject:{user.id}")
            ]
        ])

        forward_text = (
            f"🔔 <b>নতুন UID:</b> <code>{message_text}</code>\n"
            f"👤 <b>Username:</b> @{user.username or 'NoUsername'}\n"
            f"🆔 <b>User ID:</b> <code>{user.id}</code>"
        )

        sent = await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=forward_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

        pending_uids[str(sent.message_id)] = user.id
        with open(UID_MAP_FILE, "w", encoding="utf-8") as f:
            json.dump(pending_uids, f)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id_str = query.data.split(":")
    user_id = int(user_id_str)

    if action == "approve":
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "📢 <b>IMPORTANT NOTICE ‼️</b>\n\n"
                "আমাদের লিংকে তৈরি করা অ্যাকাউন্টে Trade করবেন , অন্য কোনও অ্যাকাউন্ট ব্যবহার করবেন না, "
                "অন্যথায় আমরা আপনাকে VIP থেকে বের করে দিব।\n\n"
                "কাউন্টে ডলার থাকুক বা না থাকুক কখনোই আপনার কোটেক্স অ্যাকাউন্টটি DELETE করবেন না।\n\n"
                "<b>WELCOME TO BLACK DEMON AI 👇</b>\n"
                "https://t.me/+P5KGxa94UfJhYTA1\n"
                "https://t.me/+P5KGxa94UfJhYTA1\n\n"
                "আমাদের সাথে প্রতারণা করবেন না ✅"
            ),
            parse_mode="HTML"
        )
        await query.edit_message_text(text="✅ Approved and user notified.", parse_mode="HTML")

    elif action == "reject":
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ দুঃখিত , সাময়িক সমস্যার কারণে আপনাকে NON MTG AI দেওয়া সম্ভব হচ্ছে না।\n\n"
                 "আপনার UID তে সমস্যা আছে, দয়া করে সাপোর্ট আইডিতে মেসেজ করুন @TraderFxOfficial"
        )
        await query.edit_message_text(text="❌ Rejected and user notified.", parse_mode="HTML")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_uid))
app.add_handler(CallbackQueryHandler(handle_buttons))

print("🤖 Bot is running with button-based hosting support...")
app.run_polling()
