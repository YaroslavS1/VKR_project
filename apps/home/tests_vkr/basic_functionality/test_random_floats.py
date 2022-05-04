import pytest
import allure

from VKR_project.apps.home.tests_vkr.tools.base import get_random_floats_with_given_sum


@allure.feature('Basic functionality')
@allure.story('Test function for getting an iterable object of random float with a given sum')
@pytest.mark.parametrize('n', [40, 30, 20, 10, 11, 49, 1000, 1010])
@pytest.mark.parametrize('total', [10000, 10, 12.23, 90.90, 0, 0.1, 100000000])
def test_random_floats(n: int, total: float):
    float_iter = get_random_floats_with_given_sum(n, total)
    float_list = [i for i in float_iter]
    assert all([isinstance(i, float) for i in float_iter])
    assert len(float_list) == n
    assert round(sum(float_list), 2) == round(total, 2)
