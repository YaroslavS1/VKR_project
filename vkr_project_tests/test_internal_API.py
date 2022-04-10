import random
import time

import pytest


@pytest.mark.parametrize('identifier', ['1', '2', '3', '4', '5', '6', '7', '8'])
def test_api_direct(identifier):
    time.sleep(random.randint(1, 5))
    assert identifier in ['1', '2', '3', '4', '5', '6', '7', '8']