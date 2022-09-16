import re
import sqlite3
import time
import math


day = 60 * 60 * 24
addMemoriRe = r"^<\d{1,}>"
text_help = """
В треугольных скобках(<>) пишутся параметры. Можно пропускать если указано в подсказке к команде.\n
$addmemori <количество дней хранения текста, больше нуля и четное> ваш текст для сохранения - сохраняет сообщение на один день или введенное вами число\n
$delmemori номер удаляемого сообщения\n
$memori - выводит все сохранённые сообщения на канале\n
$allmemori - выводит все сохранённые сообщения на сервере\n
$help - пишет подсказки команд\n
"""


def requestData(request_text, save=False):
    cnx = sqlite3.connect("data.db")
    cursor = cnx.cursor()
    cursor.execute(request_text)
    if save:
        cnx.commit()
    out = cursor.fetchall()
    cnx.close()
    return out


def savememori(text, c_id, u_id, s_id):
    nday = 1
    val = re.findall(addMemoriRe, text)
    if val:
        if int(val[0][1:-1]) > 0:
            text = "".join(re.split(addMemoriRe, text)[1:])
            nday = int(val[0][1:-1])
    t = time.time() + (day * nday)
    text = str(u_id) + ": " + text
    requestData(
        "INSERT INTO memori VALUES ("
        + str(t)
        + ", '"
        + text
        + "', "
        + str(c_id)
        + ", "
        + str(s_id)
        + ", "
        + str(nday)
        + ");",
        True,
    )


def loadmemori(check_id, whose_id):
    t = time.time()
    requestData("DELETE FROM memori WHERE time_end < " + str(t) + ";", True)
    memori = requestData("SELECT * FROM memori;")
    out = "Сохраненные сообщения:\n"
    n = 0
    for i in memori:
        if whose_id == "channel":
            db_id = i[2]
        if whose_id == "server":
            db_id = i[3]
        if db_id == check_id:
            n += 1
            day_stay = str(math.ceil((i[0] - time.time()) / day))
            out += (
                str(n)
                + ". "
                + i[1]
                + "\n Время хранения: "
                + str(i[4])
                + "\nОсталось дней хранения: "
                + day_stay
                + "\n"
            )
    return [out, n]


def deletememori(index, id_server):
    memori = requestData("SELECT * FROM memori WHERE id_server ==" + str(id_server) + ";")
    if index >= 1 and index <= len(memori):
        # время в данном случии как id
        time_end = memori[index - 1][0]
        requestData("DELETE FROM memori WHERE time_end == " + str(time_end) + ";", True)
        return "Сообщение удаленно"
    return "Данного номера сообщения не существуюет"


class Generaldb(object):
    def create(self):
        try:
            requestData("SELECT * FROM memori")
        except Exception:
            requestData(
                """CREATE TABLE memori
               (time_end real,  title text, id_channel INTEGER, id_server INTEGER, cout_day INTEGER)""",
                True,
            )

    def delete(self):
        requestData("DROP TABLE memori;", True)
