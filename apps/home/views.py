# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import io

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from plotly.subplots import make_subplots

from .core_convert.adv import ADVrepr
from .core_convert.crm import CRMext

_a1 = ADVrepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_1.csv')
_a2 = ADVrepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_2.csv')
_a3 = ADVrepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_3.csv')
_a4 = ADVrepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_4.csv')
_a5 = ADVrepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_5.csv')
_a6 = ADVrepr('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/DEMOA_6.csv')
a1 = _a1.load_csv
a2 = _a2.load_csv
a3 = _a3.load_csv
a4 = _a4.load_csv
a5 = _a5.load_csv
a6 = _a6.load_csv
adv = (a1, a2, a3, a4, a5, a6)
advs = pd.concat((a1, a2, a3, a4, a5, a6))

_crm = CRMext('/home/y_sukhorukov/VKR/VKR_PROJECT/tests/crm.csv')
crm = _crm.load_csv


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'Главная'}

    buffer = io.StringIO()

    summary_cost = round(sum([i['cost'].sum() for i in adv]), 2)
    summary_profit = round(crm['profit'].sum(), 2)
    customers = sum([i['clicks'].sum() for i in adv])
    payment = round(crm['payment'].sum(), 2)
    addto_cart = round(crm['addto_cart'].sum(), 2)

    context.update({'cost': summary_cost})
    context.update({'profit': summary_profit})
    context.update({'cpc': 0 if customers == 0 else round(summary_cost / customers, 2)})
    context.update({'customers': customers})
    context.update({'payment': payment})
    context.update({'conversion': customers / payment})
    context.update({'CAR': round((1 - payment / addto_cart) * 100, 2)})
    context.update({'aov': round(summary_profit / customers, 2)})
    context.update({'addto_cart': addto_cart})
    context.update({'roi': round(((summary_profit - summary_cost) / summary_cost) * 100, 2)})

    ll = [(i['source'].unique()[0], i['name'].unique()[0]) for i in adv]
    costs = [i['cost'].sum() for i in adv]
    profits = [crm.loc[crm['name'] == i[1]]['profit'].sum() for i in ll]
    _roi = [round((profit - cost) / cost * 100, 2) for cost, profit in zip(costs, profits)]
    _roi_rep = [(n[0] + ' ' + n[1], i) for i, n in zip(_roi, ll) if i <= 0]

    context.update({'roi_rep': _roi_rep})

    # labels = [i[0] + ' ' + i[1] for i in ll]
    # values = [crm.loc[crm['name'] == i[1]]['profit'].sum() for i in ll]
    # fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    ll = [(i['source'].unique()[0], i['name'].unique()[0]) for i in adv]
    labels = [l[0] + ' ' + l[1] for l in ll]
    costs = [i['cost'].sum() for i in adv]
    impression = [i['impressions'].sum() for i in adv]
    profits = [crm.loc[crm['name'] == i[1]]['profit'].sum() for i in ll]

    fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=costs,
                         name="Затраты", title_text='Затраты'), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=profits,
                         name="Выручка", title_text='Выручка'), 1, 2)
    fig.add_trace(go.Pie(labels=labels, values=impression,
                         name="Показы", title_text='Показы'), 1, 3)
    fig.write_html(buffer, config={'displaylogo': False})
    html_bytes1 = buffer.getvalue()
    context.update({'plot1': html_bytes1})

    fig = go.Figure()
    for i in adv:
        fig.add_trace(go.Scatter(x=i['date'], y=i['cost'], name=i['source'].unique()[0] + ' ' + i['name'].unique()[0]))
    fig.update_xaxes(rangeslider_visible=True)
    fig.write_html(buffer, config={'displaylogo': False})
    html_bytes = buffer.getvalue()
    context.update({'plot2': html_bytes})

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def campaigns(request):
    context = {'segment': 'Рекламные кампании'}
    html_template = loader.get_template('home/campaigns.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def add(request):
    context = {'segment': 'Данные'}
    html_template = loader.get_template('home/add.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def sdash(request):
    context = {'segment': 'Дашборд'}
    html_template = loader.get_template('home/sdash.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def kpi(request):
    context = {'segment': 'KPI'}
    html_template = loader.get_template('home/campaigns_kpi.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def funnel(request):
    buffer = io.StringIO()
    stages = ["Количество показов рекламы", "Клики по рекламным обьявлениям", "Добавления в корзину",
              "Оформление заказов", "Покупки"]
    df_s = []
    # crm_adv_inf = _crm.adv
    label = [(i['source'].unique()[0], i['name'].unique()[0]) for i in adv]
    impressions = [i['impressions'].sum() for i in adv]
    visit = [i['clicks'].sum() for i in adv]
    addto_cart = [crm.loc[crm['name'] == i[1]]['addto_cart'].sum() for i in label]
    pass_ = [crm.loc[crm['name'] == i[1]]['pass'].sum() for i in label]
    payment = [crm.loc[crm['name'] == i[1]]['payment'].sum() for i in label]

    for i in zip(label, impressions, visit, addto_cart, pass_, payment):
        df_ = pd.DataFrame(dict(
            количество=i[1:], стадии=stages))
        df_['Рекламная кампания'] = i[:1][0][0] + ' ' + i[:1][0][1]
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
