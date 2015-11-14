from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.core import serializers

from store.models import User, Supplier, Order, Product, Orders, Supplies, Contains

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

import json

# Gets an order by its ID
# May only be used by staff members
def get_by_id(request, cart_id):
    if not is_authenticated(request):
        return NO_ACTIVE_SESSION
    if not is_staff(request):
        return PERMISSIONS

    c = Contains.objects.filter(order_id=cart_id).values('order__date', 'product__active', 'product__name', 'product__description', 'product__price', 'product__stock_quantity', 'quantity')
    o = Orders.objects.filter(order_id=cart_id).values('user__address', 'user__name', 'user__email', 'user_id', 'order__date', 'order__paid')

    products = []

    if(list(o)):
        o = list(o)[0]
    else:
        return JsonResponse({'status': 'bad', 'message': 'Order does not exist'})

    try:
        for product in c:
            products.append({
                'product_name': product['product__name'],
                'product_description': product['product__description'],
                'product_stock_quantity': product['product__stock_quantity'],
                'product_price': product['product__price'],
                'product_active': product['product__active'],
                'product_quantity': product['quantity'],
            })

        return JsonResponse({
            'status': 'good',
            'user': {
                'address': o['user__address'],
                'email': o['user__email'],
                'name': o['user__name'],
                'id': o['user_id'],
            },
            'order': {
                'paid': o['order__paid'],
                'date': o['order__date'],
            },
            'products': products
        })
    except Exception, e:
        return JsonResponse({'status': 'bad', 'message': 'Order does not exist'})

# Searches for an order
# May only be used by staff members
# Results must be sortable on the server
@require_http_methods(["POST"])
def search(request, page):

    return 0

# Gets the specified page of results
# See: get_all
# May only be used by staff members
def get_page(request, page):

    return 0

# Gets the active user's active cart
# The cart should be sortable on the server
def get(request):

    return 0

# Gets all orders
# Should return information about the orderer, the order, and the products
def get_all(request):

    return 0

# Adds an item to the active user's active cart
# If there is no active cart, create one and add the item to it
# This is an alias of product.order
@require_http_methods(["POST"])
def add_item(request):
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

    try:
        o = get_active_cart(me.id)
        add_to_cart(id, quantity, o)
    except Exception:
        o = create_cart(me.id)
        add_to_cart(id, quantity, o)

    return JsonResponse({'status': 'good'})

# Removes an item from the active user's active cart
# If there is more than one of the item in the cart, remove all of them
@require_http_methods(["POST"])
def remove_item(request):
    id = request.POST.get('id')

    if 'id' not in request.POST or id == '':
        return JsonResponse({'status': 'bad', 'message': 'No specified product'})

    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    me = get_my_account(request)

    def get_active_cart(uid):
        return list(Orders.objects.filter(order__paid=False, user__id=uid).values())[0]['order_id']

    def remove_from_cart(product_id, cart_id):
        c = Contains.objects.filter(order_id=cart_id, product_id=product_id)
        c.delete()

    try:
        o = get_active_cart(me.id)
        remove_from_cart(id, o)
    except Exception, e:
        return JsonResponse({'status': 'bad', 'message': 'You have no active carts!', 'e': str(e)})

    return JsonResponse({'status': 'good'})

# Remove all items from the active user's active cart
@require_http_methods(["POST"])
def clear(request):
    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    me = get_my_account(request)

    def get_active_cart(uid):
        return list(Orders.objects.filter(order__paid=False, user__id=uid).values())[0]['order_id']

    def clear_cart(cart_id):
        c = Contains.objects.filter(order_id=cart_id)
        c.delete()

    try:
        o = get_active_cart(me.id)
        clear_cart(o)
        return STATUS_GOOD
    except Exception, e:
        return JsonResponse({'status': 'bad', 'message': 'Could not clear cart'})

# Mark the active user's active cart as paid (inactive)
@require_http_methods(["POST"])
def checkout(request):
    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    me = get_my_account(request)

    def get_active_cart(uid):
        return Orders.objects.get(order__paid=False, user__id=uid)

    o = get_active_cart(me.id)
    return JsonResponse({'val': o.id}, safe=False)

# Adds an item to the specified cart
# May only be used by staff members
@require_http_methods(["POST"])
def add_item_by_id(request, cart_id):

    return 0

# Removes an item from the specified cart
# May only be used by staff members
@require_http_methods(["POST"])
def remove_item_by_id(request, cart_id):

    return 0

# Updates an item in a specified cart
# May only be used by staff members
@require_http_methods(["POST"])
def update_item_by_id(request, cart_id):

    return 0

# Clear a specified cart
# May only be used by staff members
@require_http_methods(["POST"])
def clear_by_id(request, cart_id):

    return 0
