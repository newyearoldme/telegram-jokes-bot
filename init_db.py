import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import BigInteger, DateTime, UniqueConstraint, String
from sqlalchemy.orm import mapped_column, declarative_base, Mapped
from datetime import datetime, timezone

import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("db_url")

Base = declarative_base()

class FavoriteJoke(Base):
    __tablename__ = "favorite_jokes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    joke_text: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    joke_hash: Mapped[str] = mapped_column(String(32), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'joke_hash', name='unique_user_joke'),
    )
    
async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
