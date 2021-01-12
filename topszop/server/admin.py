from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(Discount_Product)
admin.site.register(Cart)
admin.site.register(Cart_Product)
admin.site.register(Order)
admin.site.register(Delivery)
