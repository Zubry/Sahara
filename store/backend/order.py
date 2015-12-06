from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.db.models import Sum

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

    c = Contains.objects.filter(order_id=cart_id).values('id', 'order__date', 'product__id', 'product__active', 'product__name', 'product__description', 'product__price', 'product__stock_quantity', 'quantity')
    o = Orders.objects.filter(order_id=cart_id).values('user__address', 'user__name', 'user__email', 'user_id', 'order__date', 'order__paid')

    products = []

    if(list(o)):
        o = list(o)[0]
    else:
        return JsonResponse({'status': 'bad', 'message': 'Order does not exist'})

    try:
        for product in c:
            products.append({
                'order_id': product['id'],
                'product_name': product['product__name'],
                'product_description': product['product__description'],
                'product_stock_quantity': product['product__stock_quantity'],
                'product_price': product['product__price'],
                'product_active': product['product__active'],
                'product_quantity': product['quantity'],
                'product_id': product['product__id'],
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
def search(request):
    if not is_authenticated(request):
        return NO_ACTIVE_SESSION
    if not is_staff(request):
        return PERMISSIONS

    email = request.POST.get("email")
    p = User.objects.get(email=email)
    o = Orders.objects.filter(user=p)

    orders = []
    if o.exists():
        try:
            for order in o:
                c = Contains.objects.filter(order=order.id).values('id', 'order__date', 'product__active', 'product__name', 'product__description', 'product__price', 'product__stock_quantity', 'quantity')
                products = []
                orders.append({'order_id':order.order_id})
                for product in c:
                    products.append({
                        'order_id': product['id'],
                        'product_name': product['product__name'],
                        'product_description': product['product__description'],
                        'product_stock_quantity': product['product__stock_quantity'],
                        'product_price': product['product__price'],
                        'product_active': product['product__active'],
                        'product_quantity': product['quantity'],})
                orders.append({'products': products})

        except Exception:
            return JsonResponse({'status': 'bad', 'message': 'Undefined Error'})

        return JsonResponse({'status': 'good', 'data': orders})
    else:
        return JsonResponse({'status': 'bad', 'message': 'No orders for this user'})

# Gets the specified page of results
# See: get_all
# May only be used by staff members
def get_page(request):
    if not is_authenticated:
        return NO_ACTIVE_SESSION
    if not is_staff:
        return PERMISSIONS

    o = Orders.objects.all()
    pageNum = request.POST.get("page")
    #change back to 10 after testing
    pageStart = ((int(pageNum)  - 1) * 10) + 1
    orderNum = Order.objects.all().count()
    if pageStart > orderNum:
        return JsonResponse({'status': 'good', 'message': 'No results for this page'})
    #return to + 9 after testing with + 1
    pageEnd = pageStart + 9
    if pageEnd > orderNum:
        pageEnd = orderNum
    if pageNum < 1:
        return JsonResponse({'status': 'bad', 'message': 'Invalid page number'})

    print(orderNum)
    print(pageStart)
    print(pageEnd)
    output = []
    if pageStart == orderNum:
        try:
            g = Order.objects.all()[pageStart-1]
            c = Contains.objects.filter(order=g).values('order__date', 'product__active', 'product__name', 'product__description', 'product__price', 'product__stock_quantity', 'quantity')
            p = Orders.objects.filter(order=g).values('user__address', 'user__name', 'user__email', 'user__id')
            for order in p:
                output.append({'user__email': order['user__email'], 'user__name': order['user__name'], 'user__address': order['user__address'], 'user__id': order['user__id']})
            for product in c:
                output.append({'product_name': product['product__name'],
                            'product_description': product['product__description'],
                            'product_stock_quantity': product['product__stock_quantity'],
                            'product_price': product['product__price'],
                            'product_active': product['product__active'],
                            'product_quantity': product['quantity'],
                            })
        except Exception:
            return JsonResponse({'status': 'bad', 'message': 'Index out of bounds'})
    else:
        try:
            for i in range(pageStart,pageEnd):
                if(i > orderNum):
                    return JsonResponse({'status': 'good', 'data': output})
                g = Order.objects.all()[i-1]
                c = Contains.objects.filter(order=g).values('order__date', 'product__active', 'product__name', 'product__description', 'product__price', 'product__stock_quantity', 'quantity')
                p = Orders.objects.filter(order=g).values('user__address', 'user__name', 'user__email', 'user__id')
                for order in p:
                    output.append({'user__email': order['user__email'], 'user__name': order['user__name'], 'user__address': order['user__address'], 'user__id': order['user__id']})
                for product in c:
                    output.append({'product_name': product['product__name'],
                                'product_description': product['product__description'],
                                'product_stock_quantity': product['product__stock_quantity'],
                                'product_price': product['product__price'],
                                'product_active': product['product__active'],
                                'product_quantity': product['quantity'],
                                })
        except Exception:
            return JsonResponse({'status': 'bad', 'message': 'Index out of bounds'})
    return JsonResponse({'status': 'good', 'data': output})

# Gets the active user's active cart
# The cart should be sortable on the server
def get(request):
    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    me = get_my_account(request)

    def get_active_cart(uid):
        return Orders.objects.get(order__paid=False, user__id=uid).order

    def get_products_in_cart(cart_id):
        # Django makes it really, really, really difficult to do something like SELECT SUM(price * quantity) without interacting with raw SQL, which you're really not supposed to do. Fortunately, it's trivial to do with JavaScript on the client, and we don't expect there to be enough items in a cart for it to create a memory/processing power issue
        c = Contains.objects.filter(order_id=cart_id).values('id', 'order__date', 'product__active', 'product__name', 'product__description', 'product__price', 'product__stock_quantity', 'quantity')

        products = []

        for product in c:
            products.append({
                'order_id': product['id'],
                'product_name': product['product__name'],
                'product_description': product['product__description'],
                'product_stock_quantity': product['product__stock_quantity'],
                'product_price': product['product__price'],
                'product_active': product['product__active'],
                'product_quantity': product['quantity'],
            })

        return products

    try:
        o = get_active_cart(me.id)

        return JsonResponse({'status': 'good', 'data': {
            'products': get_products_in_cart(o.id),
            'date': o.date
        }})
    except Exception, e:
        # In all likelihood, this just means they have no active cart
        return JsonResponse({'status': 'good', 'data': {
            'products': []
        }})


# Gets all orders
# Should return information about the orderer, the order, and the products
def get_all(request):
    if not is_authenticated(request):
        return NO_ACTIVE_SESSION
    if not is_staff(request):
        return PERMISSIONS
    o = Orders.objects.all()
    output = []
    if not o.exists():
        return JsonResponse({'status': 'bad', 'message': 'No orders'})
    try:
        for order in o:
            c = Contains.objects.filter(order=order.order).values('id', 'order__date', 'order__paid', 'product__active', 'product__name', 'product__description', 'product__price', 'product__stock_quantity', 'quantity')
            p = Orders.objects.filter(user=order.user).values('user__email').distinct()
            for person in p:
                output.append({'user__email': person['user__email']})
                for product in c:
                    output.append({
                        'order_id': product['id'],
                        'product_name': product['product__name'],
                        'product_description': product['product__description'],
                        'product_stock_quantity': product['product__stock_quantity'],
                        'product_price': product['product__price'],
                        'product_active': product['product__active'],
                        'product_quantity': product['quantity'],
                        'order__date': product['order__date'],
                        'order__paid': product['order__paid'],
                    })

    except Exception:
        return JsonResponse({'status': 'bad', 'message': 'Undefined Error'})
    return JsonResponse({'status': 'good', 'data': output})

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
        p = Product.objects.get(id=pid)
        r = p.stock_quantity
        s = int(c.quantity)
        p.stock_quantity=(r - s)
        p.save()

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
        c = Contains.objects.filter(order_id=cart_id, id=id)
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
        os = Orders.objects.filter(order__paid=False, user__id=uid)

        for o in os:
            o.order__paid = True
            o.save()

        return list(Orders.objects.filter(order__paid=False, user__id=uid).values())[0]['order_id']

    def clear_cart(cart_id):
        c = Contains.objects.filter(order_id=cart_id)
        c.delete()

    try:
        o = get_active_cart(me.id)
        clear_cart(o)
        return STATUS_GOOD
    except Exception, e:
        return JsonResponse({'status': 'bad', 'message': str(e)})

# Mark the active user's active cart as paid (inactive)
@require_http_methods(["POST"])
def checkout(request):
    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    me = get_my_account(request)

    def get_active_cart(uid):
        return Orders.objects.get(order__paid=False, user__id=uid).order

    try:
        o = get_active_cart(me.id)
        o.paid = True
        o.save()
        return STATUS_GOOD
    except Exception, e:
        return JsonResponse({'status': 'bad', 'message': 'Could not checkout'})

# Adds an item to the specified cart
# May only be used by staff members
@require_http_methods(["POST"])
def add_item_by_id(request, user_id):
    id = request.POST.get('id')
    quantity = request.POST.get('quantity')

    if 'id' not in request.POST or id == '':
        return JsonResponse({'status': 'bad', 'message': 'No specified product'})

    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    if not is_staff(request):
        return PERMISSIONS

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
        o = get_active_cart(user_id)
        add_to_cart(id, quantity, o)
    except Exception:
        o = create_cart(user_id)
        add_to_cart(id, quantity, o)

    return JsonResponse({'status': 'good'})

# Removes an item from the specified cart
# May only be used by staff members
@require_http_methods(["POST"])
def remove_item_by_id(request, cart_id):
    id = request.POST.get('id')

    if 'id' not in request.POST or id == '':
        return JsonResponse({'status': 'bad', 'message': 'No specified product'})

    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    if not is_staff(request):
        return PERMISSIONS

    def remove_from_cart(id, cart_id):
        c = Contains.objects.filter(order_id=cart_id, id=id)
        c.delete()

    try:
        remove_from_cart(id, cart_id)
    except Exception, e:
        return JsonResponse({'status': 'bad', 'message': 'User has no active carts!'})

    return JsonResponse({'status': 'good'})

# Updates an item in a specified cart
# May only be used by staff members
# The only thing to update, really, is the quantity, since everything else can be done using another method
@require_http_methods(["POST"])
def update_item_by_id(request, user_id):
    id = request.POST.get('id')
    quantity = request.POST.get('quantity')

    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    if not is_staff(request):
        return PERMISSIONS

    def get_active_cart(uid):
        return list(Orders.objects.filter(order__paid=False, user__id=uid).values())[0]['order_id']

    def update_cart(cart_id, id, quantity):
        c = Contains.objects.get(order_id=cart_id, id=id)
        c.quantity = quantity
        c.save()

    try:
        o = get_active_cart(user_id)
        update_cart(o, id, quantity)
        return STATUS_GOOD
    except Exception, e:
        return JsonResponse({'status': 'bad', 'message': 'Could not update cart'})

# Clear a specified cart
# May only be used by staff members
@require_http_methods(["POST"])
def clear_by_id(request, cart_id):
    if not is_authenticated(request):
        return NO_ACTIVE_SESSION

    if not is_staff(request):
        return PERMISSIONS

    def get_active_cart(id):
        os = Orders.objects.filter(order__paid=False, id=id)

        for o in os:
            o.order__paid = True
            o.save()

        return list(Orders.objects.filter(order__paid=False, user__id=uid).values())[0]['order_id']

    def clear_cart(cart_id):
        c = Contains.objects.filter(order_id=cart_id)
        c.delete()

    try:
        get_active_cart(cart_id)
        clear_cart(cart_id)
        return STATUS_GOOD
    except Exception, e:
        return JsonResponse({'status': 'bad', 'message': 'Could not clear cart'})
