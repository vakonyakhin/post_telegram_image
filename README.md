# post telegram image
Данный скрипт используется для чат бота в telegram. Скрипт скачивает фотограции используя API NASA и SpaceX, и публикует их в чате. По одной фотографии раз в сутки.

Все фото по умолчанию сохраняются в папке images. Для изменения папки измените значение переменной directory

Фотографии NASA скачиваются за последний месяц. Для получения фотографий SpaceX скрипт берет случайный запуск по номеру от 1 до 100.

## Как установить
Python3 уже должен быть установлен.Рекомендуется использовать venv для изоляции проекта.

Затем используйте pip для установки зависимостей

`pip install -r requirements.txt`

## Цель проекта
Образовательная цель в рамках изучения API и библиотек requests и python-telegram-bot
 
## Используемы переменные окружения
TG_KEY - токен чат бота. Необходимо получить токен от чат бота у @BotFather. 

NASA API KEY - ключ API NASA. Можно использовать ограниченный ключ DEMO_KEY либо получить свой зарегистрировшись по ссылке https://api.nasa.gov/

CHAT_ID - ID чата. Можно получить отправив сообщение боту @ShowJsonBot. Использовать значение из ответа в поле id
 
## Пример запуcка
 
### Для скрытия данных используется .env файл и соответствующие переменные
 
```
from dotenv import load_dotenv
 
load_dotenv()
 
chat_id = os.getenv('CHAT_ID')
    
tg_token = os.getenv('TG_KEY')

nasa_key = os.getenv('NASA_API_KEY')
```
 
Запуск осуществляется из IDE или из командной строки 
```
python main.py
```
