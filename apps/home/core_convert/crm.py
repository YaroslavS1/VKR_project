from typing import Tuple

import pandas as pd

from .aggregation_crm import get_utm, get_pass, get_payment
from .aggregation_crm import get_visit
from .aggregation_crm import get_addto_cart
from .aggregation_crm import get_number

__all__ = [
    'CRMRepr'
]


def prepare(original: Tuple[int, float], _visit, _addto_cart, _pass, _payment, _profit):
    assert len(original) == 5
    visit = original[0]
    addto_cart = original[1]
    pass_ = original[2]
    payment_ = original[3]
    profit = original[4]
    return visit + _visit, addto_cart + _addto_cart, _pass + pass_, _payment + payment_, profit + _profit


class CleanedCRM:
    def __init__(self, date):
        self.date = date


class CRMRepr:
    def __init__(self, path):
        self.path = path

    @property
    def load_csv(self):
        df = pd.read_csv(self.path)
        df = df.drop(df.columns[0], axis=1)
        return df

    @property
    def prepare_load_csv(self):
        df = self.load_csv
        aa = dict()
        for day in df['date_time'].unique():
            df_day = df.loc[df['date_time'] == day]
            s_ = dict()
            for session in df_day['session'].unique():
                df_ses = df_day.loc[df_day['session'] == session]
                utm_source = df_ses.groupby(['date_time']).agg(
                    {'utm_source': get_utm}).reset_index()['utm_source'][0]
                utm_campaign = df_ses.groupby(['date_time']).agg(
                    {'utm_campaign': get_utm}).reset_index()['utm_campaign'][0]
                profit = df_ses.groupby(['date_time']).agg(
                    {'profit': get_number}).reset_index()['profit'][0]
                addto_cart = df_ses.groupby(['date_time']).agg(
                    {'mapped_event': get_addto_cart}).reset_index()['mapped_event'][0]
                visit = df_ses.groupby(['date_time']).agg(
                    {'utm_source': get_visit}).reset_index()['utm_source'][0]
                pass_ = df_ses.groupby(['date_time']).agg(
                    {'mapped_event': get_pass}).reset_index()['mapped_event'][0]
                payment = df_ses.groupby(['date_time']).agg(
                    {'mapped_event': get_payment}).reset_index()['mapped_event'][0]

                if utm_source is not None and utm_campaign is not None:
                    if len(s_) == 0:
                        s_[(utm_source, utm_campaign)] = (visit, addto_cart, pass_, payment, profit)
                    else:
                        s_.update(
                            {(utm_source, utm_campaign): prepare(s_.get((utm_source, utm_campaign), (0, 0, 0, 0, 0)),
                                                                 visit, addto_cart, pass_, payment, profit)})

            aa[day] = s_

        return aa

    @property
    def adv(self):
        a = self.prepare_load_csv
        res = dict()
        for i in a:
            key = next(iter(a[i].keys()))
            if len(res) == 0:
                res[key] = a[i][key]
            else:
                res.update({key: tuple([x+y for x, y in zip(a[i][key], res.get(key, (0, 0, 0, 0, 0)))])})
        return res
