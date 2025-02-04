from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from order_service.db import get_session
from order_service import setting
from order_service import order_pb2, product_pb2  # Compiled Protobuf files
from sqlmodel import select
from order_service.models import ProductCache
from order_service.setting import KAFKA_SERVER, KAFKA_PRODUCT_TOPIC, KAFKA_CONSUMER_GROUP_ID,KAFKA_ORDER_TOPIC
import aiohttp
# Kafka producer instance for order messages
producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)

# Kafka consumer instance for product messages
consumer = AIOKafkaConsumer(
    KAFKA_PRODUCT_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    group_id=KAFKA_CONSUMER_GROUP_ID
)

# Function to send order messages to Kafka
async def send_order_message(order, action):
    await producer.start()
    try:
        # Create a Protobuf message
        order_message = order_pb2.OrderMessage(
            id=order.id,
            user_id=order.user_id,
            product_id=order.product_id,
            quantity=order.quantity,
            total_price=order.total_price,
            status=order.status,
            action=order.action  # "created", "updated", "deleted"
        )
        # Serialize the message to send to Kafka
        serialized_message = order_message.SerializeToString()
        # Send message to Kafka
        await producer.send_and_wait(KAFKA_ORDER_TOPIC, serialized_message)
        print(f"Sent order message to Kafka: {action}, order id: {order.id}")
    finally:
        await producer.stop()

# Function to consume product messages and update local cache
async def consume_product_messages():
    await consumer.start()
    print("Kafka consumer started...")
    try:
        async for msg in consumer:
            print(f"Received message {msg}")

            try:
                product_message = product_pb2.ProductMessage()
                product_message.ParseFromString(msg.value)

                print(f"Parsed product message: ID={product_message.id}, Name={product_message.name}, Price={product_message.price}, Quantity={product_message.quantity}, Action={product_message.action}")
            except Exception as e:
                print(f"Error parsing message: {e}")
                continue  # Skip this message if there's an error

            # Correctly use async with to manage session context
            async with get_session() as session:
                result = await session.execute(
                    select(ProductCache).where(ProductCache.id == product_message.id)
                )
                product_cache = result.scalar_one_or_none()

                # Handle created and updated actions
                if product_message.action in ["created", "updated"]:
                    if not product_cache:
                        product_cache = ProductCache(
                            id=product_message.id,
                            name=product_message.name,
                            description=product_message.description,
                            price=product_message.price,
                            quantity=product_message.quantity
                        )
                    else:
                        product_cache.name = product_message.name
                        product_cache.description = product_message.description
                        product_cache.price = product_message.price
                        product_cache.quantity = product_message.quantity

                    session.add(product_cache)
                    await session.commit()
                    print(f"Product cache updated for product ID: {product_message.id}")

                # Handle deleted action
                elif product_message.action == "deleted" and product_cache:
                    await session.delete(product_cache)
                    await session.commit()
                    print(f"Product cache deleted for product ID: {product_message.id}")

    finally:
        await consumer.stop() 

# Function to check inventory stock from the Inventory Service via HTTP
async def check_inventory(product_id: int, quantity: int):
    # Use the service name 'inventory_service' for inter-service communication
    inventory_url = f"http://inventory_service:8005/inventory/{product_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(inventory_url) as response:
            if response.status == 200:
                inventory_data = await response.json()
                available_stock = inventory_data.get("stock", 0)
                print(f"Available stock for product {product_id}: {available_stock}")
                return available_stock >= quantity  # Return True if enough stock is available
            else:
                print(f"Failed to fetch inventory for product ID: {product_id}, Status: {response.status}")
                return False  # Assume insufficient stock if the request fails
