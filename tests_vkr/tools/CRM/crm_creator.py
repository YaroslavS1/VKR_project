import datetime
from typing import Union, Tuple

from VKR_project.tests_vkr.tools import BaseTime


class Record:
    # Отображает запись в CRM
    def __init__(self):
        self.srm_id = object()
        pass


class Event:
    # Отображает событие: дейсвтие одного пользователя в рамках одной 'сессии'
    def __init__(self, date: datetime.date):
        self.date = date
        self.crm_id = object()
        self.other_id = object()
        self.type = object()


class CrmReport(BaseTime):
    def __init__(self, sum_profit: float, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date]):
        super().__init__(start_date=start_date, end_date=end_date)
        # TODO подумать над структурой utm меток
        self.adv_campaigns: Tuple[str]  # Имя рекламных компаний
        self.sum_profit = sum_profit
        self.records = self.create_records
        # Нужна ли прослойка в виде класса который бы оъеденил записи по логике:
        # клиент пришел безрезультатно
        # пришел купил
        # пришел зарегистировался купил
        # и прочее

    def create_records(self):
        pass


