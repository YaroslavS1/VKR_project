import numpy as np

__all__ = [
    'get_utm',
    'get_number',
    'get_addto_cart',
    'get_visit',
    'get_pass',
    'get_payment'
]


def is_nan(i):
    try:
        return np.isnan(i)
    except TypeError:
        return not isinstance(i, str)


def get_utm(s):
    k = [i for i in s.unique() if not is_nan(i)]
    return k[0] if len(k) > 0 else None


def get_number(s):
    return s.sum()


def get_addto_cart(s):
    try:
        return s.value_counts()['AddTo_Cart']
    except KeyError:
        return 0


def get_registration(s):
    try:
        return s.value_counts()['registration']
    except KeyError:
        return 0


def get_visit(s):
    try:
        return sum(s.value_counts())
    except KeyError:
        return 0


def get_pass(s):
    try:
        return s.value_counts()['pass']
    except KeyError:
        return 0


def get_payment(s):
    try:
        return s.value_counts()['payment']
    except KeyError:
        return 0
