import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import requests

# تنظیمات
BOT_TOKEN = os.environ['BOT_TOKEN']
DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

# لاگ‌گیری
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update, context):
    await update.message.reply_text('🌹 سلام! من رُزم! با من چت کن!')

async def debug_message(update, context):
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    chat_type = update.message.chat.type
    
    logger.info(f"🔍 دیباگ - پیام از {user_name} در {chat_type}: {user_message}")
    
    # تست ساده بدون DeepSeek
    response = f"سلام {user_name} جان! 😊 پیامت رو دیدم: '{user_message}'"
    
    logger.info(f"📤 ارسال پاسخ: {response}")
    await update.message.reply_text(response)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # فقط دو هندلر ساده
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, debug_message))
    
    logger.info("🤖 بات دیباگ در حال اجرا...")
    application.run_polling()

if __name__ == '__main__':
    main()
