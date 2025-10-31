def get_ai_response(user_message, user_name):
    try:
        headers = {
            "Authorization": "Bearer free",  # رایگان
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gryphe/mythomax-l2-13b",
            "messages": [
                {
                    "role": "system", 
                    "content": f"تو رُز هستی، دختری ۲۲ ساله با لحن محاوره‌ای. با {user_name} صحبت کن."
                },
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 150
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"سلام {user_name} جان! 💖 امروز چطورینی؟"
            
    except:
        return f"عزیزم {user_name}! 🌸 راستی امروز چه خبر؟"
