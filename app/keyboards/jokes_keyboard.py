from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.config import Config
from app.database import crud
from app.parsers.jokes_parser import extract_joke_text

def get_category_keyboard() -> InlineKeyboardMarkup:
    """Динамическая клавиатура для выбора категорий анекдотов"""
    keyboard = []
    for category_id, category_data in Config.categories.items():
        keyboard.append([
            InlineKeyboardButton(
                text=category_data["name"],
                callback_data=f"category_{category_id}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_joke_keyboard(category_id: str, message_text: str, user_id: int) -> InlineKeyboardMarkup:
    """Клавиатура после показа анекдота"""
    joke_text = extract_joke_text(message_text)
    is_in_favorites = await crud.is_joke_in_favorites(user_id, joke_text)

    if is_in_favorites:
        favorite_button = InlineKeyboardButton(
            text="🗑️ Удалить из избранного", 
            callback_data="remove_favorite"
        )
    else:
        favorite_button = InlineKeyboardButton(
            text="❤️ Добавить в избранное", 
            callback_data="add_favorite"
            )
        
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎭 Ещё анекдот", callback_data=f"category_{category_id}"),
            favorite_button,
        ],
        [
            InlineKeyboardButton(text="🔙 Сменить категорию", callback_data="main_menu")
        ]
    ])

def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для подтверждения действий"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, удалить", callback_data="confirm_remove"),
            InlineKeyboardButton(text="❌ Нет, отменить", callback_data="cancel_remove")
        ]
    ])
