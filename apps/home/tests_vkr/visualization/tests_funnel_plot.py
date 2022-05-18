import random
import tempfile

import allure
import pandas as pd
import plotly.express as px
import pytest

from ..tools.ADV import AdvCampaign


def count_adv(adv: AdvCampaign):
    cost_campaign = 0
    impressions = 0
    clicks = 0
    name_campaign = adv.campaign[0].name
    for i in adv.campaign:
        assert i.name == name_campaign
        cost_campaign += i.cost
        impressions += i.impressions
        clicks += i.clicks
    return {(adv.source, name_campaign): (impressions, clicks, cost_campaign)}


@allure.feature('ADV campaign')
@allure.story('Test of creating an advertising company with a given price')
@pytest.mark.parametrize(
    'end_date', [
        '24.10.2010',
        # '25.11.2010',
        # '01.01.2022'
    ])
@pytest.mark.parametrize(
    'start_date', [
        '24.05.2010',
        # '25.05.2010',
        # '01.01.2000',
    ])
@pytest.mark.parametrize('n_compaign', [3])
def test_tests_funnel(start_date, end_date, n_compaign):
    # TODO: тест не полный и довольно тревиальный, нужно дополнить
    adv_campaigns = list()
    sum_cost = [random.randint(10000, 90000) for _ in range(n_compaign)]
    profit = [random.randint(10000, 1000000) for _ in range(n_compaign)]
    visits = [random.randint(1000, 2000) for _ in range(n_compaign)]
    purchases = [random.randint(1000, 1500) for _ in range(n_compaign)]
    for i in range(n_compaign):
        adv_campaigns.append(
            AdvCampaign(
                name=f'Test_campain{i}',
                start_date=start_date,
                end_date=end_date,
                sum_cost=sum_cost[i]))

    crm = {('yandex', f'Test_campain{i}'): (profit[i], visits[i], purchases[i]) for i in range(n_compaign)}

    stages = ["Количество показов рекламы", "Клики по рекламным обьявлениям", "Покупки"]
    df_s = []
    for i, i_c, adv in zip(range(n_compaign), crm, adv_campaigns):
        concurrent_adv = count_adv(adv)
        df_ = pd.DataFrame(dict(количество=[concurrent_adv[i_c][2], concurrent_adv[i_c][2],
                                        # concurrent_adv[i_c][2],
                                        crm[i_c][2]], стадии=stages))
        # print(i_c)
        df_['Рекламная кампания'] = i_c[0] + i_c[1]
        # df_toronto = pd.DataFrame(dict(number=[52, 36, 18, 14, 5], stage=stages))
        # df_toronto['office'] = 'Toronto'
        df_s.append(df_)
    df = pd.concat(df_s, axis=0)
    fig = px.funnel(df, x='количество', y='стадии', color='Рекламная кампания',)
    fig.show()

    temp = tempfile.NamedTemporaryFile()
    fig.write_html(f'{temp.name}')
    allure.attach.file(f'{temp.name}', attachment_type=allure.attachment_type.HTML)

    # for i, i_c, adv in zip(range(n_compaign), crm, adv_campaigns):
    #     concurrent_adv = count_adv(adv)
    #
    #     assert round(concurrent_adv[i_c][0]) == round(sum_cost[i])
    #     assert ((crm[i_c]-concurrent_adv[i_c][0])/concurrent_adv[i_c][0])*100 == ((profit[i] - sum_cost[i])/sum_cost[i])*100
