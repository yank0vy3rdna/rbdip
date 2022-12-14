import gettext
import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from app.database.query import change_language, get_language_by_user_id
from app.utils.clickhouse import clickhouse


class States(StatesGroup):
    waiting_for_change_language = State()
    wait_for_upload_photo_for_delete_face = State()
    wait_for_upload_photo_for_create_vignette = State()


sticker_id = 'CAACAgIAAxkBAAEGfBxjetaQOBsjRQTDC3an2dyQS5Q01AAC3RkAAuQOcUrcT4DHnnyMxisE'


async def start(message: Message, state: FSMContext):
    await state.finish()
    _ = await get_language(message.from_user.id)
    clickhouse.record(
        {"user_id": message.from_user.id, "photo_size": 111, "action_type": "delete", "processing_time": 1111})
    await message.answer(_("This bot is designed to remove a face or create a vignette. "
                           "Use the following commands to interact with it:\n"
                           "/start - Bot description\n"
                           "/language - Language selection\n"
                           "/vignette - Make a vignette\n"
                           "/delete - Remove a face from a photo\n"))


async def language(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Русский", "English")
    await States.waiting_for_change_language.set()
    _ = await get_language(message.from_user.id)
    await message.answer(_("Select a language"), reply_markup=keyboard)


async def change_language_to_russian(message: Message, state: FSMContext):
    await change_language(message.from_user.id, 'ru')
    await message.answer("Выбран русский язык", reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def change_language_to_english(message: Message, state: FSMContext):
    await change_language(message.from_user.id, 'en')
    await message.answer("English lang chosen", reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def get_language(id):
    language = await get_language_by_user_id(id)
    translation = gettext.translation('messages', os.path.join("home", "yank0vy3rdna", "Cloud", 'locale'), [language])
    translation.install()
    _ = translation.gettext
    return _
