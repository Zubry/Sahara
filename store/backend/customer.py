from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

from store.models import User

import bcrypt
import json

STATUS_GOOD = JsonResponse({'status': 'good'})
NO_ACTIVE_SESSION = JsonResponse({'status': 'bad', 'message': 'No active session'})

def get_my_account(request):
    if request.session['user_id']:
        return User.objects.get(id=request.session['user_id'])

def is_authenticated(request):
    return request.session['authenticated']

def me(request):
    if is_authenticated(request):
        u = get_my_account(request);

        return JsonResponse({
            'status': 'good',
            'data': {
                'name': u.name,
                'address': u.address,
                'email': u.email,
                'staff': u.is_staff
            }
        })
    else:
        return NO_ACTIVE_SESSION


@require_http_methods(["POST"])
def delete(request):
    # Require a password to delete an account
    password = request.POST.get("password")
    if is_authenticated(request):
        try:
            u = get_my_account(request)
            hashed = u.password

            # Make sure that the current password is valid
            if bcrypt.hashpw(password.encode('utf-8'), hashed.encode('utf-8')) == hashed:
                u.delete()
                request.session['authenticated'] = False
                request.session['user_id'] = None
                return STATUS_GOOD
            else:
                return JsonResponse({'status': 'bad', 'message': 'Incorrect password'})
        except Exception, e:
            return JsonResponse({'status': 'bad', 'message': 'Could not delete account'})
    else:
        return NO_ACTIVE_SESSION

@require_http_methods(["POST"])
def update_name(request):
    new_name = request.POST.get("name")
    if is_authenticated(request):
        try:
            u = get_my_account(request)
            u.name = new_name
            u.save()
            u = get_my_account(request)
            return JsonResponse({'status': 'good', 'data': {
                'name': u.name
            }});
        except Exception, e:
            return JsonResponse({'status': 'bad', 'message': 'Invalid name'})
    else:
        return NO_ACTIVE_SESSION

@require_http_methods(["POST"])
def update_email(request):
    new_email = request.POST.get("email")
    if is_authenticated(request):
        try:
            u = get_my_account(request)
            u.email = new_email
            u.save()
            return STATUS_GOOD
        except Exception, e:
            return JsonResponse({'status': 'bad', 'message': 'Invalid email'})
    else:
        return NO_ACTIVE_SESSION

@require_http_methods(["POST"])
def update_address(request):
    new_address = request.POST.get("address")
    if is_authenticated(request):
        try:
            u = get_my_account(request)
            u.address = new_address
            u.save()
            return STATUS_GOOD
        except Exception, e:
            return JsonResponse({'status': 'bad', 'message': str(e)})
    else:
        return NO_ACTIVE_SESSION

@require_http_methods(["POST"])
def update_password(request):
    new_password = request.POST.get("new_password")
    current_password = request.POST.get("current_password")

    if is_authenticated(request):
        try:
            u = get_my_account(request)
            hashed = u.password

            # Make sure that the current password is valid
            if bcrypt.hashpw(current_password.encode('utf-8'), hashed.encode('utf-8')) == hashed:
                u.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(14))
                u.save()
                return STATUS_GOOD
            else:
                return JsonResponse({'status': 'bad', 'message': 'Incorrect password'})
        except Exception, e:
            return JsonResponse({'status': 'bad', 'message': 'Invalid password'})
    else:
        return NO_ACTIVE_SESSION
