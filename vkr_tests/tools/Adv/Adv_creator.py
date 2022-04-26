import datetime
"""
Средняя сумма, которую вы платите за клик по вашему объявлению.
Средняя цена за клик (средняя цена за клик) рассчитывается путем деления общей стоимости ваших кликов на общее количество кликов.
"""


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


class AvgCampaign:
    def __init__(self, name: str, sum_cost: int, period:):
        self.name = name
        self.sum_cost = sum_cost
        self.period = period
        # проанализировать какие KPI какие параметры используют
        self.campaign = self.create_campaign(name, sum_cost, period)

    def create_campaign(self, name, sum_cost):
        """campaign creation method"""
        # запустить цикл по дням из периода создавая записи о реклама