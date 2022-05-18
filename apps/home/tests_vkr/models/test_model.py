import random

import pytest
import time


@pytest.mark.parametrize('n_compaign', [40, 30, 20, 10, 11, 49])
def test_model(n_compaign):
    time.sleep(random.randint(1, 10))
    pass
