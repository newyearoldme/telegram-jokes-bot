from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, DateTime, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
import hashlib

Base = declarative_base()

class FavoriteJoke(Base):
    __tablename__ = "favorite_jokes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    joke_text: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    joke_hash: Mapped[str] = mapped_column(String(32), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'joke_hash', name='unique_user_joke'),
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.joke_hash and self.joke_text:
            self.joke_hash = self.generate_hash(self.joke_text)
    
    @staticmethod
    def generate_hash(text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()
