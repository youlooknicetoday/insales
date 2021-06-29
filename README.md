# InSales
Данный модуль является оберткой для API InSales реализованный на Python

### Проект находится в стадии разработки

Также в модуле <a href="https://github.com/youlooknicetoday/insales/tree/master/discounts">discounts</a> пример работы с внешними скидками
## Пример использования
Инициализация
```python
from insalesapi import InSalesAPI
from insalesapi.config import load_config

config = load_config('api.ini')
api = InSalesAPI(*config)
```
Собираем все продукты по условиям
```python
from datetime import datetime, timedelta

three_weeks = datetime.now() - timedelta(days=21)

for product in api.products.get_all(page=1, per_page=42, updated_since=three_weeks):
    print(product.title)
```
Фильтр **where** возвращает список id 

Фильтрация по id категории происходит следующим образом:

```python
for product_id in api.products.where(collection_id=18489984):
    product = api.products.get(product_id)
    print(product.title)
```

Также есть фильтр сопутсвующих товаров:
```python
for product_id in api.products.related(product_id=product_id):
    product = api.products.get(product_id)
    print(product.title)
```

## Релизовано

Ресурсы добавляются по мере необходимости, на данный момент есть самые нужные для повседневной работы
<ul>
<li>Продукты</li>
<li>Изображения</li>
<li>Заказы</li>
<li>Категории</li>
</ul>