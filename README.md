# post telegram image
Данный скрипт используется для чат бота в telegram. Скрипт скачивает фотографии используя API NASA и SpaceX, и публикует по одной фотографии раз в сутки.

Все фото по умолчанию сохраняются в папке images. Для изменения папки измените значение переменной directory.

Фотографии NASA скачиваются за последний месяц. Для получения фотографий SpaceX скрипт берет случайный запуск по номеру от 1 до 100.

## Как установить
Python3 уже должен быть установлен. Рекомендуется использовать venv для изоляции проекта.

Затем используйте pip для установки зависимостей

`pip install -r requirements.txt`

## Цель проекта
Образовательная цель в рамках изучения API и библиотек requests и python-telegram-bot
 
### Для скрытия данных используется .env файл и соответствующие переменные
tg_token = os.getenv('TG_KEY') - уникальный токен чат бота. Необходимо получить токен от чат бота у @BotFather. Используется методами для взаимодействия с ботом.

nasa_key = os.getenv('NASA_API_KEY') - ключ API NASA. Можно использовать ограниченный ключ DEMO_KEY либо получить свой зарегистрировшись по ссылке https://api.nasa.gov/. Используется при get запросах к данным NASA

tg_chat_id = os.getenv('TG_CHAT_ID') - ID чата. Можно получить отправив сообщение боту @ShowJsonBot. Использовать значение из ответа в поле id. Используется методами для взаимодействия с ботом.
 
## Пример запуcка
 
Запуск осуществляется из IDE или из командной строки командой
```
python main.py
```
