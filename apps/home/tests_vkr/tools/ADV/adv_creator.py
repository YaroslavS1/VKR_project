import datetime
import random
from typing import Tuple
from typing import Union, Optional

from ..base import BaseTime
from ..base import get_random_floats_with_given_sum

__all__ = [
    'AdvCampaign'
]


class RecordAdv:
    def __init__(self,
                 date: datetime.date,
                 name: str,
                 # avg_click_position: float,
                 impressions: int,
                 clicks: int,
                 cost: float,
                 source: str
                 ):
        self.date = date
        self.name = name
        # self.avg_click_position = avg_click_position
        self.impressions = impressions
        self.clicks = clicks

        self.ctr = round(impressions / clicks, 2)
        '''Эталонное значение как правило на ~3 больше'''

        self.cost = cost

        self.avg_cpc = round(cost / clicks, 2)
        '''в среднем на 0.5 больше '''

        self.avg_pageviews = object()
        self.source = source

    def __repr__(self) -> str:
        return f'date: {self.date}, ' \
               f'name: {self.name}, ' \
               f'cost: {self.cost}, ' \
               f'impressions: {self.impressions},   ' \
               f'clicks: {self.clicks}'


class AdvCampaign(BaseTime):
    def __init__(self, name: str, sum_cost: int, start_date: Union[str, datetime.date],
                 end_date: Union[str, datetime.date], allocation: Optional[Tuple[int]] = None, source='yandex'):
        super().__init__(start_date=start_date, end_date=end_date)
        self.name = name
        assert sum_cost > 0
        self.sum_cost = sum_cost
        # impressions количество показов
        # проанализировать какие KPI какие параметры используют
        self.allocation = allocation
        self.source = source
        self.campaign = self.create_campaign()

    @property
    def as_dict(self):
        date = []
        name = []
        impressions = []
        clicks = []
        ctr = []
        cost = []
        avg_cpc = []
        source = []
        for i in self.campaign:
            date.append(i.date)
            name.append(i.name)
            impressions.append(i.impressions)
            clicks.append(i.clicks)
            ctr.append(i.ctr)
            cost.append(i.cost)
            avg_cpc.append(i.avg_cpc)
            source.append(i.source)
        return {
            'date': date,
            'source': source,
            'name': name,
            'impressions': impressions,
            'clicks': clicks,
            'ctr': ctr,
            'cost': cost,
            'avg_cpc': avg_cpc,
        }

    def create_campaign(self) -> Tuple[RecordAdv]:
        """campaign creation method"""
        campaign = list()
        number_days = int((self.end_date - self.start_date).days) + 1

        cost_allocation = get_random_floats_with_given_sum(
            number_days if self.allocation is None else len([i for i in self.allocation if i != 0]), self.sum_cost)

        if self.allocation is not None:
            al_it = iter(self.allocation)
            for date in self.daterange:
                cur_al_it = next(al_it)
                campaign.append(
                    RecordAdv(
                        date=date,
                        name=self.name,
                        source=self.source,
                        impressions=random.randint(cur_al_it, cur_al_it*random.randint(2, 5)),
                        clicks=cur_al_it,
                        cost=0 if cur_al_it == 0 else next(cost_allocation)))
        else:
            for date in self.daterange:
                campaign.append(
                    RecordAdv(
                        date=date,
                        name=self.name,
                        source=self.source,
                        impressions=random.randint(100, 1000),
                        clicks=random.randint(100, 200),
                        cost=next(cost_allocation)))

        return tuple(campaign)
