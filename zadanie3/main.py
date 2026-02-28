from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime

# Konfiguracja bazy danych SQLite
DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Modele bazy danych (tabele)
class PostDB(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    author = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    comments = relationship("CommentDB", back_populates="post")


class CommentDB(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    author = Column(String(100))
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("PostDB", back_populates="comments")


# Tworzymy tabele w bazie
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")


def get_db():
    """Dependency - daje sesję bazy danych i zamyka ją po użyciu."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Modele Pydantic (walidacja danych wejściowych/wyjściowych)
class PostCreate(BaseModel):
    title: str
    content: str
    author: str


class CommentCreate(BaseModel):
    content: str
    author: str


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(PostDB).all()


@app.post("/posts", status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = PostDB(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post nie istnieje")
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "created_at": post.created_at,
        "comments": post.comments
    }


@app.put("/posts/{post_id}")
def update_post(post_id: int, updated: PostCreate, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post nie istnieje")
    post.title = updated.title
    post.content = updated.content
    post.author = updated.author
    db.commit()
    db.refresh(post)
    return post


@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post nie istnieje")
    db.delete(post)
    db.commit()


@app.post("/posts/{post_id}/comments", status_code=201)
def add_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post nie istnieje")
    new_comment = CommentDB(**comment.dict(), post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@app.get("/posts/{post_id}/comments")
def get_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post nie istnieje")
    return db.query(CommentDB).filter(CommentDB.post_id == post_id).all()
