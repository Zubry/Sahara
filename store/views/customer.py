from django.http import HttpResponse
from django.template.loader import get_template
from django import template

def register(request):
    t = get_template('register.html')
    c = template.Context({'name': 'Adrian'})
    return HttpResponse(t.render(c))


def login(request):
    t = get_template('login.html')
    c = template.Context({'name': 'Adrian'})
    return HttpResponse(t.render())
