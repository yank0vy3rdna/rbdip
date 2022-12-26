import io

from PIL import Image, ImageFilter

from tg_bot.database.model import Photo


async def smooth(photo: Photo):
    img = Image.open(io.BytesIO(photo.photo))
    img = img.filter(ImageFilter.SMOOTH)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    photo.photo = img_byte_arr.getvalue()
    return photo

