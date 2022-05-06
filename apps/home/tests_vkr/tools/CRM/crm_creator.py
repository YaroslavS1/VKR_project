import datetime
import math
import random
from enum import Enum
from typing import Iterable, List, Dict, Optional
from typing import Tuple
from typing import Union

from VKR_project.apps.home.core_convert.crm import prepare
from ..base import BaseTime
from ..base import pseudo_data
from ..base import get_random_ints_with_given_sum
from ..base import get_random_floats_with_given_sum

__all__ = [
    'AdvContextCRM',
    'CrmReport'

]

EVENT_LIST = ('brand_page', 'catalog_page', 'brand_page', 'OpenProductPage', 'Open_ProductSpecs')


class AdvContextCRM:
    """Advertising campaign data in the context of CRM"""

    def __init__(self, source: str, campaign: str, profit: float, clicks: int):
        self.source = source
        self.campaign = campaign
        self.profit = profit
        self.clicks = clicks


class _AdvContextCRM:
    def __init__(self, source: str, campaign: str, profit: float, clicks: int):
        self.source = source
        self.campaign = campaign
        self.profit = profit
        self.clicks = clicks

    def __repr__(self):
        return f'{self.source} {self.campaign} {self.profit} {self.clicks}'


class Rec(Enum):
    MINOR = 0
    REGISTER = 1
    ADDTOCART = 2


class RecordCrm:
    """CRM entry"""

    def __init__(self,
                 date_time: datetime.date,
                 crm_id: Optional[str],
                 user_id: str,
                 session: int,
                 mapped_event: str,
                 utm_source: Optional[str],
                 # utm_medium: str,
                 utm_campaign: Optional[str],
                 profit: Optional[float] = None):
        self.date_time = date_time  # date_time?
        self.crm_id = crm_id  # до момента регистрации не существует
        self.user_id = user_id
        self.session = session
        self.mapped_event = mapped_event
        self.utm_source = utm_source
        # self.utm_medium = utm_medium
        self.utm_campaign = utm_campaign
        self.profit = profit

    def __repr__(self):
        return f'|{self.profit}|'


class Event:
    """A class that unites a group of CRM entry within one day"""

    def __init__(self, date: datetime.date, config: Dict[AdvContextCRM, Tuple[float, int]]):
        self.date = date
        self.config = config
        self.minor_entries = random.randint(0, 5)
        self.register_entries = random.randint(0, 1)
        self.addto_cart_entries = random.randint(0, 1)

    @staticmethod
    def _get_dummy_event(date, mapped_event, current_id, current_session):
        return RecordCrm(
            date_time=date,
            crm_id=None,
            user_id=current_id,
            session=current_session,
            mapped_event=mapped_event,
            utm_source=None,
            utm_campaign=None)

    def get_day_entry(self, pseudo_id, pseudo_session):
        event_mask = []
        for i in self.config:
            if self.config[i][1] != 0:
                event_mask.append(_AdvContextCRM(i.source, i.campaign, *self.config[i]))
        for i in range(self.minor_entries):
            event_mask.append(Rec.MINOR)
        for i in range(self.register_entries):
            event_mask.append(Rec.REGISTER)
        for i in range(self.register_entries):
            event_mask.append(Rec.ADDTOCART)
        random.shuffle(event_mask)
        daily_events = []

        for i in event_mask:
            if isinstance(i, _AdvContextCRM):
                current_price = get_random_floats_with_given_sum(i.clicks, i.profit)
                for j in range(0, i.clicks):
                    _current_price = next(current_price)
                    current_id = next(pseudo_id)
                    current_session = next(pseudo_session)
                    daily_events.append(RecordCrm(
                        date_time=self.date,
                        crm_id=None,
                        user_id=current_id,
                        session=current_session,
                        mapped_event='session_start',
                        utm_source=i.source,
                        utm_campaign=i.campaign))
                    for event_ in EVENT_LIST:
                        daily_events.append(self._get_dummy_event(self.date, event_, current_id, current_session))
                    if _current_price == 0.:
                        if random.randint(0, 2):
                            daily_events.append(RecordCrm(
                                date_time=self.date,
                                crm_id=None,
                                user_id=current_id,
                                session=current_session,
                                mapped_event='AddTo_Cart',
                                utm_source=None,
                                utm_campaign=None))
                            if random.randint(0, 1):
                                daily_events.append(RecordCrm(
                                    date_time=self.date,
                                    crm_id=None,
                                    user_id=current_id,
                                    session=current_session,
                                    mapped_event='pass',
                                    utm_source=None,
                                    utm_campaign=None))
                    else:
                        daily_events.append(RecordCrm(
                            date_time=self.date,
                            crm_id=None,
                            user_id=current_id,
                            session=current_session,
                            mapped_event='AddTo_Cart',
                            utm_source=None,
                            utm_campaign=None))
                    if _current_price == 0.:
                        pass
                        # if random.randint(0, 1):
                        #     daily_events.append(RecordCrm(
                        #         date_time=self.date,
                        #         crm_id=None,
                        #         user_id=current_id,
                        #         session=current_session,
                        #         mapped_event='pass',
                        #         utm_source=None,
                        #         utm_campaign=None))
                    else:
                        daily_events.append(RecordCrm(
                            date_time=self.date,
                            crm_id=None,
                            user_id=current_id,
                            session=current_session,
                            mapped_event='pass',
                            utm_source=None,
                            utm_campaign=None))
                    if _current_price != 0.:
                        daily_events.append(RecordCrm(
                            date_time=self.date,
                            crm_id=None,
                            user_id=current_id,
                            session=current_session,
                            mapped_event='payment',
                            utm_source=None,
                            utm_campaign=None,
                            profit=_current_price))
            elif i is Rec.ADDTOCART:
                pass
                # current_id = next(pseudo_id)
                # current_session = next(pseudo_session)
                # daily_events.append(RecordCrm(
                #     date_time=self.date,
                #     crm_id=None,
                #     user_id=current_id,
                #     session=current_session,
                #     mapped_event='session_start',
                #     utm_source=None,
                #     utm_campaign=None))
                # for event_ in EVENT_LIST:
                #     daily_events.append(self._get_dummy_event(self.date, event_, current_id, current_session))
                # daily_events.append(RecordCrm(
                #     date_time=self.date,
                #     crm_id=None,
                #     user_id=current_id,
                #     session=current_session,
                #     mapped_event='AddTo_Cart',
                #     utm_source=None,
                #     utm_campaign=None))
            elif i is Rec.MINOR:
                current_id = next(pseudo_id)
                current_session = next(pseudo_session)
                daily_events.append(RecordCrm(
                    date_time=self.date,
                    crm_id=None,
                    user_id=current_id,
                    session=current_session,
                    mapped_event='session_start',
                    utm_source=None,
                    utm_campaign=None))
                for event_ in EVENT_LIST:
                    daily_events.append(self._get_dummy_event(self.date, event_, current_id, current_session))
            elif i is Rec.REGISTER:
                current_id = next(pseudo_id)
                current_session = next(pseudo_session)
                daily_events.append(RecordCrm(
                    date_time=self.date,
                    crm_id=None,
                    user_id=current_id,
                    session=current_session,
                    mapped_event='session_start',
                    utm_source=None,
                    utm_campaign=None))
                for event_ in EVENT_LIST:
                    daily_events.append(self._get_dummy_event(self.date, event_, current_id, current_session))
                daily_events.append(RecordCrm(
                    date_time=self.date,
                    crm_id=None,
                    user_id=current_id,
                    session=current_session,
                    mapped_event='registration',
                    utm_source=None,
                    utm_campaign=None))
            else:
                raise AssertionError
        return daily_events


