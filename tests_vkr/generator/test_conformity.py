import pytest
import allure
from VKR_project.tests_vkr.tools.ADV import AdvCampaign
from VKR_project.tests_vkr.tools.CRM import CrmReport
from VKR_project.tests_vkr.tools.CRM import AdvContextCRM


@allure.feature('CRM_ADV')
@allure.story('Test compliance of the report and the advertising company')
@pytest.mark.parametrize('end_date', ['30.10.2010'])
@pytest.mark.parametrize('start_date', ['25.10.2010'])
@pytest.mark.parametrize('sum_cost', [8000])
@pytest.mark.parametrize('clicks', [1000])
@pytest.mark.parametrize('name', ['Test campain'])
@pytest.mark.parametrize('source', ['yandex'])
def test_conformity(start_date, end_date, sum_cost, name, source, clicks):
    report_ = CrmReport(
        start_date=start_date,
        end_date=end_date,
        config=(AdvContextCRM(source, name, clicks, sum_cost), ))
    a = AdvCampaign(
        name=name,
        start_date=start_date,
        end_date=end_date,
        sum_cost=sum_cost,
        source=source,
        allocation=report_.allocation[(source, name)])

    aa = report_.get_an_idea()
    bb = a.campaign
    for i, j in zip(aa, bb):
        print(i, aa[i][0], j.clicks)
