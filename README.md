# InSales
Данный модуль является оберткой для API InSales

## Пример использования
Инициализация
```python
from insalesapi.src import init_credentials
from insalesapi.endpoints import Product

init_credentials('api.ini')
products = Product()
```
Собираем все продукты по условиям
```python
from datetime import datetime, timedelta

three_weeks = datetime.now() - timedelta(days=21)

for product in products.get_all(page=1, per_page=42, updated_since=three_weeks):
    print(product.title)
```
Фильтрация по айди категории происходит следующим образом <br>
Фильтр <strong>where</strong> возвращает список id 
```python
for product_id in products.where(collection_id=18489984):
    product = products.get(product_id)
    print(product.title)
```