import requests
from bs4 import BeautifulSoup
from time import sleep
from consts import HEADERS, BASE_URL


session = requests.Session()

def session_handler(target_url: str) -> list | None:
    """
    Вызывает функции в модуле и возвращает список со всеми страницами.\n
    Создает сессию, затем получает первую страницу и добавляет её в список htmls.\n
    Если не удалось получить первую страницу - вернет None.\n
    Проверяет наличие других страниц и получает их, добавляя в список htmls.\n
    Возвращает htmls.
    """
    
    htmls = []
    attempts = 0

    start_session(BASE_URL, HEADERS)
    
    while True:
        if attempts >= 3:
            return None
        
        html = get_html(url=target_url, wait=bool(attempts)) # Получаем первую страницу
        if html:
            htmls.append(html)
            print('Первая страница получена\n')
        else:
            print('From "session_handler":\nСтраница 1 не получена\n')
            attempts += 1
            continue

        urls = check_quantity(htmls[0], url=target_url) # Проверяем количество объявлений и корректность страницы
        if urls != False:
            break
        else: 
            attempts += 1
            continue
                    
    for i in urls:      # Проходимся по списку адресов, делая запросы и добавляя результаты в htmls
        attempts = 0
        while True:
            if attempts >= 3:
                print(f'From "session_handler":\nНе удалось получить страницу {urls.index(i)+2}\n')
                return None
            
            html = get_html(url=i, wait=True)
            html = check_page(html)
            if html:
                htmls.append(html)
                print(f'{urls.index(i)+2} страница получена\n')
                break
            else:
                print(f'From "session_handler":\nСтраница {urls.index(i)+2} не получена\n')
                attempts += 1
        
    return htmls


def start_session(url: str, headers: dict) -> bool:
    """Создает сессию с Авито, а если не удалось - возвращает False"""
    
    try:
        res = session.get(url=url, headers=headers)
    except Exception as exc:
        print('Session was not created\n', exc.__str__())
        return False
    
    print('Session created' if res.status_code == 200 else res.status_code)
    return True


def get_html(url: str, wait: bool = False) -> str | bool:
    """Делает GET запрос на переданный url и возвращает либо страницу, либо False"""
    
    if wait:
        sleep(60)

    for _ in range(3):      # Трижды пробуем получить страницу
        try:
            res = session.get(url=url)
            html = res.text
        except Exception as exc:
            print('From "get_html":\nНе удалось получить страницу\n', exc)
            html = False
        if html:            # Если страница получена, прекращаем цикл
            break
        sleep(60)
        
    return html
    

def check_quantity(html: str, url: str) -> list | bool:
    """
    Достает из полученной html количество выданных Авито объявлений, считает\n
    количество страниц и формирует список ссылок на эти страницы, начиная со второй.\n
    Если страница одна - вернет пустой список. Вернет None, если получена неожиданная\n
    страница (например с капчей).
    """
    
    urls = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        quantity = int(soup.find('span', {"data-marker": "page-title/count"}).get_text())
    except:
        print("From 'check_quantity': Error in soup.find")
        return False
    
    if quantity <= 50:      # Если страница одна, то вернет пустой список
        return urls

    count = quantity//50
    if quantity%50 != 0:    # Этот кусочек нужен, чтобы учитывать страницу с "аппендиксом" - остатком деления на 50
        count += 1

    for i in range(2, count+1, 1):
        urls.append(url+f'&p={i}')
    
    print(f'Страниц по запросу - {count}\n')
    return urls


def check_page(page: str) -> str | bool:
    """Проверяет корректность полученной страницы"""
    
    try:
        soup = BeautifulSoup(page, 'html.parser')
        items = soup.find('div', {"data-marker": "catalog-serp"}).find_all('div', {"data-marker": "item"})
    except:
        print("From 'check_page': Получена не корректная страница")
        return False    
    return page