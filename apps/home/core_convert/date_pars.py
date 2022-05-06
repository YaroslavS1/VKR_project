from datetime import datetime
__all__ = [
    'dateparse'
]

dateparse = lambda dates: [datetime.strptime(d, '%Y-%m-%d').date() for d in dates]
