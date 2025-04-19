
import os
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN = os.getenv("ADMIN_USERNAME")

ISMI, TEL, MAHSULOT, MANZIL = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Buyurtma berish uchun ismingizni yozing:")
    return ISMI

async def get_ism(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['ism'] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:")
    return TEL

async def get_tel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['tel'] = update.message.text
    await update.message.reply_text("Mahsulot nomini kiriting:")
    return MAHSULOT

async def get_mahsulot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mahsulot'] = update.message.text
    await update.message.reply_text("Manzilingizni yozing:")
    return MANZIL

async def get_manzil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['manzil'] = update.message.text
    msg = f"Yangi buyurtma:\n\nIsm: {context.user_data['ism']}\nTelefon: {context.user_data['tel']}\nMahsulot: {context.user_data['mahsulot']}\nManzil: {context.user_data['manzil']}"
    await context.bot.send_message(chat_id=ADMIN, text=msg)
    await update.message.reply_text("Buyurtmangiz qabul qilindi! Tez orada bog‘lanamiz.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Buyurtma bekor qilindi.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ISMI: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ism)],
            TEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tel)],
            MAHSULOT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_mahsulot)],
            MANZIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_manzil)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
