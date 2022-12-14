from enum import Enum

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.helpers import create_ssl_context

from app.read_conf import config, AppType


class Topics(Enum):
    PROCESSED_IMAGES = "processed_images"  # processed photo.id to send back to user
    IMAGE_PROCESSING = "image_processing"  # uploaded photo.id to process it, with processing type


async def init_consumer():
    return AIOKafkaConsumer(
        Topics.PROCESSED_IMAGES.value
        if config.app.type == AppType.BOT
        else Topics.IMAGE_PROCESSING.value,
        bootstrap_servers=config.kafka.bootstrap_servers,
        sasl_plain_username='bot',
        sasl_plain_password='qwerty123',
        group_id=config.app.type.value,
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="SCRAM-SHA-512",
    )


async def init_producer():
    return AIOKafkaProducer(
        bootstrap_servers=config.kafka.bootstrap_servers,
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="SCRAM-SHA-512",
        sasl_plain_username='bot',
        sasl_plain_password='qwerty123',
    )
