from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from app.kafka import Topics
from app.read_conf import config


async def init_consumer():
    return AIOKafkaConsumer(
        Topics.PROCESSED_IMAGES.value,
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
