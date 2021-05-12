from io import BytesIO
from pathlib import Path
from PIL import Image


from insalesapi.src import init_credentials
from insalesapi.images.endpoints import ImagesController
from insalesapi.images.utils import merge, IMAGE_FILES_DIR, load_image
from insalesapi.products.endpoints import ProductsController


additional_image = load_image('mark.png')

for product_id in products_ids:
    product_title = products.get_one(product_id).removesuffix(' + подарок')
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


def get_all_promo_bundles(category_id):
    pass


def get_all_():
    pass


def main():
    images = images_controller.get_all('245742154')
    image_ids = [image.id for image in images.list]
    print(image_ids)


if __name__ == '__main__':
    config_file = Path.joinpath(Path(__file__).resolve().parent.parent, 'api.ini')
    init_credentials(config_file)
    images_controller = ImagesController()
    products_controller = ProductsController()
    main()
