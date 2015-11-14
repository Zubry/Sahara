"""online_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from store.backend import auth
from store.backend import customer as user
from store.backend import supplier
from store.backend import product
from store.backend import order

from store.views import customer
from store.views import static

urlpatterns = [
    url(r'^$', static.index),
    url(r'^admin/', include(admin.site.urls)),


    # Auth
    url(r'^api/auth/register/$', auth.register),
    url(r'^api/auth/login/$', auth.login),
    url(r'^api/auth/logout/$', auth.logout),

    # User
    url(r'^api/user/me/$', user.me),
    url(r'^api/user/me/email/$', user.update_email),
    url(r'^api/user/me/address/$', user.update_address),
    url(r'^api/user/me/name/$', user.update_name),
    url(r'^api/user/me/password/$', user.update_password),
    url(r'^api/user/me/delete/$', user.delete),

    # Suppliers
    url(r'^api/supplier/add/$', supplier.add),
    url(r'^api/supplier/remove/$', supplier.remove),
    url(r'^api/supplier/(.*)/$', supplier.get),

    url(r'^api/suppliers/search/$', supplier.search), # Pagination needs to be added
    url(r'^api/suppliers/$', supplier.get_all),

    # Products
    url(r'^api/product/add/$', product.add),
    url(r'^api/product/remove/$', product.remove),
    url(r'^api/product/update/$', product.update),
    url(r'^api/product/order/$', product.order),
    url(r'^api/product/supply/$', product.supply),
    url(r'^api/product/(.*)/$', product.get),
    url(r'^api/product/(.*)/activate/$', product.activate),
    url(r'^api/product/(.*)/deactivate/$', product.deactivate),

    url(r'^api/products/search/(.*)/$', product.search),
    url(r'^api/products/(.*)/$', product.get_page),
    url(r'^api/products/$', product.get_all),

    # Order
    url(r'^api/order/add-item/$', order.add_item),
    url(r'^api/order/remove-item/$', order.remove_item),
    url(r'^api/order/clear/$', order.clear),
    url(r'^api/order/checkout/$', order.checkout),

    url(r'^api/order/(.*)/$', order.get_by_id),
    url(r'^api/order/(.*)/add-item/$', order.add_item_by_id),
    url(r'^api/order/(.*)/remove-item/$', order.remove_item_by_id),
    url(r'^api/order/(.*)/update-item/$', order.update_item_by_id),
    url(r'^api/order/(.*)/clear/$', order.clear_by_id),

    url(r'^api/orders/search/(.*)/$', order.search),
    url(r'^api/orders/$', order.get_all),
    url(r'^api/orders/(.*)/$', order.get_page),

    url(r'^api/order/$', order.get),

]
