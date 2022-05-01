import datetime
import random
from enum import Enum
from typing import Iterable, List, Dict
from typing import Tuple
from typing import Union

from ..base import BaseTime
from ..base import get_random_ints_with_given_sum
from ..base import get_random_floats_with_given_sum

__all__ = [
    'AdvContextCRM',
    'CrmReport'

]


class AdvContextCRM:
    """Advertising campaign data in the context of CRM"""

    def __init__(self, source: str, campaign: str, profit: float, clicks: int):
        self.source = source
        self.campaign = campaign
        self.profit = profit
        self.clicks = clicks


class Rec(Enum):
    MINOR = 0
    REGISTER = 1


class RecordCrm:
    """CRM entry"""

    def __init__(self,
                 date_time: datetime.datetime,
                 crm_id: str,
                 user_id: str,
                 session: int,
                 mapped_event: str,
                 utm_source: str,
                 utm_medium: str,
                 utm_campaign: str):
        self.date_time = date_time  # date_time?
        self.crm_id = crm_id  # до момента регистрации не существует
        self.user_id = user_id
        self.session = session
        self.mapped_event = mapped_event
        self.utm_source = utm_source
        self.utm_medium = utm_medium
        self.utm_campaign = utm_campaign


class Event:
    """A class that unites a group of CRM entry within one day"""

    def __init__(self, date: datetime.date, config: Dict[AdvContextCRM, Tuple[float, int]]):
        self.date = date
        self.config = config
        self.minor_entries = random.randint(0, 5)
        self.register_entries = random.randint(0, 1)

    def get_day_entry(self):
        event_mask = []
        for i in self.config:
            for j in range(self.config[i][1]):
                event_mask.append(i)
        for i in range(self.minor_entries):
            event_mask.append(Rec.MINOR)
        for i in range(self.register_entries):
            event_mask.append(Rec.REGISTER)
        random.shuffle(event_mask)

        for i in event_mask:
            if isinstance(i, AdvContextCRM):
                pass
            elif i is Rec.MINOR:
                pass
            elif i is Rec.REGISTER:
                pass
            else:
                raise AssertionError
        return None


class CrmReport(BaseTime):
    """CRM report"""

    def __init__(self, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date],
                 config: Iterable[AdvContextCRM]):
        super().__init__(start_date=start_date, end_date=end_date)
        # TODO подумать над структурой utm меток
        # self.adv_campaigns: Tuple[str]  # Имя рекламных компаний
        # self.sum_profit = sum_profit
        self.config = config  # Количество переходов = количество кликов в рекламной
        '''
        {('рекламный источник', 'имя компании'): прибыль в рамках компании, количество кликов в рекламной компании}
        '''
        self.records = self.create_records()
        # Нужна ли прослойка в виде класса который бы оъеденил записи по логике:
        # клиент пришел безрезультатно
        # пришел купил
        # пришел зарегистировался купил
        # и прочее

    @staticmethod
    def _prepare_zero_click(clicks: List[int], profit: float):
        no_zero = len(clicks) - clicks.count(0)
        prepare_profit = []
        profit_allocation = get_random_floats_with_given_sum(no_zero, profit)
        for i in clicks:
            if i == 0:
                prepare_profit.append(0)
            else:
                prepare_profit.append(next(profit_allocation))

        return prepare_profit

    @property
    def _split_by_company(self) -> Dict[AdvContextCRM, Tuple[List[Union[int, float]], List[int]]]:
        final_split = dict()
        for i in self.config:
            clicks_allocation = [i for i in get_random_ints_with_given_sum(self.number_days, i.clicks)]
            profit_allocation = self._prepare_zero_click(clicks_allocation, i.profit)
            final_split[i] = profit_allocation, clicks_allocation
        return final_split

    @staticmethod
    def _slice_by_day(index, data) -> Dict[AdvContextCRM, Tuple[float, int]]:
        slice_ = dict()
        for k in data:
            # print(data[k][0][index], data[k][1][index])
            slice_[k] = data[k][0][index], data[k][1][index]
        return slice_

    def create_records(self):
        data = self._split_by_company
        for i, days in enumerate(self.daterange):
            days_entries = Event(days, self._slice_by_day(i, data))
            days_entries.get_day_entry()
