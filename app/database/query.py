from tortoise import Tortoise

from app.database.model import User, Photo
from app.read_conf import config


async def db_start():
    url = f'{config.db_bot.db_type}://{config.db_bot.user}:{config.db_bot.password}@{config.db_bot.host}:{int(config.db_bot.port)}/{config.db_bot.db_name}'
    # tortoise_config: dict = generate_config(url, {"models": ["app.database.model"]})
    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "database": config.db_bot.db_name,
                        "host": config.db_bot.host,
                        "password": config.db_bot.password,
                        "port": config.db_bot.port,
                        "user": config.db_bot.user,
                    }
                }
            },
            "apps": {
                "models": {
                    "models": ["app.database.model"],
                    "default_connection": "default",
                }
            },
        }
    )
    await Tortoise.generate_schemas()


async def get_or_create_user(tg_id: int):
    return await User.get_or_create(tg_id=tg_id)


async def get_language_by_user_id(tg_id: int):
    user = await User.get_or_create(tg_id=tg_id)
    if user is None:
        return 'en'
    return user[0].language


async def upload_photo(user: User, photo: bytes):
    return await Photo.create(user=user, photo=photo)


async def get_photo(photo_id: str):
    return await Photo.get(id=photo_id).prefetch_related("user")


async def change_language(tg_id: int, language: str):
    user = await User.filter(tg_id=tg_id).first()
    user.language = language
    await user.save()


async def db_close_connections():
    await Tortoise.close_connections()
