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
@pytest.mark.parametrize('end_date', ['30.10.2020'])
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
    res = CRMRepr.slice_by_day(pd.DataFrame(crm_report.as_dict))
    # print(res)
