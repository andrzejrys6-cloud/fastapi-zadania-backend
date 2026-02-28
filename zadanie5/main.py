from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./produkty.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Katalog Produktów")


class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(String(500))
    price = Column(Float)
    category = Column(String(100))
    available = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    available: bool = True


@app.post("/products", status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = ProductDB(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/products")
def get_products(
    # Filtrowanie
    category: Optional[str] = Query(None, description="Filtruj po kategorii"),
    min_price: Optional[float] = Query(None, description="Minimalna cena"),
    max_price: Optional[float] = Query(None, description="Maksymalna cena"),
    available: Optional[bool] = Query(None, description="Tylko dostępne"),
    # Wyszukiwanie
    search: Optional[str] = Query(None, description="Szukaj w nazwie i opisie"),
    # Sortowanie
    sort: Optional[str] = Query(None, description="price_asc, price_desc, name_asc, name_desc"),
    # Paginacja
    page: int = Query(1, ge=1, description="Numer strony"),
    per_page: int = Query(10, ge=1, le=100, description="Ile wyników na stronie"),
    db: Session = Depends(get_db)
):
    query = db.query(ProductDB)

    # Filtrowanie
    if category:
        query = query.filter(ProductDB.category == category)
    if min_price is not None:
        query = query.filter(ProductDB.price >= min_price)
    if max_price is not None:
        query = query.filter(ProductDB.price <= max_price)
    if available is not None:
        query = query.filter(ProductDB.available == available)

    # Wyszukiwanie po nazwie lub opisie
    if search:
        query = query.filter(
            or_(
                ProductDB.name.contains(search),
                ProductDB.description.contains(search)
            )
        )

    # Sortowanie
    if sort == "price_asc":
        query = query.order_by(ProductDB.price.asc())
    elif sort == "price_desc":
        query = query.order_by(ProductDB.price.desc())
    elif sort == "name_asc":
        query = query.order_by(ProductDB.name.asc())
    elif sort == "name_desc":
        query = query.order_by(ProductDB.name.desc())

    # Łączna liczba wyników (przed paginacją)
    total = query.count()

    # Paginacja
    offset = (page - 1) * per_page
    products = query.offset(offset).limit(per_page).all()

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "results": products
    }
