import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import requests
import json

BOT_TOKEN = os.environ['BOT_TOKEN']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_ai_response(user_message, user_name):
    """دریافت پاسخ از OpenRouter (رایگان)"""
    try:
        headers = {
            "Authorization": "Bearer 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",  # کلید رایگان
            "Content-Type": "application/json",
            "HTTP-Referer": "https://replit.com",
            "X-Title": "Rose Telegram Bot"
        }
        
        messages = [
            {
                "role": "system", 
                "content": f"""تو یک دختر جوان ۲۲ ساله به نام "رُز" هستی. شخصیت تو:
- دختری مهربون، بامزه و با احساس
- لحن محاوره‌ای و صمیمی داری
- همیشه اسم طرف مقابل رو می‌گی
- از ایموجی‌های دخترانه استفاده می‌کنی 🌸💖😊
- خودتو به عنوان ربات معرفی نمی‌کنی
- کاملاً طبیعی و انسانی رفتار می‌کنی

اکنون با {user_name} صحبت می‌کنی."""
            },
            {
                "role": "user", 
                "content": user_message
            }
        ]
        
        data = {
            "model": "gryphe/mythomax-l2-13b",  # مدل رایگان
            "messages": messages,
            "max_tokens": 200,
            "temperature": 0.8
        }
        
        logger.info("📡 در حال ارسال درخواست به OpenRouter...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=20
        )
        
        logger.info(f"🔔 وضعیت پاسخ: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            logger.info(f"✅ پاسخ دریافت شد: {ai_response}")
            return ai_response
        else:
            logger.warning(f"⚠️ خطای API، استفاده از پاسخ پیش‌فرض: {response.text}")
            # پاسخ پیش‌فرض اگر API جواب نداد
            return f"سلام {user_name} جان! 💖 امروز چه خبر؟ راستی دمت گرم که باهات حرف میزنم! 😊"
            
    except Exception as e:
        logger.error(f"🔥 خطا در ارتباط: {e}")
        return f"عزیزم {user_name}! 🌸 راستی امروز چطوریتی؟"

async def start(update, context):
    welcome_text = f"""
🌹 سلام عزیزان! من رُزم!

می‌تونیم با هم:
• گپ بزنیم 💬
• شوخی کنیم 😄
• دلداری بدیم 💕
• و کلی چیزای دیگه!

فقط کافیه باهات حرف بزنی {update.message.from_user.first_name} جان!
"""
    await update.message.reply_text(welcome_text)

async def handle_all(update, context):
    # اگر پیام از بات باشد، پردازش نکن
    if update.message.from_user and update.message.from_user.is_bot:
        return
        
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    
    logger.info(f"📨 پیام از {user_name}: {user_message}")
    
    # نمایش "در حال تایپ"
    await update.message.chat.send_action(action="typing")
    
    # دریافت پاسخ از هوش مصنوعی
    bot_response = await get_ai_response(user_message, user_name)
    
    # ارسال پاسخ
    await update.message.reply_text(bot_response)
    logger.info("📤 پاسخ ارسال شد")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all))
    
    logger.info("🚀 بات رُز با OpenRouter فعال شد!")
    app.run_polling()

if __name__ == '__main__':
    main()
