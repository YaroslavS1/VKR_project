import pytest


class Static_DataFrame:
    def __init__(self, value):
        self.value = value


@pytest.mark.parametrize('test_case', [Static_DataFrame(10), Static_DataFrame(20), Static_DataFrame(30), Static_DataFrame(40)])
def test_atach(test_case):
    if test_case.value < 29:
        pass
    else:
        raise ValueError
