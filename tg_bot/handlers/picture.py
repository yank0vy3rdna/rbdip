from io import BytesIO

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tg_bot.database.query import upload_photo, get_or_create_user
from tg_bot.handlers import States, get_language
from worker.image_processing import ProcessingTypes
from tg_bot.kafka.processing_bot import produce_photo_to_process


async def vignette_face(message: Message):
    await States.wait_for_upload_photo_for_create_vignette.set()
    _ = await get_language(message.from_user.id)
    await message.answer(_("Send me the photo"))


async def delete_face(message: Message):
    await States.wait_for_upload_photo_for_delete_face.set()
    _ = await get_language(message.from_user.id)
    await message.answer(_("Send me the photo"))


async def upload_img_for_delete(message: Message, state: FSMContext):
    photo_dest = BytesIO()
    await message.photo[-1].download(destination_file=photo_dest)
    user, created = await get_or_create_user(message.from_user.id)
    photo = await upload_photo(user)
    await produce_photo_to_process(str(photo.id), photo_dest.read(), ProcessingTypes.DELETE_FACES)
    await state.finish()
    _ = await get_language(message.from_user.id)
    await message.answer(_("Wait, photo processing ..."))


async def upload_img_for_vignette(message: Message, state: FSMContext):
    photo_dest = BytesIO()
    await message.photo[-1].download(destination_file=photo_dest)
    user, created = await get_or_create_user(message.from_user.id)
    photo = await upload_photo(user)
    await produce_photo_to_process(str(photo.id), photo_dest.read(), ProcessingTypes.VIGNETTE)
    await state.finish()
    _ = await get_language(message.from_user.id)
    await message.answer(_("Wait, photo processing ..."))
