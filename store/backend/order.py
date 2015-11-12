from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.core import serializers

from store.models import User, Supplier, Order, Product, Orders, Supplies, Contains

import json

# Gets an order by its ID
# May only be used by staff members
def get_by_id(request, cart_id):

    return 0

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
@require_http_methods(["POST"])
def add_item(request):

    return 0

# Removes an item from the active user's active cart
# If there is more than one of the item in the cart, remove all of them
@require_http_methods(["POST"])
def remove_item(request):

    return 0

# Update the active user's active cart's information, potentially including its quantity
@require_http_methods(["POST"])
def update_item(request):

    return 0

# Remove all items from the active user's active cart
@require_http_methods(["POST"])
def clear(request):

    return 0

# Mark the active user's active cart as paid (inactive)
@require_http_methods(["POST"])
def checkout(request):

    return 0

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
