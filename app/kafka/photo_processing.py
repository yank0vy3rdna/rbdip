import dataclasses
import marshal

from worker.image_processing import ProcessingTypes


@dataclasses.dataclass
class PhotoObject:
    processing_type: ProcessingTypes
    photo: bytes
    photo_id: str

    def dump(self) -> bytes:
        return marshal.dumps(self)


def load(obj: bytes) -> PhotoObject:
    return marshal.loads(obj)
