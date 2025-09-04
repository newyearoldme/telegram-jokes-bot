import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    token = os.getenv("token")
    timeout = int(os.getenv("timeout", "10"))

    if not token:
        raise ValueError("⚠️ Токен не найден в .env файле")
    
    categories = {
        "shtirlitz": {
            "name": "🚗 Про Штирлица",
            "url": "https://anekdoty.ru/pro-shtirlica/",
            "max_pages": 22
        },
        "tupo": {
            "name": "👦 Тупые, но смешные", 
            "url": "https://anekdoty.ru/tupo-no-smeshno/",
            "max_pages": 28
        },
        "black": {
            "name": "⚫ Чёрный юмор",
            "url": "https://anekdoty.ru/cherniy-yumor/",
            "max_pages": 5
        },
        "programmers": {
            "name": "💻 Программисты",
            "url": "https://anekdoty.ru/pro-programmistov/",
            "max_pages": 12
        }
    }

