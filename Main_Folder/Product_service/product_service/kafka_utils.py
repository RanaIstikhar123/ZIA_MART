from aiokafka import AIOKafkaProducer
from product_service.setting import KAFKA_SERVER, KAFKA_PRODUCT_TOPIC
from product_service import product_pb2  # Compiled Protobuf

producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)

async def send_product_message(product, action):
    await producer.start()
    try:
        product_message =product_pb2.ProductMessage( 
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            action=action  # "created", "updated", "deleted"
        )
        serialized_message = product_message.SerializeToString()
        await producer.send_and_wait(KAFKA_PRODUCT_TOPIC, serialized_message)
    finally:
        await producer.stop()
