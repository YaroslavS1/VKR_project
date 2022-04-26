
"""Стоит ли тут использовать датакласс? или лучше Pydantic"""
class Session:
    def __init__(self):
        pass


class Event:
    def __init__(self):
        self.date = object()
        self.crm_id = object()
        self.other_id = object()
        self.type = object()


