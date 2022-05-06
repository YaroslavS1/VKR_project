import allure
import pandas as pd
import pytest

from VKR_project.apps.home.core_convert import CRMRepr
from VKR_project.apps.home.core_convert.adv import ADVrepr
from VKR_project.apps.home.tests_vkr.tools.ADV import AdvCampaign
from VKR_project.apps.home.tests_vkr.tools.CRM import AdvContextCRM
from VKR_project.apps.home.tests_vkr.tools.CRM import CrmReport


@allure.feature('CRM_ADV')
@allure.story('Test compliance of the report and the advertising company')
@pytest.mark.parametrize('end_date', ['30.11.2021'])
@pytest.mark.parametrize('start_date', ['25.10.2021'])
@pytest.mark.parametrize('profit1', [9876])
@pytest.mark.parametrize('clicks1', [200])
@pytest.mark.parametrize('profit2', [5678])
@pytest.mark.parametrize('clicks2', [450])
@pytest.mark.parametrize('name1', ['Test campain1'])
@pytest.mark.parametrize('source1', ['yandex'])
@pytest.mark.parametrize('name2', ['Test campain2'])
@pytest.mark.parametrize('source2', ['yandex'])
def test_conformity(start_date, end_date, name1, source1, name2, source2, clicks1, profit1, clicks2, profit2):
    crm_report = CrmReport(
        start_date=start_date,
        end_date=end_date,
        config=(AdvContextCRM(source1, name1, profit1+100, clicks1), AdvContextCRM(source2, name2, profit2+10000, clicks2)))
    adv_1 = AdvCampaign(
        name=name1,
        start_date=start_date,
        end_date=end_date,
        sum_cost=profit1,
        source=source1,
        allocation=crm_report.allocation[(source1, name1)])
    adv_2 = AdvCampaign(
        name=name2,
        start_date=start_date,
        end_date=end_date,
        sum_cost=profit2,
        source=source2,
        allocation=crm_report.allocation[(source2, name2)])

    data_frame = pd.DataFrame(crm_report.as_dict)
    data_frame.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMO.csv')

    data_frame_1 = pd.DataFrame(adv_1.as_dict)
    data_frame_1.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_1.csv')

    data_frame_2 = pd.DataFrame(adv_2.as_dict)
    data_frame_2.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_2.csv')

    # read_ = ADVrepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_1.csv')
    # a = read_.load_csv
    # print(a.info())
    # print(a)
    # print(read_.adv)
    # crm = crm_report.get_an_idea()
    # adv = adv_.campaign
    # sum_cost = 0
    # sum_profit = 0
    # for c, a in zip(crm, adv):
    #     assert crm[c][0] == a.clicks
    #     if a.clicks == 0:
    #         assert crm[c][4] == 0
    #     sum_cost += a.cost
    #     sum_profit += crm[c][4]
    #
    # assert round(sum_cost, 2) == round(sum_profit, 2)
    # assert sum_cost - profit < 1e-8

