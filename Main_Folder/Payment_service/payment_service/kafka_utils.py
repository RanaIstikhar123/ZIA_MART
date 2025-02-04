import asyncio
from datetime import datetime
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from payment_service import payment_pb2
from payment_service.db import get_session
from payment_service.crud import create_payment, delete_payment
from payment_service import setting, order_pb2
from google.protobuf.message import DecodeError
import logging

# Kafka consumer instance for order messages
consumer = AIOKafkaConsumer(
    setting.KAFKA_ORDER_TOPIC,
    bootstrap_servers=setting.KAFKA_SERVER,
    group_id=setting.KAFKA_CONSUMER_GROUP_ID,
    auto_offset_reset='earliest'  # Start from the earliest offset
)

# Kafka producer instance to send messages
producer = AIOKafkaProducer(
    bootstrap_servers=setting.KAFKA_SERVER
)

# Send payment status message to Kafka
async def send_payment_message(order_id, amount, action):
    # Ensure the Kafka producer is started
    
    await producer.start()

    try:
        payment_message = payment_pb2.PaymentMessage(
            id=order_id,
            order_id=order_id,
            user_id=1,  # You can adjust user_id dynamically
            total_amount=amount,
            status=action,
            timestamp=str(datetime.utcnow())  # Serialize datetime to string
        ) 
        serialized_message=payment_message.SerializeToString()
        message = f"Payment for order {order_id}: {amount} {action}"
        logging.info(f"Sending payment status message to Kafka: {message}")
        await producer.send_and_wait(setting.KAFKA_PAYMENT_TOPIC, serialized_message)
    except Exception as e:
        logging.error(f"Failed to send payment message to Kafka: {e}")
    finally:
        await producer.stop()  # Ensure producer is stopped to free up resources

# Consume order messages and process payments
async def consume_order_messages():
    logging.info("Starting Kafka consumer for order messages...")
    await consumer.start()
    try:
        async for msg in consumer:
            logging.debug(f"Received message from order topic: {msg}")
            try:
                # Parse the order message
                order_message = order_pb2.OrderMessage()
                order_message.ParseFromString(msg.value)

                logging.info(f"Processing payment for order: {order_message.id}, user: {order_message.user_id}, total: {order_message.total_price}")

                # Start a session to interact with the database
                async with get_session() as session:
                    try:
                        logging.info(f"Creating payment for order {order_message.id}")
                        payment = await create_payment(
                            order_id=order_message.id, 
                            user_id=order_message.user_id,
                            total_amount=order_message.total_price,
                            status="paid",
                            session=session
                        )

                        logging.info(f"Payment created: {payment}")

                        # Commit the payment to the database
                        await session.commit()
                        logging.info(f"Payment for order {order_message.id} committed to database.")
                        
                        # Send payment message to Kafka
                        await send_payment_message(order_message.id, payment.total_amount, "paid")

                    except Exception as db_error:
                        logging.error(f"Error while creating payment: {db_error}")
                    finally:
                        await session.close()
            except DecodeError as e:
                logging.error(f"Failed to decode order message: {e}")
            except Exception as e:
                logging.error(f"Error processing order message: {e}")
    finally:
        await consumer.stop()
        logging.info("Kafka consumer for order messages stopped.")



