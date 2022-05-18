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
@pytest.mark.parametrize('end_date', ['30.10.2021'])
@pytest.mark.parametrize('start_date', ['25.05.2020'])
@pytest.mark.parametrize('profit1', [(1876, 5000)])
@pytest.mark.parametrize('clicks1', [200])
@pytest.mark.parametrize('profit2', [(5678, 9090)])
@pytest.mark.parametrize('clicks2', [450])
@pytest.mark.parametrize('profit3', [(10876, 90000)])
@pytest.mark.parametrize('clicks3', [6000])
@pytest.mark.parametrize('profit4', [(1800, 1800)])
@pytest.mark.parametrize('clicks4', [900])
@pytest.mark.parametrize('profit5', [(98760, 5000)])
@pytest.mark.parametrize('clicks5', [700])
@pytest.mark.parametrize('profit6', [(56798, 78000)])
@pytest.mark.parametrize('clicks6', [450])
@pytest.mark.parametrize('name1', ['yandex_direct1'])
@pytest.mark.parametrize('source1', ['yandex'])
@pytest.mark.parametrize('name2', ['yandex_direct2'])
@pytest.mark.parametrize('source2', ['yandex'])
@pytest.mark.parametrize('name3', ['vk_1'])
@pytest.mark.parametrize('source3', ['vk'])
@pytest.mark.parametrize('name4', ['vk_2'])
@pytest.mark.parametrize('source4', ['vk'])
@pytest.mark.parametrize('name5', ['avito_1'])
@pytest.mark.parametrize('source5', ['avito'])
@pytest.mark.parametrize('name6', ['rambler_1'])
@pytest.mark.parametrize('source6', ['rambler'])
def test_conformity_many(start_date, end_date,
                         source1, name1, profit1, clicks1,
                         source2, name2, profit2, clicks2,
                         source3, name3, profit3, clicks3,
                         source4, name4, profit4, clicks4,
                         source5, name5, profit5, clicks5,
                         source6, name6, profit6, clicks6,
                         ):
    pytest.skip(f'Not suitable for CI')
    adv_list = (
        AdvContextCRM(source1, name1, profit1[1], clicks1),
        AdvContextCRM(source2, name2, profit2[1], clicks2),
        AdvContextCRM(source3, name3, profit3[1], clicks3),
        AdvContextCRM(source4, name4, profit4[1], clicks4),
        AdvContextCRM(source5, name5, profit5[1], clicks5),
        AdvContextCRM(source6, name6, profit6[1], clicks6)
    )
    crm_report = CrmReport(
        start_date=start_date,
        end_date=end_date,
        config=adv_list)

    adv_1 = AdvCampaign(
        name=name1,
        start_date=start_date,
        end_date=end_date,
        sum_cost=profit1[0],
        source=source1,
        allocation=crm_report.allocation[(source1, name1)])
    adv_2 = AdvCampaign(
        name=name2,
        start_date=start_date,
        end_date=end_date,
        sum_cost=profit2[0],
        source=source2,
        allocation=crm_report.allocation[(source2, name2)])
    adv_3 = AdvCampaign(
        name=name3,
        start_date=start_date,
        end_date=end_date,
        sum_cost=profit3[0],
        source=source3,
        allocation=crm_report.allocation[(source3, name3)])
    adv_4 = AdvCampaign(
        name=name4,
        start_date=start_date,
        end_date=end_date,
        sum_cost=profit4[0],
        source=source4,
        allocation=crm_report.allocation[(source4, name4)])
    adv_5 = AdvCampaign(
        name=name5,
        start_date=start_date,
        end_date=end_date,
        sum_cost=profit5[0],
        source=source5,
        allocation=crm_report.allocation[(source5, name5)])
    adv_6 = AdvCampaign(
        name=name6,
        start_date=start_date,
        end_date=end_date,
        sum_cost=profit6[0],
        source=source6,
        allocation=crm_report.allocation[(source6, name6)])

    data_frame = pd.DataFrame(crm_report.as_dict)
    data_frame.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMO.csv')

    data_frame_1 = pd.DataFrame(adv_1.as_dict)
    data_frame_1.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_1.csv')

    data_frame_2 = pd.DataFrame(adv_2.as_dict)
    data_frame_2.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_2.csv')

    data_frame_3 = pd.DataFrame(adv_3.as_dict)
    data_frame_3.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_3.csv')

    data_frame_4 = pd.DataFrame(adv_4.as_dict)
    data_frame_4.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_4.csv')

    data_frame_5 = pd.DataFrame(adv_5.as_dict)
    data_frame_5.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_5.csv')

    data_frame_6 = pd.DataFrame(adv_6.as_dict)
    data_frame_6.to_csv('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_6.csv')
