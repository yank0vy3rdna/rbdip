from enum import Enum

from app.database.model import Photo
from app.image_processing.delete_faces import delete_faces
from app.image_processing.vignette import vignette


class ProcessingTypes(Enum):
    VIGNETTE = "vignette"
    DELETE_FACES = "delete_faces"


async def process_image(photo: Photo, processing_type: ProcessingTypes) -> Photo:
    proc_f = {
        ProcessingTypes.VIGNETTE: vignette,
        ProcessingTypes.DELETE_FACES: delete_faces,
    }[processing_type]
    return await proc_f(photo)
