from sqlalchemy import TEXT, VARCHAR, LargeBinary
from models.base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(TEXT, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(VARCHAR(100))
    email: Mapped[str] = mapped_column(VARCHAR(100), unique=True)
    password: Mapped[str] = mapped_column(LargeBinary)

    favourites = relationship("Favourite", back_populates="user")