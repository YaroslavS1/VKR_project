import random

import allure
import pytest

from ..tools.CRM import AdvContextCRM
from ..tools.CRM import CrmReport


@allure.feature('CRM report')
@allure.story('Test of creating CRM report')
@pytest.mark.parametrize(
    'end_date', [
        '10.10.2010',
        '25.11.2010',
        '01.01.2022'
    ])
@pytest.mark.parametrize(
    'start_date', [
        '01.10.2010',
        '25.05.2010',
        '01.01.2000',
    ])
@pytest.mark.parametrize('n', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_dummy_campaign_crm(start_date, end_date, n):
    clicks = []
    profits = []
    camaign = []
    for i in range(n):
        click = random.randint(100, 10000)
        profit = random.randint(click, 10000)
        camaign.append(AdvContextCRM('yandex', f'test_campaign{i}', profit, click))
        clicks.append(click)
        profits.append(profit)

    report_ = CrmReport(
        start_date=start_date,
        end_date=end_date,
        config=camaign)

    assert sum([i.profit for i in report_.records if isinstance(i.profit, float)]) - sum(profits) < 1e-5
    for i, click, profit in zip(range(n), clicks, profits):
        assert sum([1 for j in report_.records if j.utm_campaign == f'test_campaign{i}']) == click

