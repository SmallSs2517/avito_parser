from datetime import datetime
from queue import SimpleQueue
from db_models.database import SyncORM

# Временное решение для тестов
# def add_marker():
#     with open('avito_parser/src/data.txt', 'a+', encoding='UTF-8') as file:
#         file.write(str(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))+'\n')

# def add_data(data: list[int], number: int):
#     pr_data = []
#     for i in data:
#         pr_data.append(str(i)+', ')

#     with open('avito_parser/src/data.txt', 'a+', encoding='UTF-8') as file:
#         file.write(f'Страница номер {number}: ' + '\n')
#         file.writelines(pr_data)
#         file.write('\n')

# def add_average(data: int):
#     pr_data = '\n' + 'Средняя цена: ' + str(data) + '\n'
#     with open('avito_parser/src/data.txt', 'a+', encoding='UTF-8') as file:
#         file.write(pr_data)
#         file.write('\n________________________\n')


def db_handler(in_queue: SimpleQueue, work_out_queue: SimpleQueue, report_out_queue: SimpleQueue):
    """
    Из in_queue очереди получаем кортеж, первым элементом которого должны быть флаги: \n
    'gm' - Get Models. Флаг: str \n
    'wa' - Write Average. Флаг: str и кортеж (offers: int, average: int, model_id: int) \n
    'gca' - Get Current Average. Флаг: str и id модели: int \n
    'gaa' - Get All Average. Флаг: str и id модели: int \n
    'gads' - Get Average Data Selection. Флаг: str и кортеж (id модели: int, (от: datetime, до: datetime)) \n

    """
    try:
        while True:
            print(f'\n{datetime.now().time().isoformat('seconds')}\nFrom db_thread: Ждет задачу из очереди\n') # Лог в консоль
            task = in_queue.get()

            if task[0] == 'gm':
                resp = SyncORM.select_all_models()
                work_out_queue.put(resp)

            elif task[0] == 'wa':
                try:
                    args = task[1]
                    SyncORM.insert_average_price(args[0], args[1], args[2])
                except:
                    work_out_queue.put(False)
                else:
                    work_out_queue.put(True)
            
            elif task[0] == 'gca':
                pass
            
            elif task[0] == 'gaa':
                pass
            
            elif task[0] == 'gads':
                pass
    except:
        print("From 'db_handler':\nошибка в операция с БД\n")
        return
