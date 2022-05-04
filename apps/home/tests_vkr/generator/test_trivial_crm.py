import random

import allure
import pytest

from ..tools.ADV import AdvCampaign


def count_adv(adv: AdvCampaign):
    cost_campaign = 0
    name_campaign = adv.campaign[0].name
    for i in adv.campaign:
        assert i.name == name_campaign
        cost_campaign += i.cost
    return {(adv.source, name_campaign): cost_campaign}


@allure.feature('ADV campaign')
@allure.story('Test of creating an advertising company with a given price')
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
@pytest.mark.parametrize('n_compaign', [40, 30, 20, 10, 11, 49])
def test_trivial_crm(start_date, end_date, n_compaign):
    # TODO: тест не полный и довольно тревиальный, нужно дополнить
    adv_campaigns = list()
    sum_cost = [random.randint(10000, 90000) for _ in range(n_compaign)]
    profit = [random.randint(10000, 1000000) for _ in range(n_compaign)]
    for i in range(n_compaign):
        adv_campaigns.append(
            AdvCampaign(
                name=f'Test_campain{i}',
                start_date=start_date,
                end_date=end_date,
                sum_cost=sum_cost[i]))

    crm = {('yandex', f'Test_campain{i}'): profit[i] for i in range(n_compaign)}

    for i, i_c, adv in zip(range(n_compaign), crm, adv_campaigns):
        concurrent_adv = count_adv(adv)
        assert round(concurrent_adv[i_c]) == round(sum_cost[i])
        assert round(((crm[i_c] - count_adv(adv)[i_c]) / concurrent_adv[i_c]) * 100) == round(
            ((profit[i] - sum_cost[i]) / sum_cost[i]) * 100)
