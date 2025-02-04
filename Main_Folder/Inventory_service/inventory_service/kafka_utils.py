from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from sqlmodel import Session
from inventory_service.db import get_session
from inventory_service.crud import create_or_update_inventory, get_inventory_by_product_id
from inventory_service.models import Inventory
from inventory_service import product_pb2, order_pb2  # Compiled Protobuf files
from inventory_service.setting import KAFKA_SERVER, KAFKA_PRODUCT_TOPIC, KAFKA_ORDER_TOPIC, KAFKA_CONSUMER_GROUP_ID

# Kafka producer instance (if needed for notifications or other events)
producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)

# Kafka consumer instance for product and order messages
consumer = AIOKafkaConsumer(
    KAFKA_PRODUCT_TOPIC, KAFKA_ORDER_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    group_id=KAFKA_CONSUMER_GROUP_ID
)

async def consume_messages():
    print("Kafka consumer is starting...")
    await consumer.start()
    print("Kafka consumer started.")

    try:
        async for msg in consumer:
            print(f"Received message from topic {msg.topic}: {msg.value}")

            # Handle product messages from product_topic
            if msg.topic == KAFKA_PRODUCT_TOPIC:
                product_message = product_pb2.ProductMessage()  # type: ignore
                product_message.ParseFromString(msg.value)
                print(f"Consuming product message: id={product_message.id}, action={product_message.action}")

                async with get_session() as session:
                    # Add or update the product in the inventory with stock 100
                    await create_or_update_inventory(session, product_message.id, 100)
                    print(f"Product with id={product_message.id} added to inventory with stock 100.")

            # Handle order messages from order_topic
            elif msg.topic == KAFKA_ORDER_TOPIC:
                order_message = order_pb2.OrderMessage()  # type: ignore
                order_message.ParseFromString(msg.value)
                print(f"Consuming order message: id={order_message.id}, action={order_message.action}")

                async with get_session() as session:
                    inventory = await get_inventory_by_product_id(session, order_message.product_id)

                    if inventory:
                        if order_message.action == "created":
                            # Reduce stock when an order is created
                            inventory.stock -= order_message.quantity
                            print(f"Reduced stock by {order_message.quantity}. New stock: {inventory.stock}")

                        elif order_message.action == "deleted":
                            # Restore stock when an order is deleted
                            print(f"Before update: Inventory stock for product_id={order_message.product_id} is {inventory.stock}")
                            inventory.stock += order_message.quantity
                            print(f"After update: Restored stock by {order_message.quantity}. New stock: {inventory.stock}")
                        if inventory.stock < 0:
                            print(f"Low stock warning: Product ID {order_message.product_id} has insufficient stock.Please add quantity  to inventory and try again and order will not be processed")

                            inventory.stock = 0  # Adjust to 0 or other logic as needed

                        session.add(inventory)
                        await session.commit()
                        print(f"Inventory updated in DB for product_id {order_message.product_id}")
                    else:
                        print(f"Inventory for product_id {order_message.product_id} not found.")
    finally:
        print("Kafka consumer stopped.")
        await consumer.stop()


