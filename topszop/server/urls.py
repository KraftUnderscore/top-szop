from django.urls import path

from . import views

urlpatterns = [
    path('my_cart', views.my_cart, name='my_cart'),
    path('my_cart/change_amount', views.change_amount, name='change_amount'),
    path('my_cart/add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('my_cart/search', views.search, name='search'),
    path('my_cart/remove', views.remove, name='remove'),
    path('my_cart/order', views.order, name='order'),
    path('my_cart/order_summary', views.order_summary, name='order_summary'),
    path('my_cart/payment', views.payment, name='payment'),
    path('panel', views.panel, name='panel'),
    path('panel/discount_creator', views.discount_creator, name='discount_creator'),
    path('panel/edit_products', views.edit_products, name='edit_products'),
    path('panel/edit_products/add_product', views.add_product, name='add_product'),
    path('panel/edit_products/remove_checked', views.remove_checked, name='remove_checked'),
    path('panel/edit_products/remove_from_entry', views.remove_from_entry, name='remove_from_entry'),
    path('my_cart/confirm_order', views.confirm_order, name='confirm_order'),
]
