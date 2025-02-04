from aiokafka import AIOKafkaConsumer
from notification_service import order_pb2, payment_pb2
from notification_service.db import get_session
from notification_service.crud import create_notification, update_notification, delete_notification
from google.protobuf.message import DecodeError
from notification_service import setting
import logging

# Adjust logging level to INFO to suppress excessive logs
logging.basicConfig(level=logging.INFO)
logging.getLogger("aiokafka").setLevel(logging.WARN)  # Only show warnings from aiokafka
logging.getLogger("kafka").setLevel(logging.WARN)

# Kafka consumer instances for order and payment messages
order_consumer = AIOKafkaConsumer(
    setting.KAFKA_ORDER_TOPIC,
    bootstrap_servers=setting.KAFKA_SERVER,
    group_id=setting.KAFKA_CONSUMER_GROUP_ID,
    auto_offset_reset='earliest'
)

payment_consumer = AIOKafkaConsumer(
    setting.KAFKA_PAYMENT_TOPIC, 
    bootstrap_servers=setting.KAFKA_SERVER,
    group_id=setting.KAFKA_CONSUMER_GROUP_ID,
    auto_offset_reset='earliest'
)

# Consume order messages and handle notifications
async def consume_order_messages():
    await order_consumer.start()
    try:
        async for msg in order_consumer:
            logging.info(f"Received message from order topic: {msg}")
            try:
                order_message = order_pb2.OrderMessage()
                order_message.ParseFromString(msg.value)

                logging.info(f"Processing order message: {order_message.id}, action: {order_message.action}")

                async with get_session() as session:
                    if order_message.action == "created":
                        notification_message = f"Order {order_message.id} has been created."
                        logging.info(notification_message)
                        await create_notification(
                            user_id=order_message.user_id,
                            message=notification_message,
                            event_type="order_created",
                            session=session
                        )
                    elif order_message.action == "updated":
                        notification_message = f"Order {order_message.id} has been updated."
                        logging.info(notification_message)
                        await update_notification(
                            notification_id=order_message.id,
                            new_message=notification_message,
                            new_event_type="order_updated",
                            session=session
                        )
                    elif order_message.action == "deleted":
                        logging.info(f"Order {order_message.id} has been deleted.")
                        await delete_notification(
                            notification_id=order_message.id,
                            session=session
                        )
            except DecodeError as e:
                logging.error(f"Failed to decode order message: {e}")
            except Exception as e:
                logging.error(f"Error processing order message: {e}")
    finally:
        await order_consumer.stop()

# Similar changes for payment consumer


# Consume payment messages and handle notifications
async def consume_payment_messages():
    await payment_consumer.start()  # Start the Kafka consumer
    try:
        async for msg in payment_consumer:  # Process each message
            logging.debug(f"Received message from payment topic: {msg}")
            try:
                payment_message = payment_pb2.PaymentMessage()
                payment_message.ParseFromString(msg.value)

                logging.info(f"Processing payment message: {payment_message.order_id}, status: {payment_message.status}")

                async with get_session() as session:
                    logging.info("Inside session context for payment processing")

                    if payment_message.status == "paid":
                        notification_message = f"Payment for order {payment_message.order_id} has been processed."
                        logging.info(f"Notification message created: {notification_message}")

                        try:
                            await create_notification(
                                user_id=payment_message.user_id,
                                message=notification_message,
                                event_type="payment_processed",
                                session=session
                            )
                            logging.info(f"Notification created for payment: {payment_message.order_id}")
                        except Exception as e:
                            logging.error(f"Failed to create notification: {e}")

                    # elif payment_message.status == "refunded":
                    #     notification_message = f"Payment for order {payment_message.order_id} has been refunded."
                    #     logging.info(f"Notification message created: {notification_message}")

                    #     try:
                    #         await update_notification(
                    #             notification_id=payment_message.order_id,
                    #             new_message=notification_message,
                    #             new_event_type="payment_refunded",
                    #             session=session
                    #         )
                    #         logging.info(f"Notification updated for refund: {payment_message.order_id}")
                    #     except Exception as e:
                    #         logging.error(f"Failed to update notification: {e}")

            except DecodeError as e:
                logging.error(f"Failed to decode payment message: {e}")
            except Exception as e:
                logging.error(f"Error processing payment message: {e}")
    finally:
        await payment_consumer.stop()  # Stop the consumer on exit
