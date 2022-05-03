import random

import allure
import pytest
import pandas as pd

from ..tools.CRM import AdvContextCRM
from ..tools.CRM import CrmReport


@allure.feature('CRM report')
@allure.story('Test of creating CRM report')
@pytest.mark.parametrize(
    'end_date', [
        '10.10.2010',
        # '25.11.2010',
        # '01.01.2022'
    ])
@pytest.mark.parametrize(
    'start_date', [
        '05.10.2010',
        # '25.05.2010',
        # '01.01.2000',
    ])
@pytest.mark.parametrize('profit1, profit2, click1, click2', [(100, 100, 500, 600)])
def test_dump_crm(start_date, end_date, profit1, profit2, click1, click2):

    cam1 = AdvContextCRM('yandex', f'test_campaign1', profit1, click1)
    cam2 = AdvContextCRM('yandex', f'test_campaign2', profit2, click2)

    report_ = CrmReport(
        start_date=start_date,
        end_date=end_date,
        config=(cam1, cam2))

    assert sum([i.profit for i in report_.records if isinstance(i.profit, float)]) - (profit1+profit2) < 1e-5
    # for i, click, profit in zip(range(n), clicks, profits):
    #     assert sum([1 for j in report_.records if j.utm_campaign == f'test_campaign{i}']) == click

    date_time = []
    crm_id = []
    user_id = []
    session = []
    mapped_event = []
    utm_source = []
    utm_campaign = []
    profit = []
    for i in report_.records:
        date_time.append(i.date_time)
        crm_id.append(i.crm_id)
        user_id.append(i.user_id)
        session.append(i.session)
        mapped_event.append(i.mapped_event)
        utm_source.append(i.utm_source)
        utm_campaign.append(i.utm_campaign)
        profit.append(i.profit)
    domain_dict = {
        'date_time': date_time,
        'crm_id': crm_id,
        'user_id': user_id,
        'session': session,
        'mapped_event': mapped_event,
        'utm_source': utm_source,
        'utm_campaign': utm_campaign,
        'profit': profit}

    # data_frame = pd.DataFrame(domain_dict)
    # data_frame.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMO.csv')
