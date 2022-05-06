# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import io
import random

import pandas as pd
import plotly.express as px
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import plotly.graph_objects as go

from .core_convert import CRMRepr
from .core_convert.adv import ADVrepr
from .tests_vkr.tools.ADV import AdvCampaign
from .tests_vkr.visualization.tests_funnel_plot import count_adv

_a1 = ADVrepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_1.csv')
_a2 = ADVrepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_2.csv')
a1 = _a1.load_csv
a2 = _a2.load_csv

_crm = CRMRepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMO.csv')
crm = _crm.prepare_load_csv


@login_required(login_url="/login/")
def index(request):
    crm_ = _crm.load_csv
    context = {'segment': 'Дашборд'}
    buffer = io.StringIO()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a1['date'], y=a1['cost'], name=a1['source'].unique()[0]+' '+a1['name'].unique()[0]))
    fig.add_trace(go.Scatter(x=a2['date'], y=a2['cost'], name=a2['source'].unique()[0]+' '+a2['name'].unique()[0]))
    # fig.add_trace(go.Scatter(x=crm_['date'], y=crm_['cost'], name='Прибыль'))
    context.update({'cost': a1['cost'].sum() + a2['cost'].sum()})
    context.update({'profit': crm_['profit'].sum()})
    context.update({'сustomers': a1['clicks'].sum() + a2['clicks'].sum()})
    context.update({'registr': a1['cost'].sum() + a2['cost'].sum()})



    # go.Scatter(x=df['Date'], y=df['AAPL.High'])
    # df = px.data.iris()  # replace with your own data source
    # fig = px.scatter(
    #     df, x="sepal_width", y="sepal_length",
    #     color="species")
    fig.update_layout(paper_bgcolor='#ffeed6')
    fig.write_html(buffer, config={'displaylogo': False})
    html_bytes = buffer.getvalue()
    context.update({'plot1': html_bytes})

    html_template = loader.get_template('home/dashboard.html')

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def campaigns(request):
    context = {'segment': 'Рекламные кампании'}
    html_template = loader.get_template('home/campaigns.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def kpi(request):
    context = {'segment': 'KPI'}
    html_template = loader.get_template('home/campaigns_kpi.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def funnel(request):
    buffer = io.StringIO()
    stages = ["Количество показов рекламы", "Клики по рекламным обьявлениям", "Добавления в корзину", "Оформление заказов", "Покупки"]
    df_s = []
    crm_adv_inf = _crm.adv
    for i, i_c, adv in zip(range(2), crm_adv_inf, (_a1, _a2)):
        df_ = pd.DataFrame(dict(
            количество=[adv.info_[0],
                        adv.info_[1],
                        crm_adv_inf[i_c][1],
                        crm_adv_inf[i_c][2],
                        crm_adv_inf[i_c][3]], стадии=stages))
        df_['Рекламная кампания'] = i_c[0] + '' + i_c[1]
        df_s.append(df_)
    df = pd.concat(df_s, axis=0)
    fig = px.funnel(df, x='количество', y='стадии', color='Рекламная кампания', height=800)
    fig.write_html(buffer, config={'displaylogo': False})
    html_template = loader.get_template('home/funnel.html')
    html_bytes = buffer.getvalue()
    context = {'segment': 'Воронка продаж', 'plot1': html_bytes}

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    # if request.path.split('/')[1] == 'django_plotly_dash':
    #     return None
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
