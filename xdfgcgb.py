from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os

# Buraya BotFather'dan aldığın token'ı yaz
TOKEN =9259720678:AAHVwLmwN3_xAK94MrkX6EAz5HZyDuW0FMI

user_photos = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba!\n\nBana bir fotoğraf gönder.\nSonra ne yapmak istediğini seçeceksin."
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    file_path = f"temp_{user_id}.jpg"
    await file.download_to_drive(file_path)
    user_photos[user_id] = file_path

    keyboard = [
        [InlineKeyboardButton("Bikini", callback_data="bikini")],
        [InlineKeyboardButton("İç Çamaşırı", callback_data="underwear")],
        [InlineKeyboardButton("Elbise", callback_data="dress")],
        [InlineKeyboardButton("İptal", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Ne yapmak istersin?", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    choice = query.data

    if choice == "cancel":
        await query.edit_message_text("İşlem iptal edildi.")
        if user_id in user_photos:
            os.remove(user_photos[user_id])
            del user_photos[user_id]
        return

    if user_id not in user_photos:
        await query.edit_message_text("Önce bir fotoğraf göndermelisin.")
        return

    await query.edit_message_text("İşleniyor, lütfen bekle...")

    # Şimdilik aynı fotoğrafı geri gönderiyoruz
    result_path = user_photos[user_id]

    await context.bot.send_photo(chat_id=user_id, photo=open(result_path, "rb"))
    await query.edit_message_text("İşte sonucun!")

    os.remove(user_photos[user_id])
    del user_photos[user_id]

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()