from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.core import serializers

from store.models import User, Supplier

import json

STATUS_GOOD = JsonResponse({'status': 'good'})
NO_ACTIVE_SESSION = JsonResponse({'status': 'bad', 'message': 'No active session'})

def get_my_account(request):
    if request.session['user_id']:
        return User.objects.get(id=request.session['user_id'])

def is_authenticated(request):
    return request.session['authenticated']

def is_staff(request):
    u = User.objects.get(id=request.session['user_id'])
    return u.is_staff

def get_all(request):
    # Django makes it absurdly hard to get just the name and the id. I spent at least an hour trying to come up with this
    s = Supplier.objects.all().values('id', 'name')
    return JsonResponse({'status': 'good', 'data': json.loads(json.dumps(list(s)))})

def get(request, id):
    s = Supplier.objects.filter(id=id).values('id', 'name')
    return JsonResponse({'status': 'good', 'data': json.loads(json.dumps(list(s)))})

@require_http_methods(['POST'])
def add(request):
    me = get_my_account(request)
    if is_authenticated(request) and is_staff(request):
        supplier_name = request.POST.get('name')
        try:
            s = Supplier(name=supplier_name)
            s.save()
            s = Supplier.objects.get(name=supplier_name)
            return JsonResponse({'status': 'good', 'data': {
                'id': s.id,
                'name': s.name
            }})
        except Exception:
            return JsonResponse({'status': 'bad', 'message': 'Could not add supplier'})
    else:
        return JsonResponse({'status': 'bad', 'message': 'User not authorized staff member'})

@require_http_methods(['POST'])
def remove(request):
    me = get_my_account(request)
    if is_authenticated(request) and is_staff(request):
        supplier_id = request.POST.get('id')
        try:
            s = Supplier(id=supplier_id)
            s.delete()
            return STATUS_GOOD
        except Exception:
            return JsonResponse({'status': 'bad', 'message': 'Could not remove supplier'})
    else:
        return JsonResponse({'status': 'bad', 'message': 'User not authorized staff member'})

@require_http_methods(['POST'])
def search(request):
    supplier_name = request.POST.get('name')
    s = Supplier.objects.filter(name__icontains=supplier_name).values('id', 'name')
    return JsonResponse({'status': 'good', 'data': json.loads(json.dumps(list(s)))})
