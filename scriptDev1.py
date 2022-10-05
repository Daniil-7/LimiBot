import re


class FormEvent:
    def name(self, nicks, server):
        out = re.findall(r"<@\d{18}>", nicks)
        out = list(map(lambda nick: nick[2:-1], out))
        serverValid = re.findall(r"<server>", nicks)
        if serverValid:
            out.append(server)
        return out if out else None

    def number(self, period):
        period = " ".join(period.split())
        out = re.findall(r"^[1-9]+$", period)
        return int(out[0]) if out else None
    
    def time(self, arg_time):
      arg_time = " ".join(arg_time.split())
      out = re.findall(r"^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", arg_time)
      return out[0] if out else None


class InputEvent:
  def __init__(self):
    self.user_data = {}
    self.fe = FormEvent()
  
  def start(self, id_user):
    self.user_data[id_user] = {
      "receiver": [], # получатели
      "remind": 0, # период напоминания(в днях)
      "wait": 0, # через сколько дней напомнить
      "frequency": 0, # частота напоминания
      "from_time": "", # начало времени отправки во время дня
      "before_time": "", # конец времени отправки во время дня
      "stage": 0, # этап заполнения
    }
    return """
    Создание напоминания(event)!
    Отвечайте на вопросы с помошью команды $ep($ep ваш ответ)
    1) Введите ники людей которым нужно напомнить или введите: <server>, что бы отправлять в этот канал 
    """
  
  def post(self, id_user, id_server, message):
    if not self.user_data.__contains__(id_user):
      return """
      Сначало надо начать создание нопоминания(event)!
      Введите $es чтобы начать!
      """
      
      
    stage = self.user_data[id_user]["stage"]
    if  stage == 0:
      name = self.fe.name(message, id_server)
      if name:
        self.user_data[id_user]["receiver"] = name
        self.user_data[id_user]["stage"] += 1
        return """
        Получатели успешно сохранены!
        2) период напоминания(в днях)
        """
      return """
        Данные не корректные!!!
        1) Введите ники людей которым нужно напомнить или введите: <server>, что бы отправлять в этот канал
      """
      
      
    if stage == 1:
      day = self.fe.number(message)
      if day:
        self.user_data[id_user]["remind"] = day
        self.user_data[id_user]["stage"] += 1
        return """
        Период напоминания сохранен!
        3) Через сколько дней напомнить
        """
      return """
        Данные не корректные!!!
        2) Период напоминания(в днях)
      """
      
      
    if stage == 2:
      day = self.fe.number(message)
      if day:
        self.user_data[id_user]["wait"] = day
        self.user_data[id_user]["stage"] += 1
        return """
        Через какое количество дней напомнить сохранено!
        4) Частота напоминания в день. Не может быть больше 10
        """
      return """
        Данные не корректные!!!
        3) Через сколько дней напомнить
      """
      
      
    if stage == 3:
      day = self.fe.number(message)
      if day:
        if day < 11:
          self.user_data[id_user]["frequency"] = day
          self.user_data[id_user]["stage"] += 1
          return """
            Частота напоминания в день сохранена!
            5) Время напоминание(промежуток) со скольки?
          """
      return """
        Данные не корректные!!!
        4) Частота напоминания в день. Не может быть больше 10
      """
      
      
    if stage == 4:
      from_time = self.fe.time(message)
      if from_time:
        self.user_data[id_user]["from_time"] = from_time
        self.user_data[id_user]["stage"] += 1
        return """
        Время напоминание(промежуток) со скольки сохранено!
        6) Время напоминание(промежуток) до скольки
        """
      return """
        Данные не корректные!!!
        5) Время напоминание(промежуток) со скольки?
      """
      
    if stage == 5:
      before_time = self.fe.time(message)
      if before_time:
        self.user_data[id_user]["before_time"] = before_time
        self.user_data[id_user]["stage"] += 1
        return """
        Время напоминание(промежуток) до скольки сохранено!
        7) 
        """
      return """
        Данные не корректные!!!
        6) Время напоминание(промежуток) до скольки?
      """
    
        
  
  


# testing InputEvent
ie = InputEvent()
print(ie.start(626832798258429952))
print(ie.post(626832798258429952, 626832798258429952, "<server>"))




# testing FormEvent
fe = FormEvent()
print(
    fe.name( """
  a<@626832798258429952>
  <@626832798258429952> 
  <server>
  """,
        "626832798258429952",
    )
)
print(fe.number("   1   "))
print(fe.time("2:00"))
