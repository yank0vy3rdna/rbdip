import io

from PIL import Image, ImageFilter

from app.database.model import Photo


async def vignette(photo: Photo):
    img = Image.open(io.BytesIO(photo.photo))
    img = img.filter(ImageFilter.CONTOUR)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    photo.photo = img_byte_arr.getvalue()
    return photo

