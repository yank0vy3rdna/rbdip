from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from app.handlers.default import *
from app.handlers.picture import *


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")

    dp.register_message_handler(language, commands="language", state="*")
    dp.register_message_handler(change_language_to_english, Text(equals="English", ignore_case=True),
                                state=States.waiting_for_change_language)
    dp.register_message_handler(change_language_to_russian, Text(equals="Русский", ignore_case=True),
                                state=States.waiting_for_change_language)

    dp.register_message_handler(delete_face, commands="delete", state="*")
    dp.register_message_handler(upload_img_for_delete,
                                state=States.wait_for_upload_photo_for_delete_face, content_types=[ContentType.PHOTO])
    dp.register_message_handler(vignette_face, commands="vignette", state="*")
    dp.register_message_handler(upload_img_for_vignette,
                                state=States.wait_for_upload_photo_for_create_vignette, content_types=[ContentType.PHOTO])
