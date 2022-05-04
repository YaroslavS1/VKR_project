import random
from typing import Iterator
from numpy.random import multinomial

__all__ = [
    'get_random_floats_with_given_sum',
    'get_random_ints_with_given_sum'
]


def get_random_floats_with_given_sum(n: int, total: float) -> Iterator[float]:
    values = [0.0] + [round(random.triangular(0, total), 2) for i in range(n - 1)] + [total]
    values.sort()
    return iter([round(values[i + 1] - values[i], 2) for i in range(len(values) - 1)])


def get_random_ints_with_given_sum(n: int, total: int) -> Iterator[int]:
    return iter(list(multinomial(total, [1/n] * n)))
