from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session
from order_service.models import Order
from order_service.db import get_session, create_db_and_tables
from order_service.crud import create_order_in_db, get_all_orders, get_order_by_id, get_product_from_cache, update_order_in_db, delete_order_in_db
from order_service.kafka_utilts import send_order_message, consume_product_messages
import asyncio
from order_service.schemas import CreateOrder, UpdateOrder
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Database Tables")
    await create_db_and_tables()
    asyncio.create_task(consume_product_messages())
    print("Kafka consumer task started")
    try:
        yield
    finally:
        # Any necessary cleanup can go here (e.g., closing database connections, shutting down services)
        print("Shutting down...")

# Initialize FastAPI app with lifespan management
app = FastAPI(
    lifespan=lifespan,
    title="Order Service",
    version="0.0.1")



@app.get("/")
def read_root():
    return {"Hello": "Order Service"}

# Route to create a new order service
@app.post("/orders/")
async def create_order(order_data: CreateOrder, session: AsyncSession = Depends(get_session)):
    # Use async with to get a session
    async with get_session() as session:
        # Get the product details from the cache
        product_cache = await get_product_from_cache(session, order_data.product_id)

        # If product is not found, return 404 error
        if not product_cache:
            raise HTTPException(status_code=404, detail="Product not found")

        # Call the function to create the order in the database
        order = await create_order_in_db(session, order_data, product_cache)
        # **Send order message to Kafka**
        await send_order_message(order, "created")
        # Return the created order
        return order


# Route to retrieve all orders
@app.get("/orders/")
async def read_orders(session: AsyncSession = Depends(get_session)):
    async with get_session() as session:
        # Call the asynchronous function to get all orders
        orders = await get_all_orders(session)
        return orders

# Route to retrieve a single order by its ID
@app.get("/orders/{id}")
async def read_order(id: int):
    async with get_session() as session:
        order = await get_order_by_id(session, id)  # Await the async function
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order


# Route to update an order's status
@app.put("/orders/{id}")
async def update_order(id: int, updated_order: UpdateOrder, session: AsyncSession = Depends(get_session)):
    async with get_session() as session:  # Properly using get_session with async with
        order = await update_order_in_db(session, id, updated_order)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        await send_order_message(order, "order has updated")
        return order


# Route to delete an order
@app.delete("/orders/{id}")
async def delete_order(id: int):
    async with get_session() as session:  # Properly use async with to manage session
        order = await delete_order_in_db(session, id)  # Ensure delete function is awaited
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Send Kafka message after order deletion
        await send_order_message(order, "deleted")
        return {"message": "Order deleted successfully"} 
