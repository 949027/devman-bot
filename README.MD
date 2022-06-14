# Сервис уведомлений о проверке работ 
Скрипт отправляет ученику сообщения о результате проверки работ на 'Devman'

### Как установить
1. Python3 должен быть уже установлен. 
2. Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.
3. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```python
pip install -r requirements.txt
```
4. Создайте бота и получите токен у бота `@BotFather`.
5. Узнайте свой `id` в Telegram у бота `@userinfobot`.
6. Получите токен для API Devman по [ссылке](https://dvmn.org/api/docs/) (вы должны быть авторизированы на сайте).
7. Создайте файл ```.env``` в корне проекта и пропишите в нем переменные окружения:`TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`, `DEVMAN_TOKEN`.
### Как пользоваться
Запустите скрипт командой:
```python
python devman_bot.py 
```
Когда преподаватель проверит вашу работу - вы получите результат в Telegram.
При сбоях в работе бота вы получите сообщение в Telegram. 

### Docker на локальной машине
1. Установите [Docker](https://docs.docker.com/get-started/).

2. Перейдите в корень проекта и соберите образ командой:
```commandline
docker build -t devman-bot .
```
3. Запустите контейнер командой:
```commandline
docker run -dp 3000:3000 --env-file ./.env devman-bot
```
4. В телеграм должно придти сообщение о включении бота. Если этого не случилось, узнайте ID контейнера командой: 
```commandline
docker ps -all
```
и изучите логи командой:
```commandline
docker logs -f <container-id>
```