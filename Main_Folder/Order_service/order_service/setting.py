from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=str)
KAFKA_SERVER = config("KAFKA_SERVER", cast=str)
KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC", cast=str)
KAFKA_PRODUCT_TOPIC = config("KAFKA_PRODUCT_TOPIC", cast=str)
KAFKA_CONSUMER_GROUP_ID = config("KAFKA_CONSUMER_GROUP_ID", cast=str)


