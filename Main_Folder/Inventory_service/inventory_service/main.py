from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session
from inventory_service.db import get_session, create_db_and_tables
from inventory_service.crud import create_or_update_inventory, get_all_inventory, get_inventory_by_product_id, delete_inventory
from inventory_service.kafka_utils import consume_messages
import asyncio
from contextlib import asynccontextmanager 


# Async lifespan for handling startup and shutdown processes
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Database Tables")
    await create_db_and_tables()

    # Start the Kafka consumers
   # Start Kafka consumer for product and order messages
    asyncio.create_task(consume_messages())
    yield
# Initialize FastAPI app with lifespan management
app = FastAPI(
    lifespan=lifespan,
    title="Inventory Service",
    version="0.0.1"
)

@app.get("/")
def read_root():
    return {"Hello": "Inventory Service"}
# Route to create or update inventory manually
@app.post("/inventory/")
async def create_or_update_inventory_route(product_id: int, quantity: int):
    async with get_session() as session:
        inventory = await create_or_update_inventory(session, product_id, quantity)
        return inventory

# Route to get inventory by product ID
@app.get("/inventory/{product_id}")
async def read_inventory(product_id: int):
    async with get_session() as session:
        inventory = await get_inventory_by_product_id(session, product_id)
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")
        return inventory

# Route to get all inventory records
@app.get("/inventory/")
async def read_all_inventory():
    async with get_session() as session:
        inventories = await get_all_inventory(session=session)
        return inventories

# Route to delete inventory for a product
@app.delete("/inventory/{product_id}")
async def delete_inventory_route(product_id: int):
    async with get_session() as session:
        inventory = await delete_inventory(session, product_id)
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")
        return inventory