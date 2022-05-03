import allure
import pytest

from ...apps.home.core_convert import CRMRepr


@allure.feature('CRM report')
@allure.story('Test of creating CRM report')
@pytest.skip(f'Not suitable for CI')
def test_read_crm():
    read_ = CRMRepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMO.csv')
    a = read_._load_csv()
    summary_visit = []
    summary_addto_cart = []
    summary_pass = []
    summary_payment = []
    summary_profit = []

    for i in a:
        for j in a[i]:
            summary_visit.append(a[i][j][0])
            summary_addto_cart.append(a[i][j][1])
            summary_pass.append(a[i][j][2])
            summary_payment.append(a[i][j][3])
            summary_profit.append(a[i][j][4])
    # print(summary_profit)
    assert sum(summary_profit) == 200
    print('summary_profit', sum(summary_profit))
    print('summary_visit', sum(summary_visit))
    print('summary_addto_cart', sum(summary_addto_cart))
    print('summary_pass', sum(summary_pass))
    print('summary_payment', sum(summary_payment))
    print('summary_profit', sum(summary_profit))
