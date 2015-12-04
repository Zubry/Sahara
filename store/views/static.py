from django.http import HttpResponse
from django.template.loader import get_template
from django import template

def index(request):
    t = get_template('index.html')
    c = template.Context()
    return HttpResponse(t.render())
