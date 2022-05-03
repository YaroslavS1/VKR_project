__all__ = [
    'pseudo_data'
]


def pseudo_data(point):
    i = point
    while True:
        i += 1
        yield i
