import asyncio
import json
import logging
from io import BytesIO

from aiogram import Bot

from app.database.query import get_photo
from app.image_processing import ProcessingTypes
from app.kafka import Topics, init_consumer, init_producer


async def processing(bot: Bot):
    print("Bot consuming started")
    consumer = await init_consumer()
    await consumer.start()
    while True:
        async for msg in consumer:
            try:
                decoded = json.loads(msg.value)
                photo_id = decoded['photo_id']
                photo = await get_photo(photo_id)
                photo_buffer = BytesIO(photo.photo)
                await bot.send_photo(photo.user.tg_id, photo_buffer)
            except Exception as e:
                logging.error(e)
                pass
        await asyncio.sleep(0.1)


async def produce_photo_to_process(photo_id: str, processing_type: ProcessingTypes):
    producer = await init_producer()
    await producer.start()
    await producer.send(Topics.IMAGE_PROCESSING.value, json.dumps({
        "photo_id": photo_id,
        "processing_type": processing_type.value
    }).encode('utf-8'))
    await producer.stop()
