# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import random

import pandas as pd
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import plotly.express as px

from .tests_vkr.tools.ADV import AdvCampaign
from .tests_vkr.visualization.tests_funnel_plot import count_adv


@login_required(login_url="/login/")
def index(request):

    import plotly.express as px
    import io

    buffer = io.StringIO()

    df = px.data.iris()  # replace with your own data source
    fig = px.scatter(
        df, x="sepal_width", y="sepal_length",
        color="species")
    fig.update_layout(paper_bgcolor='#F2F4F6')
    fig.write_html(buffer, config={'displaylogo': False})
    html_bytes = buffer.getvalue()
    context = {'segment': 'Дашборд', 'aaee': html_bytes}

    html_template = loader.get_template('home/dashboard.html')

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def campaigns(request):
    context = {'segment': 'Рекламные кампании'}
    html_template = loader.get_template('home/campaigns.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def funnel(request):
    import io

    buffer = io.StringIO()
    adv_campaigns = list()
    sum_cost = [random.randint(10000, 90000) for _ in range(3)]
    profit = [random.randint(10000, 1000000) for _ in range(3)]
    visits = [random.randint(1000, 2000) for _ in range(3)]
    purchases = [random.randint(1000, 1500) for _ in range(3)]
    for i in range(3):
        adv_campaigns.append(
            AdvCampaign(
                name=f'Test_campain{i}',
                start_date='24.05.2010',
                end_date='24.10.2010',
                sum_cost=sum_cost[i]))

    crm = {('yandex', f'Test_campain{i}'): (profit[i], visits[i], purchases[i]) for i in range(3)}

    stages = ["Количество показов рекламы", "Клики по рекламным обьявлениям", "Покупки"]
    df_s = []
    for i, i_c, adv in zip(range(3), crm, adv_campaigns):
        concurrent_adv = count_adv(adv)
        df_ = pd.DataFrame(dict(
            количество=[concurrent_adv[i_c][2] if i_c == ('yandex', 'Test_campain1') else concurrent_adv[i_c][1],
                        concurrent_adv[i_c][2],
                        # concurrent_adv[i_c][2],
                        crm[i_c][2]], стадии=stages))
        # print(i_c)
        df_['Рекламная кампания'] = i_c[0] + i_c[1]
        # df_toronto = pd.DataFrame(dict(number=[52, 36, 18, 14, 5], stage=stages))
        # df_toronto['office'] = 'Toronto'
        df_s.append(df_)
    df = pd.concat(df_s, axis=0)
    fig = px.funnel(df, x='количество', y='стадии', color='Рекламная кампания', height=800)
    fig.update_layout(paper_bgcolor='#F2F4F6')
    fig.write_html(buffer, config={'displaylogo': False})
    html_template = loader.get_template('home/funnel.html')
    html_bytes = buffer.getvalue()
    context = {'segment': 'Воронка продаж', 'aaee': html_bytes}

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
