import pytest
import allure
from ..tools.base import get_random_ints_with_given_sum


@allure.feature('Basic functionality')
@allure.story('Test function for getting an iterable object of random int with a given sum')
@pytest.mark.parametrize('n', [40, 30, 20, 10, 11, 49, 780])
@pytest.mark.parametrize('total', [10000, 10, 1, 10000000000])
def test_random_ints(n: int, total: int):
    int_iter = get_random_ints_with_given_sum(n, total)
    int_list = [i for i in int_iter]
    assert all([isinstance(i, int) for i in int_iter])
    assert len(int_list) == n
    assert sum(int_list) == total
