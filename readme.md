avito parser

ОБЩАЯ КОНЦЕПЦИЯ

Задача инструмента заключается в отслеживании изменения средней цены на определенный товар на авито .
Данный пример для отслеживания автомобилей.

Получаем несколько страниц с некоторым количеством предложений. Собираем все цены и вычисляем среднюю на 
текущий момент времени. Инструмент работает постоянно, собирая данные какое-то количество раз в сутки и 
формирует статистику. Целевой товар в данном варианте кода - автомобили, все написанное ниже подразумевает
работу с автомобилями

***

Поэтапно:

0. Определение целевого товара, региона поиска и т.п.
1. Создание сессии с avito и получение страницы с предложениями
2. Парсинг данных со страницы и заполнение таблицы БД
3. Формирование (оформление) статистики
4. Интерфейс для вывода отчетов по запросу пользователя
5. Работа интерфейса для возможности настройки работы приложения

***

Теперь по каждому этапу подробнее:

0. Так как инструмент может отслеживать сразу несколько товаров будет удобнее сделать отдельную таблицу БД.
Достаточный для корректной работы инструмента набор полей:
- Дата (создания строки)
- Регион поиска
- Производитель
- Модель
- Поколение
- Радиус поиска (авито так хочет)
- Отслеживать? (булиевая переменная, включатель)

При создании соединения с авито ссылка для HTTP запроса формируется исходя из этих данных. Поле "Отслеживать"
можно использовать для управления инструментом.

***

1. Создание сессии - заход на страницу авито со всеми заголовками и прочими танцами против защиты от парсинга.
Этот модуль подразумевает создание экземпляра касса Session, а также функций для создания сессии и для отправки 
запроса(-ов) и получения html файла(-ов).

***

2. Данные из полученной страницы собирает парсер на bs4. После обработки всех страниц вычисляется средняя цена
и заполняется БД 

***

3. 

***

4. 

***

5. 

***

Весь проект подразумевает модули для:

1. Выполнения HTTP запросов (requests)
2. Парсинга полученных страниц (BeautifulSoup4)
3. Работы с БД (sqlite, SQLAlchemy)
4. Формирования отчетов (matplotlib???)
5. Управления инструментом и получения отчетов (Telebot, aiogram)
