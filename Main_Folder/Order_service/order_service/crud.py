from sqlmodel import select
from order_service.models import Order, ProductCache
from sqlalchemy.ext.asyncio import AsyncSession

# Function to create an order in the database
async def create_order_in_db(session: AsyncSession, order_data, product_cache):
    if product_cache is None or not hasattr(product_cache, 'price'):
        raise ValueError("Product price not found in cache")
    
    total_price = order_data.quantity * product_cache.price
    
    order = Order(
        user_id=order_data.user_id,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        total_price=order_data.total_price,
        status="created"
    )
    session.add(order)
    await session.commit()  # Use await with async commit
    await session.refresh(order)
    return order

# Function to retrieve a product from the local cache
async def get_product_from_cache(session: AsyncSession, product_id: int):
    result = await session.execute(
        select(ProductCache).where(ProductCache.id == product_id)
    )
    return result.scalar_one_or_none()

# Function to retrieve all orders (synchronous operation)
async def get_all_orders(session: AsyncSession):
    result = await session.execute(select(Order))
    return result.scalars().all()  # Fetch all orders

# Function to retrieve a single order by ID
async def get_order_by_id(session: AsyncSession, order_id: int):
    return await session.get(Order, order_id)  # Correctly await the session.get


# Function to update an order in the database
async def update_order_in_db(session: AsyncSession, order_id: int, updated_data):
    order = await session.get(Order, order_id)  # Ensure the session.get call is awaited
    if not order:
        return None
    order.status = updated_data.status
    session.add(order)
    await session.commit()  # Await commit
    await session.refresh(order)  # Await refresh
    return order

# Function to delete an order from the database
async def delete_order_in_db(session: AsyncSession, order_id: int):
    # Use session.get and await it
    order = await session.get(Order, order_id)
    if not order:
        return None
    # Perform the deletion
    await session.delete(order)
    await session.commit()  
    return order 












