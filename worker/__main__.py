import asyncio

from worker.kafka.processing_worker import processing


async def worker():
    await processing()


def main():
    asyncio.run(worker())


if __name__ == '__main__':
    main()
