from django.urls import path

from . import views

urlpatterns = [
    path('my_cart', views.my_cart, name='my_cart'),
    path('my_cart/change_amount', views.change_amount, name='change_amount'),
    path('my_cart/add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('my_cart/search', views.search, name='search'),
    path('my_cart/remove', views.remove, name='remove'),
    path('my_cart/order', views.order, name='order'),
]
