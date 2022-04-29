import datetime
from typing import Union, Dict, Tuple

from VKR_project.tests_vkr.tools import BaseTime


class TrivialCrm(BaseTime):
    def __init__(self, sum_profit: int, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date]):
        super().__init__(start_date=start_date, end_date=end_date)
        self.sum_profit = sum_profit

        self.adv_company: Dict[Tuple[str, str], int]  # (utm_source, utm_campaign): profit
        # self.utm_medium
        self.campaign = self.create_campaign()