from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from collections import defaultdict
import os

# In-memory storage
user_points = defaultdict(int)
user_joined_by = dict()

# Replace with your actual public channel username
CHANNEL_USERNAME = "@ErnbondsAnnouncements"

# /start command logic with referral and channel check
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    if user.id not in user_joined_by:
        if args:
            referrer_id = int(args[0])
            if referrer_id != user.id:
                try:
                    # Check if user joined the channel
                    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)
                    if member.status in ['member', 'administrator', 'creator']:
                        user_points[referrer_id] += 5
                        user_joined_by[user.id] = referrer_id
                        await context.bot.send_message(
                            chat_id=referrer_id,
                            text=f"🎉 You invited {user.first_name} who joined the channel!\nYou earned +5 points.\nTotal: {user_points[referrer_id]}"
                        )
                    else:
                        await update.message.reply_text(
                            f"⚠️ Please join the channel first: {CHANNEL_USERNAME}"
                        )
                        return
                except Exception:
                    await update.message.reply_text(
                        f"⚠️ Please join the channel first: {CHANNEL_USERNAME}"
                    )
                    return

    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\nUse /referral to get your invite link."
    )

# /referral command
async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = f"https://t.me/{context.bot.username}?start={user.id}"
    await update.message.reply_text(f"🔗 Your referral link:\n{link}\n\n(Your invite must join {CHANNEL_USERNAME})")

# /mypoints command
async def mypoints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    points = user_points.get(user.id, 0)
    await update.message.reply_text(f"🏆 You have {points} point(s)!")

# Load your Telegram Bot Token from Railway environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("referral", referral))
app.add_handler(CommandHandler("mypoints", mypoints))

# Start polling
app.run_polling()
