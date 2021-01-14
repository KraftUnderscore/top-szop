from django.urls import path

from . import views

urlpatterns = [
    path('my_cart', views.my_cart, name='my_cart'),
    path('my_cart/change_amount', views.change_amount, name='change_amount'),
]
