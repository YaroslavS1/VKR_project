import allure
import pytest

from ..tools.ADV import AdvCampaign


@allure.feature('CRM')
@allure.story('CRM report preprocessing test')
@pytest.mark.parametrize(
    'end_date', [
        '24.10.2010',
        '25.11.2010',
        '01.01.2022'
    ])
@pytest.mark.parametrize(
    'start_date', [
        '24.05.2010',
        '25.05.2010',
        '01.01.2000',
    ])
@pytest.mark.parametrize('sum_cost', [8000, 1200, 3000, 5000, 10000, 1, 10000000000, 123])
def test_slyce_by_day(start_date, end_date, sum_cost):
    a = AdvCampaign(
        name='Test campain',
        start_date=start_date,
        end_date=end_date,
        sum_cost=sum_cost
    )
    cost_campaign = 0
    for i in a.campaign:
        cost_campaign += i.cost
    assert abs(cost_campaign - sum_cost) < 1e-4
