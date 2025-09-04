import hashlib
from sqlalchemy import select, delete
from app.database.models import FavoriteJoke
from app.database.db import SessionLocal

async def add_to_favorites(user_id: int, joke_text: str, category: str) -> bool:
    """Добавляет анекдот в избранное"""
    async with SessionLocal() as session:
        joke_hash = generate_joke_hash(joke_text)
        
        existing = await session.scalar(
            select(FavoriteJoke).where(
                (FavoriteJoke.user_id == user_id) & 
                (FavoriteJoke.joke_hash == joke_hash)
            )
        )
        
        if existing:
            return False
        
        favorite = FavoriteJoke(
            user_id=user_id,
            joke_text=joke_text,
            category=category,
            joke_hash=joke_hash
        )
        
        session.add(favorite)
        await session.commit()
        await session.refresh(favorite)
        return True

async def get_user_favorites(user_id: int) -> list[FavoriteJoke]:
    """Получает все избранные анекдоты пользователя"""
    async with SessionLocal() as session:
        result = await session.execute(
            select(FavoriteJoke)
            .where(FavoriteJoke.user_id == user_id)
            .order_by(FavoriteJoke.created_at.desc())
        )
        return result.scalars().all()

async def delete_favorite(favorite_id: int, user_id: int) -> bool:
    """Удаляет анекдот из избранного"""
    async with SessionLocal() as session:
        result = await session.execute(
            delete(FavoriteJoke).where(
                (FavoriteJoke.id == favorite_id) & 
                (FavoriteJoke.user_id == user_id)
            )
        )
        await session.commit()
        return result.rowcount > 0

async def is_joke_in_favorites(user_id: int, joke_text: str) -> bool:
    """Проверяет, есть ли анекдот в избранном"""
    async with SessionLocal() as session:
        joke_hash = generate_joke_hash(joke_text)
        existing = await session.scalar(
            select(FavoriteJoke).where(
                (FavoriteJoke.user_id == user_id) & 
                (FavoriteJoke.joke_hash == joke_hash)
            )
        )
        return existing is not None

async def get_favorite_by_id(favorite_id: int, user_id: int) -> FavoriteJoke | None:
    """Получает анекдот из избранного по ID"""
    async with SessionLocal() as session:
        result = await session.execute(
            select(FavoriteJoke)
            .where(
            (FavoriteJoke.id == favorite_id) &
            (FavoriteJoke.user_id == user_id)
            )
        )
        return result.scalar_one_or_none()

async def get_favorite_by_hash(user_id: int, joke_hash: str) -> FavoriteJoke | None:
    """Находит анекдот в избранном по хэшу и user_id"""
    async with SessionLocal() as session:
        result = await session.execute(
            select(FavoriteJoke)
            .where(
                (FavoriteJoke.user_id == user_id) & 
                (FavoriteJoke.joke_hash == joke_hash)
            )
        )
        return result.scalar_one_or_none()

# Вспомогательная функция для генерации хэша
def generate_joke_hash(joke_text: str) -> str:
    """Генерирует MD5 хэш текста анекдота"""
    return hashlib.md5(joke_text.encode()).hexdigest()
