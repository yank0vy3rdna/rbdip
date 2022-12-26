from enum import Enum

from tg_bot.database.model import Photo
from worker.image_processing.delete_faces import delete_faces
from worker.image_processing.detail import detail
from worker.image_processing.negative import negative
from worker.image_processing.sharp import sharp
from worker.image_processing.smooth import smooth
from worker.image_processing.vignette import vignette


class ProcessingTypes(Enum):
    VIGNETTE = "vignette"
    DELETE_FACES = "delete_faces"
    DETAIL = "detail"
    SHARP = "sharp"
    NEGATIVE = "negative"
    SMOOTH = "smooth"


async def process_image(photo: Photo, processing_type: ProcessingTypes) -> Photo:
    proc_f = {
        ProcessingTypes.VIGNETTE: vignette,
        ProcessingTypes.DELETE_FACES: delete_faces,
        ProcessingTypes.DETAIL: detail,
        ProcessingTypes.SHARP: sharp,
        ProcessingTypes.NEGATIVE: negative,
        ProcessingTypes.SMOOTH: smooth
    }[processing_type]
    return await proc_f(photo)
