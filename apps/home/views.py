# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


@login_required(login_url="/login/")
def index(request):
    print(request.method)

    import plotly.express as px
    from base64 import b64encode
    import io

    buffer = io.StringIO()

    df = px.data.iris()  # replace with your own data source
    fig = px.scatter(
        df, x="sepal_width", y="sepal_length",
        color="species")
    fig.update_layout(paper_bgcolor='#F2F4F6')
    fig.write_html(buffer)
    html_bytes = buffer.getvalue()
    # encoded = b64encode(html_bytes).decode()
    context = {'segment': 'index', 'aaee': html_bytes}

    html_template = loader.get_template('home/dashboard.html')

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
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
