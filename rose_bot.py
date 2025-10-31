import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging

# تنظیمات
BOT_TOKEN = os.environ['BOT_TOKEN']

# لاگ‌گیری
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update, context):
    await update.message.reply_text('🌹 سلام! من رُزم! حالا میتونی با من چت کنی')

async def handle_all_messages(update, context):
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    
    logger.info(f"🎯 پیام دریافت شد از {user_name}: {user_message}")
    
    # پاسخ ساده و مطمئن
    response = f"سلام {user_name} عزیز! 😊 پیامت رو خوندم: '{user_message}'"
    
    try:
        await update.message.reply_text(response)
        logger.info(f"✅ پاسخ ارسال شد: {response}")
    except Exception as e:
        logger.error(f"❌ خطا در ارسال پاسخ: {e}")

def main():
    try:
        # ساخت اپلیکیشن
        application = Application.builder().token(BOT_TOKEN).build()
        
        # افزودن هندلرها - بسیار ساده
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.ALL, handle_all_messages))
        
        logger.info("🚀 بات در حال راه‌اندازی...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"🔥 خطای جدی: {e}")

if __name__ == '__main__':
    main()
