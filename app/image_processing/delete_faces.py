import io

from PIL import Image, ImageFilter

from app.database.model import Photo
from app.utils.request import send_request_yandex_vision


async def delete_faces(photo: Photo):
    result = send_request_yandex_vision(photo.photo)
    img = Image.open(io.BytesIO(photo.photo))
    for list_x, list_y in result:
        max_x = max(list_x)
        min_x = min(list_x)
        max_y = max(list_y)
        min_y = min(list_y)
        cropped_img = img.crop((min_x, min_y, max_x, max_y))
        cropped_img = cropped_img.filter(ImageFilter.GaussianBlur(radius=10))
        img.paste(cropped_img, (min_x, min_y))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    photo.photo = img_byte_arr.getvalue()
    return photo
