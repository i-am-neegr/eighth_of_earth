from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True)
    is_released = Column(Boolean, default=False)
    poster_path = Column(String(255))           # путь к файлу или URL
    trailer_url = Column(String(255))
    rutube_url = Column(String(255))
    vk_url = Column(String(255))
    kion_url = Column(String(255))
    okko_url = Column(String(255))
    kinopoisk_url = Column(String(255))

    def __repr__(self):
        return f"<Category {self.name}>"

class HeroSuggestion(Base):
    __tablename__ = "hero_suggestions"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    username = Column(String(100))
    category_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(Text, nullable=False)      # визионерство
    contacts = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class PremiereSubscriber(Base):
    __tablename__ = "premiere_subscribers"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    full_name = Column(String(200))
    phone = Column(String(30))
    email = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

class PartnerRequest(Base):
    __tablename__ = "partner_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    username = Column(String(100), nullable=True)      # ← добавили
    company_info = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())