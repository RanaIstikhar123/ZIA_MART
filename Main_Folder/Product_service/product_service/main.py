from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel ,Session,select
from product_service.crud import create_product
from product_service.schemas import ProductCreate
from product_service.db import get_session, create_db_and_tables
from product_service.models import Product
from product_service import setting
from product_service.models import Product
from typing import List
from aiokafka import AIOKafkaProducer
from product_service import product_pb2
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from .db import create_db_and_tables, get_session
from .crud import create_product, get_product, get_all_products, update_product, delete_product
from .schemas import ProductCreate, ProductUpdate
from .kafka_utils import send_product_message
from sqlmodel import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Database Tables")
    # This creates the database tables synchronously
    create_db_and_tables()
    yield  # Continue running the application after this point
    print("Shutdown process")  # Add any shutdown logic here if needed

app = FastAPI(
    lifespan=lifespan,
    title="Product Service",
    version="0.0.1",
    servers=[
        # Optionally enable servers config during deployment
        # {
        #     "url": "http://0.0.0.0:8000",
        #     "description": "Development Server"
        # }
    ]
)





@app.get("/")
def read_root():
    return {"Hello": "Product Service"}
@app.post("/products/")
async def create_new_product(product_data: ProductCreate, session: Session = Depends(get_session)):
    product = create_product(session, product_data)
    await send_product_message(product, "created")
    return product

@app.get("/products/")
def read_all_products(session: Session = Depends(get_session)):
    return get_all_products(session)

@app.get("/products/{product_id}")
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}")
async def update_existing_product(product_id: int, product_data: ProductUpdate, session: Session = Depends(get_session)):
    product = update_product(session, product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await send_product_message(product, "updated")
    return product

@app.delete("/products/{product_id}")
async def delete_existing_product(product_id: int, session: Session = Depends(get_session)):
    product = delete_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await send_product_message(product, "deleted")
    return product
