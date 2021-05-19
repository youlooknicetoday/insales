# InSales
Данный модуль является оберткой для API InSales

Также в модуле <a href="https://github.com/youlooknicetoday/insales/tree/master/discounts">discounts</a> пример работы с внешними скидками
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
Фильтр **where** возвращает список id 

Фильтрация по айди категории происходит следующим образом:

```python
for product_id in products.where(collection_id=18489984):
    product = products.get(product_id)
    print(product.title)
```