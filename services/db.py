# services/db.py
from __future__ import annotations
import os
from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "posts.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    topic = Column(String(256))
    platform = Column(String(32))
    tone = Column(String(32))
    caption = Column(Text)
    image_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)


def save_post(topic: str, caption: str, image_url: str, platform: str, tone: str) -> int:
    with SessionLocal() as s:
        p = Post(topic=topic, platform=platform, tone=tone, caption=caption, image_url=image_url)
        s.add(p)
        s.commit()
        s.refresh(p)
        return p.id


def list_posts(limit: int = 20) -> List[Post]:
    with SessionLocal() as s:
        return s.query(Post).order_by(Post.created_at.desc()).limit(limit).all()


def get_post(post_id: int) -> Optional[Post]:
    with SessionLocal() as s:
        return s.get(Post, post_id)