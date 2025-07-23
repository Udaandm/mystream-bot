import os
import uuid
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = '8063798457:AAHqD4Sc6FcPJ646g0PzUThORN7BWvpJ0Lg'
SERVER_URL = 'https://mystream-bot.onrender.com'  # <-- replace after deployment

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.video or update.message.document
    file_id = file.file_id
    file_info = await context.bot.get_file(file_id)
    file_url = file_info.file_path
    full_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_url}"

    # Download file
    video_data = requests.get(full_url).content
    unique_id = uuid.uuid4().hex
    file_path = f"videos/{unique_id}.mp4"

    os.makedirs("videos", exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(video_data)

    # Send streaming link
    stream_link = f"{SERVER_URL}/watch/{unique_id}"
    await update.message.reply_text(f"🎬 Your streaming link:\n{stream_link}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

print("Bot is running...")
app.run_polling()
