from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.core import serializers

from store.models import User, Supplier, Orders, Supplies

import json

@require_http_methods(["GET"])
# Gets the product at the specified ID
def get(request, id):

    return 0

@require_http_methods(["GET"])
# Returns a list of all products, with the following information:
#   * Name
#   * Description
#   * Price
#   * Number in stock
#   * Suppliers (Requires a join with Supplies)
# Inactive items should not be included by default
# Results should be sortable on the server
def get_all(request):

    return 0

@require_http_methods(["GET"])
# Same specification as get_all, except the results should be paginated
def get_page(request, page):

    return 0

@require_http_methods(["POST"])
# Same specification as get_all, and products should be searched by title and description
# Users should be able to filter by price and manufacturer
# Only in-stock products should be shown
def search(request, page):

    return 0

@require_http_methods(["POST"])
# Adds a product to the database
# May only be used by staff members
# All products must have a name, description, and price
# All other attributes are optional
# Stock defaults to 0, active defaults to True
def add(request):

    return 0

@require_http_methods(["POST"])
# Removes a product from the database
# May only be used by staff members
def remove(request):

    return 0

@require_http_methods(["POST"])
# Updates an item in the database
# May only be used by staff members
# All unspecified attributes are left untouched
def update(request):

    return 0

@require_http_methods(["POST"])
# Adds the specified item to the signed-in user's active cart
def order(request):

    return 0

@require_http_methods(["POST"])
# Activates a product
# May only be used by staff members
def activate(request):

    return 0

@require_http_methods(["POST"])
# Deactivates a product
# May only be used by staff members
def deactivate(request):

    return 0

@require_http_methods(["POST"])
# Establishes a supplier of a product
# May only be used by staff members
def supply(request):

    return 0
