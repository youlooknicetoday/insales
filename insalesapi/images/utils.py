from io import BytesIO
from pathlib import Path
from PIL import Image
import base64


IMAGE_FILES_DIR = Path.joinpath(Path(__file__).resolve().parent, 'files')


# Convert Image to Base64 
def convert_image_to_base64(image: Image):
    buff = BytesIO()
    image.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str


def merge(base_image: Image, additional_image: Image, convert_to_base64: bool = False):
    base_image = base_image.convert("RGBA")
    width, height = base_image.size
    width_for_mark = width // 4
    height_for_mark = height // 4
    additional_image = additional_image.resize((width_for_mark, height_for_mark), Image.ANTIALIAS)
    base_image.alpha_composite(additional_image, (width - width_for_mark - 40, height - height_for_mark - 40))
    if convert_to_base64:
        return convert_image_to_base64(base_image)
    return base_image


def load_image(filename: str) -> Image:
    image = Image.open(Path.joinpath(IMAGE_FILES_DIR, filename))
    return image
