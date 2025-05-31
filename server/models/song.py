from sqlalchemy import TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class Song(Base):
    __tablename__ = "songs"

    id: Mapped[str] = mapped_column(TEXT, primary_key=True, index=True)
    song_url: Mapped[str] = mapped_column(TEXT)
    thumbnail_url: Mapped[str] = mapped_column(TEXT)
    artist: Mapped[str] = mapped_column(VARCHAR(100))
    song_name: Mapped[str] = mapped_column(VARCHAR(100))
    hex_code: Mapped[str] = mapped_column(VARCHAR(6))