import pytest

from VKR_project.tests_vkr.tools.ADV import AvgCampaign


@pytest.mark.parametrize(
    'start_date',
    [
        '24.05.2010',
        '25.05.2010',
        '01.01.2000'
    ]
)
@pytest.mark.parametrize(
    'end_date',
    [
        '24.10.2010',
        '25.11.2010',
        '01.01.2022'
    ]
)
@pytest.mark.parametrize('sum_cost', [1000, 1200, 3000, 5000, 10000, 1, 0, 10000000000])
def test_create_adv_compaign(start_date, end_date, sum_cost):
    a = AvgCampaign(
        name='Test campain',
        start_date=start_date,
        end_date=end_date,
        sum_cost=sum_cost
    )
    e = 0
    for i in a.campaign:
        e = e + i.cost
    assert e == sum_cost
