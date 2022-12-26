from enum import Enum


class Topics(Enum):
    PROCESSED_IMAGES = "processed_images"  # processed photo.id to send back to user
    IMAGE_PROCESSING = "image_processing"  # uploaded photo.id to process it, with processing type
