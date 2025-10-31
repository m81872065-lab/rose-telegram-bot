import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import requests
import json

BOT_TOKEN = os.environ['BOT_TOKEN']
DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_deepseek_response(user_message, user_name):
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        messages = [
            {
                "role": "system", 
                "content": f"تو رُز هستی، یک دختر ۲۲ ساله مهربون و با احساس. با {user_name} صحبت کن."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        logger.info("📡 در حال ارسال درخواست به DeepSeek...")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        logger.info(f"🔔 وضعیت پاسخ DeepSeek: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            logger.info(f"✅ پاسخ DeepSeek: {ai_response}")
            return ai_response
        else:
            error_msg = f"خطای API: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return f"متأسفانه الان مشکل فنی دارم {user_name} جان! 😔"
            
    except Exception as e:
        logger.error(f"🔥 خطا در ارتباط با DeepSeek: {e}")
        return f"ارتباطم قطع شده {user_name}! 🌸"

async def start(update, context):
    await update.message.reply_text('🌹 سلام! من رُزم! با من چت کن')

async def handle_all(update, context):
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    
    logger.info(f"📨 پیام از {user_name}: {user_message}")
    
    # نمایش "در حال تایپ"
    await update.message.chat.send_action(action="typing")
    
    # دریافت پاسخ از DeepSeek
    bot_response = await get_deepseek_response(user_message, user_name)
    
    # ارسال پاسخ
    await update.message.reply_text(bot_response)
    logger.info(f"📤 پاسخ ارسال شد")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all))
    
    logger.info("🚀 بات رُز با DeepSeek فعال شد!")
    app.run_polling()

if __name__ == '__main__':
    main()
