import pandas as pd

from .date_pars import dateparse


class ADVrepr:
    def __init__(self, path):
        self.path = path

    @property
    def load_csv(self):
        df = pd.read_csv(self.path)
        df = df.drop(df.columns[0], axis=1)
        # df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        return df

    @property
    def info_(self):
        df = self.load_csv
        return df['impressions'].sum(), df['clicks'].sum(), df['ctr'].sum(), df['cost'].sum(), \
               df['avg_cpc'].sum(), *df['source'].unique(), *df['name'].unique()
