import time
import random

import allure
import pytest


@allure.step('API Direct test')
@pytest.mark.parametrize('step', ['general request', 'query by day', ''])
def test_api_direct(step):
    time.sleep(random.randint(1, 5))
    assert step in ['general request', 'query by day', '']
