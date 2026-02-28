from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Konfiguracja
SECRET_KEY = "tajny_klucz_zmien_na_produkcji"
ALGORITHM = "HS256"
TOKEN_WAZNY_MINUTY = 30

DATABASE_URL = "sqlite:///./auth_todo.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI(title="Todo API z autoryzacją")


# Modele bazy danych
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    todos = relationship("TodoDB", back_populates="owner")


class TodoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates="todos")


Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency - daje sesję bazy danych."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Modele Pydantic
class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class TodoCreate(BaseModel):
    title: str
    completed: bool = False


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(data: dict) -> str:
    """Tworzy token JWT z datą wygaśnięcia."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_WAZNY_MINUTY)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Dependency - wyciąga zalogowanego użytkownika z tokenu."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Nieprawidłowy token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Nieprawidłowy token")
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Użytkownik nie istnieje")
    return user


@app.post("/auth/register", status_code=201)
def register(user: UserRegister, db: Session = Depends(get_db)):
    if db.query(UserDB).filter(UserDB.username == user.username).first():
        raise HTTPException(status_code=400, detail="Nazwa użytkownika zajęta")
    new_user = UserDB(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "Konto utworzone"}


@app.post("/auth/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Złe dane logowania")
    token = create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/todos")
def get_todos(current_user: UserDB = Depends(get_current_user)):
    return current_user.todos


@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    new_todo = TodoDB(**todo.dict(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo
