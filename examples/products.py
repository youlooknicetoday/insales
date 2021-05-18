from pathlib import Path

from datetime import datetime, timedelta
from insalesapi.src import init_credentials
from insalesapi.endpoints import Product


config_file = Path.joinpath(Path(__file__).parent.parent, 'api.ini')
init_credentials(config_file)

products = Product()
three_weeks = datetime.now() - timedelta(days=21)

for product in products.get_all(page=1, per_page=42, updated_since=three_weeks):
    print(product.title)

for product_id in products.where(collection_id=18489984):
    product = products.get(product_id)
    print(product.title)