class CrmReport(BaseTime):
    """CRM report"""

    def __init__(self, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date],
                 config: Iterable[AdvContextCRM]):
        super().__init__(start_date=start_date, end_date=end_date)
        self.config = config  # Количество переходов = количество кликов в рекламной компании
        self.allocation = None
        self.records = self.create_records()

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
        a = [i for i in range(len(prepare_profit)) if prepare_profit[i] != 0]
        l_a = len(a)
        separator = random.randint(1, math.floor(l_a/2))
        for source, purpose in zip(a[separator:], a[:separator]):
            prepare_profit[purpose] = prepare_profit[source]+prepare_profit[purpose]
            prepare_profit[source] = 0
        return prepare_profit

    def get_an_idea(self):
        res = dict()
        for i in self.records:
            if len(res) == 0:
                res[i.date_time] = (0 if i.utm_source is None else 1,
                                    1 if i.mapped_event == 'AddTo_Cart' else 0,
                                    1 if i.mapped_event == 'pass' else 0,
                                    1 if i.mapped_event == 'payment' else 0,
                                    i.profit if i.profit is not None else 0)
            else:
                res.update({i.date_time: prepare(
                    res.get(i.date_time, (0, 0, 0, 0, 0)),
                    0 if i.utm_source is None else 1,
                    1 if i.mapped_event == 'AddTo_Cart' else 0,
                    1 if i.mapped_event == 'pass' else 0,
                    1 if i.mapped_event == 'payment' else 0,
                    i.profit if i.profit is not None else 0
                )})
        return res

    @property
    def _split_by_company(self) -> Dict[AdvContextCRM, Tuple[List[float], List[int]]]:
        final_split = dict()
        for i in self.config:
            clicks_allocation = [i for i in get_random_ints_with_given_sum(self.number_days, i.clicks)]
            profit_allocation = self._prepare_zero_click(clicks_allocation, i.profit)
            final_split[i] = profit_allocation, clicks_allocation
        aa = dict()
        for i in final_split:
            aa[(i.source, i.campaign)] = final_split[i][-1]
        self.allocation = aa
        return final_split

    @staticmethod
    def _slice_by_day(index, data) -> Dict[AdvContextCRM, Tuple[float, int]]:
        slice_ = dict()
        for k in data:
            slice_[k] = data[k][0][index], data[k][1][index]
        return slice_

    @property
    def as_dict(self):
        date_time = []
        crm_id = []
        user_id = []
        session = []
        mapped_event = []
        utm_source = []
        utm_campaign = []
        profit = []
        for i in self.records:
            date_time.append(i.date_time)
            crm_id.append(i.crm_id)
            user_id.append(i.user_id)
            session.append(i.session)
            mapped_event.append(i.mapped_event)
            utm_source.append(i.utm_source)
            utm_campaign.append(i.utm_campaign)
            profit.append(i.profit)
        return {
            'date_time': date_time,
            'crm_id': crm_id,
            'user_id': user_id,
            'session': session,
            'mapped_event': mapped_event,
            'utm_source': utm_source,
            'utm_campaign': utm_campaign,
            'profit': profit}

    def create_records(self) -> Tuple[RecordCrm]:
        data = self._split_by_company
        all_record = []
        pseudo_id = pseudo_data(0)
        pseudo_session = pseudo_data(100)
        for i, days in enumerate(self.daterange):
            days_entries = Event(days, self._slice_by_day(i, data))
            all_record.extend(days_entries.get_day_entry(pseudo_id, pseudo_session))
        return tuple(all_record)
