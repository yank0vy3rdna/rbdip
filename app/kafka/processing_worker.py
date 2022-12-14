import asyncio
import json
import logging

from app.database.query import get_photo
from app.image_processing import ProcessingTypes, process_image
from app.kafka import Topics, init_consumer, init_producer


async def processing():
    consumer = await init_consumer()
    producer = await init_producer()
    print("Worker consuming started")
    await producer.start()
    await consumer.start()
    while True:
        async for msg in consumer:
            try:
                decoded = json.loads(msg.value)
                photo_id = decoded['photo_id']
                processing_type = ProcessingTypes(decoded['processing_type'])
                photo = await get_photo(photo_id)
                photo = await process_image(photo, processing_type)
                await photo.save()
                await producer.send(Topics.PROCESSED_IMAGES.value, json.dumps({"photo_id": photo_id}).encode('utf-8'))
            except Exception as e:
                logging.error(e)
                pass
        await asyncio.sleep(0.1)
