from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from datetime import datetime, timedelta

from store.models import User, Supplier, Orders, Supplies, Product, Contains, Order

import json

def get_my_account(request):
    if request.session['user_id']:
        return User.objects.get(id=request.session['user_id'])

def is_authenticated(request):
    return request.session['authenticated']

def is_staff(request):
    u = User.objects.get(id=request.session['user_id'])
    return u.is_staff

STATUS_GOOD = JsonResponse({'status': 'good'})
NO_ACTIVE_SESSION = JsonResponse({'status': 'bad', 'message': 'No active session'})
PERMISSIONS = JsonResponse({'status': 'bad', 'message': 'You do not have the required permissions to access this page'})

# Gets the product at the specified ID
def get(request, id):
    p = Product.objects.filter(id=id).values('id', 'name', 'description', 'price', 'stock_quantity', 'active')
    return JsonResponse({'status': 'good', 'data': json.loads(json.dumps(list(p)))})

# Returns a list of all products, with the following information:
#   * Name
#   * Description
#   * Price
#   * Number in stock
#   * Suppliers (Requires a join with Supplies)
# Inactive items should not be included by default
# Results should be sortable on the server
def get_all(request):
    p = Product.objects.filter(active=True).values('id', 'name', 'description', 'price', 'stock_quantity')
    return JsonResponse({'status': 'good', 'data': json.loads(json.dumps(list(p)))})

# Same specification as get_all, except the results should be paginated
def get_page(request, page):

    return 0

@require_http_methods(["POST"])
# Same specification as get_all, and products should be searched by title and description
# Users should be able to filter by price
# Only in-stock products should be shown
def search(request):
    query = request.POST.get('query')
    s = request.POST.get('sort')

    p = Product.objects.filter(active=True).filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )

    if s == '-p':
        p = p.order_by('-price')
    elif s == 'p':
        p = p.order_by('price')
    else:
        p = p.order_by('name')

    return JsonResponse({'status': 'good', 'data': json.loads(json.dumps(list(p.values('id', 'name', 'description', 'price', 'stock_quantity'))))})

@require_http_methods(["POST"])
# Adds a product to the database
# May only be used by staff members
# All products must have a name, description, and price
# All other attributes are optional
# Stock defaults to 0, active defaults to True
def add(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    price = request.POST.get('price')
    active = request.POST.get('active')
    stock_quantity = request.POST.get('stock_quantity')

    if is_authenticated(request) and is_staff(request):
        p = Product(name=name, description=description, price=price, stock_quantity=stock_quantity)
        p.save()
        return STATUS_GOOD
    else:
        return NO_ACTIVE_SESSION

@require_http_methods(["POST"])
# Removes a product from the database
# May only be used by staff members
# Will use assertions to ensure that the product hasn't been purchased in a month
def remove(request):
    id = request.POST.get('id')

    if 'id' not in request.POST or id == '':
        return JsonResponse({'status': 'bad', 'message': 'No specified product'})

    if is_authenticated(request) and is_staff(request):
        last_month = datetime.today() - timedelta(days=30)
        try:
            p = Product.objects.get(id=id)
            o = Order.objects.filter(date__gt=last_month)
            if not Contains.objects.filter(product=p, order=o).exists():
                p.delete()
                return STATUS_GOOD
            else:
                return JsonResponse({'status': 'bad', 'message': 'Product ordered within the last month'})
        except Exception:
            return JsonResponse({'status': 'bad', 'message': 'Product does not exist'})
    else:
        return NO_ACTIVE_SESSION

@require_http_methods(["POST"])
# Updates an item in the database
# May only be used by staff members
# All unspecified attributes are left untouched
def update(request):
    id = request.POST.get('id')

    if 'id' not in request.POST or id == '':
        return JsonResponse({'status': 'bad', 'message': 'No specified product'})

    if is_authenticated(request) and is_staff(request):
        try:
            p = Product.objects.get(id=id)

            if 'name' in request.POST and request.POST.get('name') != '':
                p.name = request.POST.get('name')
            if 'description' in request.POST and request.POST.get('description') != '':
                p.description = request.POST.get('description')
            if 'price' in request.POST and request.POST.get('price') != '':
                p.price = request.POST.get('price')
            if 'stock_quantity' in request.POST and request.POST.get('stock_quantity') != '':
                p.stock_quantity = request.POST.get('stock_quantity')

            p.save()

            p = Product.objects.filter(id=id).values()

            # Since id is unique, grabbing the 0th item in the list forces the json to just return an object, not an array with one object
            return JsonResponse({'status': 'good', 'data': json.loads(json.dumps(list(p)[0]))})
        except Exception, e:
            return JsonResponse({'status': 'bad', 'message': str(e)})
    else:
        return NO_ACTIVE_SESSION

@require_http_methods(["POST"])
# Adds the specified item to the signed-in user's active cart
def order(request):
    id = request.POST.get('id')
    quantity = request.POST.get('quantity')

    if 'id' not in request.POST or id == '':
        return JsonResponse({'status': 'bad', 'message': 'No specified product'})

    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    me = get_my_account(request)

    def get_active_cart(uid):
        return Orders.objects.get(order__paid=False, user__id=uid).order

    def create_cart(uid):
        o = Order(paid=False)
        o.save()
        os = Orders(order_id=o.id, user_id=uid)
        os.save()
        return o

    def add_to_cart(pid, quantity, cart):
        c = Contains(quantity=quantity, order=cart, product_id=pid)
        c.save()
        p = Product.objects.get(id=pid)
        r = p.stock_quantity
        s = int(c.quantity)
        p.stock_quantity=(r - s)
        p.save()


    o = None
    try:
        o = get_active_cart(me.id)
        add_to_cart(id, quantity, o)
    except Exception:
        o = create_cart(me.id)
        add_to_cart(id, quantity, o)

    return JsonResponse({'status': 'good'})

@require_http_methods(["POST"])
# Activates a product
# May only be used by staff members
def activate(request):
    id = request.POST.get('id')

    if 'id' not in request.POST or id == '':
        return JsonResponse({'status': 'bad', 'message': 'No specified product'})
    if is_authenticated(request) and is_staff(request):
        try:
            p = Product.objects.get(id=id)
            p.active = True
            p.save()
            return JsonResponse({'status': 'good', 'message': 'Product activated'})
        except Exception, e:
            return JsonResponse({'status': 'bad', 'message': str(e)})
    else:
        return NO_ACTIVE_SESSION

@require_http_methods(["POST"])
# Deactivates a product
# May only be used by staff members
def deactivate(request):
    id = request.POST.get('id')

    if 'id' not in request.POST or id == '':
        return JsonResponse({'status': 'bad', 'message': 'No specified product'})
    if is_authenticated(request) and is_staff(request):
        try:
            p = Product.objects.get(id=id)
            p.active = False
            p.save()
            return JsonResponse({'status': 'good', 'message': 'Product deactivated'})
        except Exception:
            return JsonResponse({'status': 'bad', 'message': 'Product failed to deactivate'})

    else:
        return NO_ACTIVE_SESSION

@require_http_methods(["POST"])
# Establishes a supplier of a product
# May only be used by staff members
def supply(request):
    supplier = request.POST.get('supplier')
    product = request.POST.get('product')
    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    if not is_staff(request):
        return PERMISSIONS

    s = Supplies(supplier_id=supplier, product_id=product)
    return STATUS_GOOD
