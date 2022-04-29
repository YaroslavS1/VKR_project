import datetime
import random
from typing import Union, Tuple

from VKR_project.tests_vkr.tools import BaseTime


class RecordCrm:
    # Отображает запись в CRM
    def __init__(self,
                 date: datetime.date,):
        self.date = date  # date_time?
        self.srm_id = object()  # до момента регистрации не существует
        self.other_id = object()
        self.action = object()
        self.mapped_event = object()
        self.profit = object()

        # utm_source
        # utm_medium
        # utm_campaign
        # utm_content
        # utm_term


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

    @staticmethod
    def constrained_sum_sample_pos(n, total):
        """Return a randomly chosen list of n positive integers summing to total.
        Each such list is equally likely to occur."""
        values = [0.0] + [round(random.triangular(0, total), 2) for i in range(n - 1)] + [total]
        values.sort()
        return iter([values[i + 1] - values[i] for i in range(len(values) - 1)])

    def create_records(self):
        records = list()
        number_days = int((self.end_date - self.start_date).days)+1
        cost_allocation = self.constrained_sum_sample_pos(number_days, self.sum_profit)
        for date in self.daterange:
            records.append(
                RecordCrm(
                    date=date,
                ))
