from sqlmodel import Session, select
from inventory_service.db import get_session
from inventory_service.models import Inventory
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession



async def create_or_update_inventory(session: AsyncSession, product_id: int, stock: int):
    # Execute the select query asynchronously
    result = await session.execute(select(Inventory).where(Inventory.product_id == product_id))
    inventory = result.scalar_one_or_none()

    if inventory:
        inventory.stock = stock  # Update existing inventory stock
    else:
        # Create a new inventory record if it doesn't exist
        inventory = Inventory(product_id=product_id, stock=stock)
        session.add(inventory)

    # Commit the changes asynchronously
    await session.commit()
    # Refresh the inventory object to get the latest state
    await session.refresh(inventory)
    return inventory


async def get_inventory_by_product_id(session: AsyncSession, product_id: int):
    # Execute the select query asynchronously
    result = await session.execute(select(Inventory).where(Inventory.product_id == product_id))
    # Return the first matching inventory record
    return result.scalar_one_or_none()




async def get_all_inventory(session: AsyncSession):
    # Execute the select query asynchronously
    result = await session.execute(select(Inventory))
    # Return all inventory records
    return result.scalars().all()


# Function to delete an inventory record
async def delete_inventory(session: AsyncSession, product_id: int):
    # Execute the select query asynchronously
    result = await session.execute(select(Inventory).where(Inventory.product_id == product_id))
    inventory = result.scalar_one_or_none()

    if inventory:
        # Delete the inventory record
        await session.delete(inventory)
        # Commit the transaction asynchronously
        await session.commit()

    return inventory






