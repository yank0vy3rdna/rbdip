import asyncio
import json
import logging
from io import BytesIO

from aiogram import Bot

from app.kafka.photo_processing import load, PhotoObject
from tg_bot.database import get_photo
from worker.image_processing import ProcessingTypes
from tg_bot.kafka import Topics, init_consumer, init_producer


async def processing(bot: Bot):
    print("Bot consuming started")
    consumer = await init_consumer()
    await consumer.start()
    while True:
        async for msg in consumer:
            try:
                photo = load(msg.value)
                photo_db = await get_photo(photo.photo_id)
                photo_buffer = BytesIO(photo.photo)
                await bot.send_photo(photo_db.user.tg_id, photo_buffer)
            except Exception as e:
                logging.error(e)
                pass
        await asyncio.sleep(0.1)


async def produce_photo_to_process(photo_id: str, photo: bytes, processing_type: ProcessingTypes):
    producer = await init_producer()
    await producer.start()
    await producer.send(
        Topics.IMAGE_PROCESSING.value,
        PhotoObject(
            photo_id=photo_id,
            processing_type=processing_type,
            photo=photo
        ).dump()
    )
    await producer.stop()
