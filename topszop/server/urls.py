from django.urls import path

from . import views

urlpatterns = [
    path('my_cart', views.my_cart, name='my_cart'),
]
