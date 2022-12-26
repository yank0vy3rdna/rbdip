import io

from PIL import Image, ImageFilter

from app.kafka.photo_processing import PhotoObject


async def negative(photo: PhotoObject):
    img = Image.open(io.BytesIO(photo.photo))
    img = img.filter(ImageFilter.EMBOSS)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    photo.photo = img_byte_arr.getvalue()
    return photo

