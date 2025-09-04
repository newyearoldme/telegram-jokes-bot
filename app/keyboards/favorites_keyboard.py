from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_favorites_pagination_keyboard(favorites: list, page: int = 0, page_size: int = 5) -> InlineKeyboardMarkup:
    """Клавиатура с пагинацией для избранного"""
    total_pages = (len(favorites) + page_size - 1) // page_size
    start_idx = page * page_size
    end_idx = start_idx + page_size
    page_favorites = favorites[start_idx:end_idx]

    keyboard = []

    for favorite in page_favorites:
        joke_preview = favorite.joke_text[:50] + "..." if len(favorite.joke_text) > 50 else favorite.joke_text
        keyboard.append([
            InlineKeyboardButton(
                text=f"📄 {joke_preview}", 
                callback_data=f"view_fav_{favorite.id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text=f"📄 Страница {page+1}/{total_pages}", 
            callback_data="no_action"
        )
    ])
    
    # Кнопки навигации
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"fav_page_{page-1}"))
        
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"fav_page_{page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton(text="🔙 К анекдотам", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_favorite_detail_keyboard(favorite_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для просмотра конкретного анекдота"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_fav_{favorite_id}")],
        [InlineKeyboardButton(text="📋 К списку", callback_data="fav_list")]
    ])
