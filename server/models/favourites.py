from models.base import Base
from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Favourite(Base):
    __tablename__ = "favourites"

    id: Mapped[str] = mapped_column(TEXT, primary_key=True)
    user_id: Mapped[str] = mapped_column(TEXT, ForeignKey("users.id"))
    song_id: Mapped[str] = mapped_column(TEXT, ForeignKey("songs.id"))

    song = relationship("Song")