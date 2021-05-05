from pathlib import Path

from api.src import load_config
from api.images.crud import CRUD
from api.images.utils import merge, IMAGE_FILES_DIR, load_image


config_file = Path.joinpath(Path(__file__).resolve().parent, 'api.ini')
worker = load_config(config_file)
images_worker = CRUD(worker)


def update_pictures():
    additional_image = load_image('mark.png')
    for file in IMAGE_FILES_DIR.glob('*.jpg'):
        image = load_image(file.name)
        image = merge(image, additional_image)
        image.save(Path.joinpath(IMAGE_FILES_DIR, 'completed', f'new_{file.name}.png'), format='png')


update_pictures()
