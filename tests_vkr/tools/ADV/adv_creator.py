import datetime
import random
from typing import Union, Tuple

from VKR_project.tests_vkr.tools import BaseTime

"""
Средняя сумма, которую вы платите за клик по вашему объявлению.
Средняя цена за клик (средняя цена за клик) рассчитывается путем деления общей стоимости ваших кликов на общее количество кликов.
"""
__all__ = [
    'AvgCampaign'
]


class Record:
    def __init__(self,
                 date: datetime.date,
                 name: str,
                 # avg_click_position: float,
                 impressions: int,
                 clicks: int,
                 cost: int,
                 # placement: str
                 ):
        self.date = date
        self.name = name
        # self.avg_click_position = avg_click_position
        self.impressions = impressions
        self.clicks = clicks

        self.ctr = impressions/clicks
        '''Эталонное значение как правило на ~3 больше'''

        self.cost = cost

        self.avg_cpc = cost/clicks
        '''в среднем на 0.5 больше '''

        # self.avg_pageviews = object()
        # self.placement = placement

    def __repr__(self) -> str:
        return f'date: {self.date}, ' \
               f'name: {self.name}, ' \
               f'cost: {self.cost}, ' \
               f'impressions: {self.impressions},   ' \
               f'clicks: {self.clicks}'


class AvgCampaign(BaseTime):
    def __init__(self, name: str, sum_cost: int, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date]):
        super().__init__(start_date=start_date, end_date=end_date)
        self.name = name
        self.sum_cost = sum_cost
        # impressions количество показов
        # проанализировать какие KPI какие параметры используют
        self.campaign = self.create_campaign()

    @staticmethod
    def constrained_sum_sample_pos(n, total):
        """Return a randomly chosen list of n positive integers summing to total.
        Each such list is equally likely to occur."""
        arr = []
        for i in range(n):
            if i == n - 1:
                arr.append(total - sum(arr))
            else:
                arr.append(random.randint(0, total - sum(arr)))
        assert total == sum(arr)
        return iter(arr)

    def create_campaign(self) -> Tuple[Record]:
        """campaign creation method"""
        campaign = list()
        number_days = int((self.end_date - self.start_date).days)+1
        cost_allocation = self.constrained_sum_sample_pos(number_days, self.sum_cost)
        for date in self.daterange:
            campaign.append(
                Record(
                    date=date,
                    name=self.name,
                    impressions=random.randint(10, 1000),
                    clicks=random.randint(10, 1000),
                    cost=next(cost_allocation)
                )
            )
        return tuple(campaign)
