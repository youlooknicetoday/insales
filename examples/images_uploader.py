from io import BytesIO

from lxml import etree
from pathlib import Path

import requests
from PIL import Image

from api.src import load_config
from api.endpoints import Endpoint, Images, Products
from api.images.utils import merge, IMAGE_FILES_DIR, load_image

config_file = Path.joinpath(Path(__file__).resolve().parent.parent, 'api.ini')
config = load_config(config_file)
base = Endpoint(api=config)

images = Images()
products = Products()
products_ids = (
    245742154, 245747651, 245748382, 245748947, 245751694, 245753129, 245754207, 245754337, 245754500,
    245759317, 245760203, 245760496, 245760522, 245760561, 245761007, 245761338
)

data = requests.get('http://static.promodoma.ru/files/ontek.xml')
tree = etree.fromstring(data.content)
additional_image = load_image('mark.png')

for product_id in products_ids:
    product_title = products.get_one(product_id).removesuffix(' + подарок')
    try:
        image_url = tree.xpath(f'//name[ text() = "{product_title}"]')[0].getparent().xpath('./picture')[0].text
    except IndexError:
        continue
    image = requests.get(image_url)
    image = Image.open(BytesIO(image.content))
    image = merge(image, additional_image, convert_to_base64=True)
    response = images.create(product_id, image_attachment=image)
    print(response.content)


def update_pictures():
    additional_image = load_image('mark.png')
    for file in IMAGE_FILES_DIR.glob('*.jpg'):
        image = load_image(file.name)
        image = merge(image, additional_image)
        image.save(Path.joinpath(IMAGE_FILES_DIR, 'completed', f'new_{file.name}.png'), format='png')

