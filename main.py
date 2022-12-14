import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import BotCommand

from app.database.query import db_start, db_close_connections
from app.handlers import register_handlers
from app.read_conf import config, AppType


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Bot description"),
        BotCommand(command="/language", description="Select language"),
        BotCommand(command="/vignette", description="Make a vignette for the face"),
        BotCommand(command="/delete", description="Delete a face from a photo")
    ]
    await bot.set_my_commands(commands)


storage = RedisStorage2(host=config.redis.host, port=config.redis.port, db=config.redis.db,
                        password=config.redis.password)
bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(bot, storage=storage)


async def run_bot():
    await db_start()

    register_handlers(dp)

    await set_commands(bot)
    print("bot started")
    await dp.start_polling()
    await db_close_connections()
    await dp.storage.close()
    await dp.storage.wait_closed()


async def worker():
    from app.kafka.processing_worker import processing

    await db_start()
    await processing()


def main():
    if config.app.type == AppType.BOT:
        from app.kafka.processing_bot import processing
        loop_processing = asyncio.new_event_loop()
        # thread = threading.Thread(target=loop_processing.run_until_complete, args=(processing(bot),))
        # thread.start()
        loop_processing.run_until_complete(asyncio.gather(processing(bot), run_bot(), loop=loop_processing))
    elif config.app.type == AppType.WORKER:
        asyncio.run(worker())


if __name__ == '__main__':
    main()
