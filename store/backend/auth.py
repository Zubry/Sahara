from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

from store.models import User

import string
import bcrypt
import json
import urllib

def logout(request):
    request.session['authenticated'] = False
    request.session['user_id'] = None
    return JsonResponse({'status': 'good'})

@require_http_methods(["POST"])
def login(request):
    # Get the user with the specified email and check their password against the specified password
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
        u = User.objects.get(email=email)
        hashed = u.password
        if bcrypt.hashpw(password.encode('utf-8'), hashed.encode('utf-8')) == hashed:
            request.session['authenticated'] = True
            request.session['user_id'] = u.id
            return JsonResponse({'status': 'good', 'data': {
                'name': u.name,
                'staff': u.is_staff
            }});
        else:
            return JsonResponse({'status': 'bad', 'message': 'Email or password is incorrect'})
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'bad', 'message': 'Email or password is incorrect'})

@require_http_methods(["POST"])
def register(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    name = request.POST.get("name")
    address = request.POST.get("address")
    # Generate a salt, hash the password, and store information in the database.
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
    u = User(name=name, password=password, email=email, address=address)
    try:
        u.save()
        return JsonResponse({'status': 'good', 'data': {
            'name': u.name,
            'staff': u.is_staff
        }})
    except Exception, e:
        return JsonResponse({'status': 'bad', 'message': 'Email is already registered'})


def get_email(request):
    u = User.objects.get(id=request.session['user_id'])
    return JsonResponse({'email': u.email})
