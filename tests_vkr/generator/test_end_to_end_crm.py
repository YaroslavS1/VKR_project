import tempfile
from typing import Tuple

import allure
import pandas as pd
import pytest

from ..tools.CRM import AdvContextCRM
from ..tools.CRM import CrmReport
from ...apps.home.core_convert import CRMRepr


@allure.feature('CRM report')
@allure.story('Test dump read CRM report')
@pytest.mark.parametrize(
    'end_date', [
        '06.10.2010',
        # '25.11.2010',
        # '01.01.2022'
    ])
@pytest.mark.parametrize(
    'start_date', [
        '05.10.2010',
        # '25.05.2010',
        # '01.01.2000',
    ])
@pytest.mark.parametrize('profit1, profit2, click1, click2, case1, case2', [
    (40000, 30000, 700, 600, ('yandex', 'test_campaign1'), ('yandex', 'test_campaign2'))])
@pytest.xfail(f'Not suitable for CI')
def test_end_to_end_crm(start_date, end_date, profit1: float, profit2: float, click1: int,
                        click2: int, case1: Tuple[str, str], case2: Tuple[str, str]) -> None:
    cam1 = AdvContextCRM(case1[0], case1[1], profit1, click1)
    cam2 = AdvContextCRM(case2[0], case2[1], profit2, click2)

    report_ = CrmReport(
        start_date=start_date,
        end_date=end_date,
        config=(cam1, cam2))

    assert sum([i.profit for i in report_.records if isinstance(i.profit, float)]) - (profit1 + profit2) < 1e-5

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

    data_frame = pd.DataFrame(domain_dict)
    data_frame.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMO.csv')

    read_ = CRMRepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMO.csv')
    a = read_._load_csv()
    summary_visit = {}
    summary_profit = {}
    for i in a:
        for j in a[i]:
            if len(summary_visit) == 0:
                summary_visit[j] = a[i][j][0]
            else:
                summary_visit.update({j: summary_visit.get(j, 0) + a[i][j][0]})
            if len(summary_profit) == 0:
                summary_profit[j] = a[i][j][4]
            else:
                summary_profit.update({j: summary_profit.get(j, 0) + a[i][j][4]})

    assert summary_visit[case1] == click1
    assert summary_visit[case2] == click2

    assert summary_profit[case1] - profit1 < 1e-8
    assert summary_profit[case2] - profit2 < 1e-8
    # assert sum(summary_profit) - (profit1 + profit2) <= 1e-5
