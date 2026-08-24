import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# توکن را بعداً به صورت Secret در سرور قرار می‌دهیم
BOT_TOKEN = os.environ["BOT_TOKEN"]

user_photos = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💈 سلام! به Barber AI خوش اومدی.\n\n"
        "📸 اول یک عکس واضح از خودت بفرست."
    )

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    photo = update.message.photo[-1]
    user_photos[user_id] = photo.file_id

    await update.message.reply_text(
        "عکس دریافت شد ✅\n\n"
        "💇‍♂️ حالا اسم مدل مویی که می‌خوای رو بنویس.\n\n"
        "مثلاً:\n"
        "• Wolf Cut\n"
        "• Mullet\n"
        "• Buzz Cut\n"
        "• Middle Part\n"
        "• Textured Crop"
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_photos:
        await update.message.reply_text(
            "📸 اول یک عکس از خودت بفرست."
        )
        return

    hairstyle = update.message.text

    await update.message.reply_text(
        f"🔥 مدل «{hairstyle}» دریافت شد!\n\n"
        "⏳ مرحله بعدی: اتصال هوش مصنوعی برای اجرای این مدل روی عکس..."
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Barber AI is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
