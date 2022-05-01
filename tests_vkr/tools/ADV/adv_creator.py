import datetime
import random
from typing import Union
from typing import Tuple

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
                 # placement: str
                 ):
        self.date = date
        self.name = name
        # self.avg_click_position = avg_click_position
        self.impressions = impressions
        self.clicks = clicks

        self.ctr = impressions / clicks
        '''Эталонное значение как правило на ~3 больше'''

        self.cost = cost

        self.avg_cpc = cost / clicks
        '''в среднем на 0.5 больше '''

        # self.avg_pageviews = object()
        # self.placement = placement

    def __repr__(self) -> str:
        return f'date: {self.date}, ' \
               f'name: {self.name}, ' \
               f'cost: {self.cost}, ' \
               f'impressions: {self.impressions},   ' \
               f'clicks: {self.clicks}'


class AdvCampaign(BaseTime):
    def __init__(self, name: str, sum_cost: int, start_date: Union[str, datetime.date],
                 end_date: Union[str, datetime.date]):
        super().__init__(start_date=start_date, end_date=end_date)
        self.name = name
        assert sum_cost > 0
        self.sum_cost = sum_cost
        # impressions количество показов
        # проанализировать какие KPI какие параметры используют
        self.campaign = self.create_campaign()
        self.type_adv = 'yandex'

    def create_campaign(self) -> Tuple[RecordAdv]:
        """campaign creation method"""
        campaign = list()
        number_days = int((self.end_date - self.start_date).days) + 1
        cost_allocation = get_random_floats_with_given_sum(number_days, self.sum_cost)
        for date in self.daterange:
            campaign.append(
                RecordAdv(
                    date=date,
                    name=self.name,
                    impressions=random.randint(100, 1000),
                    clicks=random.randint(100, 200),
                    cost=next(cost_allocation)
                )
            )
        return tuple(campaign)
