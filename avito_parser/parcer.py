"""
В HTML странице с авито контейнер (<div>) с объявлениями по запросу промаркирован как data-marker="catalog-serp"
Сокращенно структура до цены объявления следующая:

<div data-marker="catalog-serp">
    <div data-marker="item">
        <p data-marker="item-price">
            <meta itemprop="price" content=ИСКОМАЯ ЦЕНА
        </p>
    </div>
</div>
"""
"""
____Это работает____
with open('educational_projects/avito_parser_v2/src/html_1.html', 'r', encoding='UTF-8') as file:
    page = file.read()

soup = BeautifulSoup(page, 'html.parser')
res = soup.find('div', {'data-marker': 'item-date/wrapper'})

print(type(res))
print(res)
"""

from bs4 import BeautifulSoup

def get_prices(page: str) -> list[int]:
    """Получает HTML страницу и возвращает список цен"""

    prices = list()
    soup = BeautifulSoup(page, 'html.parser')

    items = soup.find('div', {"data-marker": "catalog-serp"}).find_all('div', {"data-marker": "item"})

    for item in items:
        p = item.find('p', {"data-marker": "item-price"})
        prices.append(int(p.find('meta', {"itemprop": "price"}).attrs['content']))

    return prices

