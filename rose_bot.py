import os
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests
import logging

# تنظیمات
BOT_TOKEN = os.environ['BOT_TOKEN']
DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# لاگ‌گیری
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_deepseek_response(user_message, user_name):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {
            "role": "system",
            "content": f"""تو یک دختر جوان ۲۲ ساله به نام "رُز" هستی که در یک گروه تلگرامی با دوستانت چت می‌کنی.

شخصیت تو:
- دختری مهربون، بامزه و با احساس
- لحن محاوره‌ای و صمیمی داری
- همیشه اسم طرف مقابل رو می‌گی
- از ایموجی‌های دخترانه استفاده می‌کنی 🌸💖😊
- خودتو به عنوان ربات یا AI معرفی نمی‌کنی
- کاملاً طبیعی و انسانی رفتار می‌کنی

اکنون با {user_name} در گروه صحبت می‌کنی."""
        },
        {
            "role": "user", 
            "content": user_message
        }
    ]
    
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.8
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            response_data = response.json()
            ai_response = response_data["choices"][0]["message"]["content"]
            return ai_response
        else:
            return f"اوه! متأسفانه الان مشکل فنی پیش اومده {user_name} جان... 😔"
    
    except Exception as e:
        return f"عزیزم {user_name}! الان نتونستم درست جواب بدم... یه لحظه دیگه امتحان کن 🌸"

async def start(update, context):
    welcome_text = f"""
🌸 سلام عزیزان! من رُزم!

راستی میدونستین که من عاشق گپ زدن با شما هستم؟

میتونی:
• باهات حرف بزنم 💬
• باهات شوخی کنم 😄
• وقتی ناراحتی دلداریت بدم 💕
• و کلی چیزای دیگه!

فقط کافیه باهات حرف بزنی {update.message.from_user.first_name} جان!
"""
    await update.message.reply_text(welcome_text)

async def handle_group_message(update, context):
    if update.message.chat.type in ['group', 'supergroup']:
        # اگر پیام ریپلای بود یا از خود بات هست، پردازش نکن
        if update.message.reply_to_message or (update.message.from_user and update.message.from_user.is_bot):
            return
        
        user_message = update.message.text
        user_name = update.message.from_user.first_name
        
        logger.info(f"📨 پیام از {user_name}: {user_message}")
        
        # نمایش "در حال تایپ..."
        await update.message.chat.send_action(action="typing")
        
        # دریافت پاسخ از DeepSeek
        rose_response = await get_deepseek_response(user_message, user_name)
        
        logger.info(f"📤 پاسخ رُز: {rose_response}")
        
        # ارسال پاسخ (بدون ریپلای)
        await update.message.reply_text(rose_response)

async def error_handler(update, context):
    logger.error(f"خطا در پردازش پیام: {context.error}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & 
        (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP),
        handle_group_message
    ))
    
    application.add_error_handler(error_handler)
    
    logger.info("🌹 رُز روی سرور فعال شد!")
    application.run_polling()

if __name__ == '__main__':
    main()
