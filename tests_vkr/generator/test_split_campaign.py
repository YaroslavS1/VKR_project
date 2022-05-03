import allure
import pytest

from ..tools.CRM import AdvContextCRM
from ..tools.CRM import CrmReport


@allure.feature('CRM report')
@allure.story('Test of creating CRM report')
@pytest.mark.parametrize(
    'end_date', [
        # '10.10.2010',
        # '25.11.2010',
        '01.01.2022'
    ])
@pytest.mark.parametrize(
    'start_date', [
        # '01.10.2010',
        # '25.05.2010',
        '01.01.2000',
    ])
@pytest.mark.parametrize('profit1', [9873])
@pytest.mark.parametrize('profit2', [8764])
@pytest.mark.parametrize('clicks1', [8000])
@pytest.mark.parametrize('clicks2', [8000])
def test_split_campaign_crm(start_date, end_date, profit1, profit2, clicks1, clicks2):
    'сделать более гибкое количество рекламных компаний'
    camaign_1 = AdvContextCRM('yandex', 'test_campaign1', profit1, clicks1)
    camaign_2 = AdvContextCRM('yandex', 'test_campaign2', profit2, clicks2)
    # camaign_3 = AdvContextCRM('yandex', 'test_campaign3', profit1, clicks1)
    # camaign_4 = AdvContextCRM('yandex', 'test_campaign4', profit2, clicks2)

    report_ = CrmReport(
        start_date=start_date,
        end_date=end_date,
        config=(camaign_1, camaign_2))
    result = report_._split_by_company

    assert sum(report_.allocation[(camaign_1.source, camaign_1.campaign)]) == camaign_1.clicks
    assert sum(report_.allocation[(camaign_2.source, camaign_2.campaign)]) == camaign_2.clicks

    summary_profit = 0
    summary_clicks = 0
    for i in result:
        summary_profit += sum(result[i][0])
        summary_clicks += sum(result[i][1])
    assert abs(summary_profit - (profit1 + profit2)) < 1e-4
    assert summary_clicks == (clicks1 + clicks2)
