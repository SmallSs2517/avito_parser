from consts import *
from time import sleep
from session import session_handler
from parcer import get_prices
from data_handler import db_handler
from datetime import datetime
from threading import Thread
from queue import SimpleQueue

db_in_queue = SimpleQueue()
db_work_out_queue = SimpleQueue()
db_report_out_queue = SimpleQueue()

def build_url(base_url: str, path: list[dict]) -> list[str]:
    urls = []
    for i in path:
        url = base_url
        _path = i.copy()
        _path['RADIUS'] = f'&radius={i['RADIUS']}&searchRadius={i['RADIUS']}'
        for l in _path:
            url += _path[l]
        urls.append(url)
    return urls



if __name__ == "__main__":
    
    
    db_thread = Thread(target=db_handler,
                       name='db_thread',
                       args=(db_in_queue, db_work_out_queue, db_report_out_queue),
                       daemon=True
                       )

    try:
        db_thread.start()
        
        while True:
            print(f'\n{datetime.now().time().isoformat('seconds')}\nПоехали!!!\n') # Лог в консоль
            
            db_in_queue.put(('gm',))
            models = db_work_out_queue.get()
            target_urls = build_url(BASE_URL, models)
            all_data = []            
            
            for url in target_urls:
                pages = session_handler(url)
                if pages == None:
                    print("From 'main_flow':\nssession_handler вернул None(((\n")
                    sleep(600)
                    continue
                
                for page in pages:
                    data = get_prices(page)
                    all_data += data
                    print(f'Данные страницы {pages.index(page)+1} записаны\n') # Лог в консоль                

                average = int(sum(all_data) / len(all_data))
                db_in_queue.put(('wa', (len(all_data), average, 1)))

                if db_work_out_queue.get():
                    print(f'\n{datetime.now().time().isoformat('seconds')}\nТаймер в 10 минут пошел\n') # Лог в консоль
                    sleep(600)
                else:
                    print(f'\n{datetime.now().time().isoformat('seconds')}\nОшибка в записи в БД\n') # Лог в консоль

    except:
        print(f'\n{datetime.now().time().isoformat('seconds')}\nОшибка в основном цикле\n') # Лог в консоль
        exit()
    finally:
        pass
