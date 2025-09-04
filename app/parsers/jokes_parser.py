import asyncio
import aiohttp
import random

from bs4 import BeautifulSoup
from app.config import Config

async def get_random_joke(category_url: str, max_pages: int) -> str:
    # Случайный выбор страницы
    page_num = random.randint(1, max_pages)
    current_url = f"{category_url.rstrip('/')}/{page_num}/" if page_num > 1 else category_url
    
    try:
        timeout = aiohttp.ClientTimeout(total=Config.timeout)     

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(current_url) as response:
                if response.status != 200:
                    return f"⚠️ Ошибка {response.status} при загрузке страницы {page_num}"
                
                html = await response.text()

            soup = BeautifulSoup(html, "lxml")
            jokes = soup.find_all("div", class_="holder-body")
            
            if not jokes:
                return "⚠️ Не удалось найти анекдот. Попробуй ещё раз!"

            joke = random.choice(jokes)
            
            # Замена <br> на перенос строк \n
            for br in joke.find_all("br"):
                br.replace_with("\n")
            
            # Удаление ссылок
            for link in joke.find_all("a"):
                link.replace_with(link.get_text())
            
            text = joke.get_text()
            
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            return '\n'.join(lines)

    except asyncio.TimeoutError:
        return "⏰ Сайт не отвечает. Попробуйте позже!"
    except aiohttp.ClientError:
        return "🌐 Ошибка соединения. Проверьте интернет!"

def extract_joke_text(message_text: str) -> str:
    """
    Извлекает чистый текст анекдота из сообщения бота
    Убирает заголовок категории (первую строку до двойного переноса)
    """
    if "\n\n" in message_text:
        parts = message_text.split("\n\n", 1)
        return parts[1].strip()
    return message_text.strip()
