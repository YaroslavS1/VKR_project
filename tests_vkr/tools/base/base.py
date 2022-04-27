import datetime
from typing import Union

__all__ = [
    'BaseTime'
]


class BaseTime:
    def __init__(self, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date]) -> None:
        self.start_date = self._sanitize_date(start_date)
        self.end_date = self._sanitize_date(end_date)

    @staticmethod
    def _sanitize_date(date: Union[str, datetime.date]) -> datetime.date:
        if isinstance(date, str):
            return datetime.datetime.strptime(date, "%d.%m.%Y").date()
        elif isinstance(date, datetime.date):
            return date
        else:
            raise AssertionError

    @property
    def daterange(self):
        for n in range(int((self.end_date - self.start_date).days)+1):
            yield self.start_date + datetime.timedelta(n)
