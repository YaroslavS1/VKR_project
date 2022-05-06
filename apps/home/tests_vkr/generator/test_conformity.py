import pytest
import allure
from VKR_project.apps.home.tests_vkr.tools.ADV import AdvCampaign
from VKR_project.apps.home.tests_vkr.tools.CRM import CrmReport
from VKR_project.apps.home.tests_vkr.tools.CRM import AdvContextCRM


@allure.feature('CRM_ADV')
@allure.story('Test compliance of the report and the advertising company')
@pytest.mark.parametrize('end_date', ['30.12.2010', '30.11.2010'])
@pytest.mark.parametrize('start_date', ['25.10.2010', '30.10.2010'])
@pytest.mark.parametrize('profit', [999.99, 7777, 2, 1.5, 44.78])
@pytest.mark.parametrize('clicks', [9999, 8998, 1400, 5432, 400])
@pytest.mark.parametrize('name', ['Test campain'])
@pytest.mark.parametrize('source', ['yandex'])
def test_conformity(start_date, end_date, name, source, clicks, profit):
    crm_report = CrmReport(
        start_date=start_date,
        end_date=end_date,
        config=(AdvContextCRM(source, name, profit, clicks), ))
    adv_ = AdvCampaign(
        name=name,
        start_date=start_date,
        end_date=end_date,
        sum_cost=profit,
        source=source,
        allocation=crm_report.allocation[(source, name)])

    crm = crm_report.get_an_idea()
    adv = adv_.campaign
    sum_cost = 0
    sum_profit = 0
    for c, a in zip(crm, adv):
        assert crm[c][0] == a.clicks
        if a.clicks == 0:
            assert crm[c][4] == 0
        sum_cost += a.cost
        sum_profit += crm[c][4]

    assert sum_cost - sum_profit < 1e-8
    assert sum_cost - profit < 1e-8

