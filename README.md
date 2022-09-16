# Дискорд бот LimiBot

### Version 0.1

### Описание
LimiBot - это бот созданый, чтобы помочь организовать работу в команде. Он поможет вам с трудностями напоминания и путаницы.
На данный момент бот еще обладает маленьким спектром возможностей, но планируется добавить еще множество крутых функций.<br>
Доступные команды бота на текущий момент:<br>
В треугольных скобках(<>) пишутся параметры. Можно пропускать если указано в подсказке к команде.<br>
$addmemori <количество дней хранения текста, больше нуля и четное> ваш текст для сохранения - сохраняет сообщение на один день или введенное вами число<br>
$delmemori номер удаляемого сообщения<br>
$memori - выводит все сохранённые сообщения на канале<br>
$allmemori - выводит все сохранённые сообщения на сервере<br>
$help - пишет подсказки команд<br>

### Инструкция по установке и запуску
1. Создайте токен. Перейдите по этой [ссылки](https://discord.com/developers/applications) и создайте приложение для бота и получите токен.
Там же добавите его на свой сервер. Как это сделать можно найти в интернете.
2. Вставьте токен в bot.py:
```python
token = "Ваш токен"
```
3. Запустите бота:
```sh
python3 bot.py
```
