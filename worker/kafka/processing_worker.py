import asyncio
import logging

from app.kafka.photo_processing import load
from worker.image_processing import process_image
from worker.kafka import Topics, init_consumer, init_producer


async def processing():
    consumer = await init_consumer()
    producer = await init_producer()
    print("Worker consuming started")
    await producer.start()
    await consumer.start()
    while True:
        async for msg in consumer:
            try:
                photo = load(msg.value)
                photo = await process_image(photo)
                await producer.send(Topics.PROCESSED_IMAGES.value, photo.dump())
            except Exception as e:
                logging.error(e)
                pass
        await asyncio.sleep(0.1)
