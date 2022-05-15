import pandas as pd
from apps.home.views import advs
from apps.home.views import crm

__all__ = [
    'sales_import'
]

sales_import = pd.merge(advs, crm, on=['date', 'source', 'name'], how="outer")
