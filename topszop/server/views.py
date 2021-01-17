from django.shortcuts import render
from django.http import HttpResponse

from .database_operations import *


# My proposition for interface between Templates and backend:
# <interface number> url path/ subpath, ex. for 3.1.2 localhost:8000/my_cart/search
# in: expected input from interface, ex. for 3.1.2 localhost:8000/my_cart/search?name=kanapka
# out: action from backend/ response page, ex. for 3.1.2 search, the backend would prepare
#      a list of all products matching the name and pass it onto the Template (which should interpret
#      whether there were results and should display them or give "Not found" message)

# 3.1.1 my_cart
# in:
# out: all products in cart
def my_cart(request):
    context = {
        'products_list': [['mikrofala', 2], ['lodowka', 5], ['zamrazarka', 14], ['piekarnik', 122]],
    }
    return render(request, 'server/index.html', context)


# 3.1.1 my_cart/change_amount (all products in cart + chosen product)
# in: productId
# out: all products in cart with updated product amount
def change_amount(request):
    name = request.GET.get('name', '')
    amount = request.GET.get('amount', '')

    if amount != '':
        # update amount to database
        return my_cart(None)
    else:
        context = {
            'products_list': [['mikrofala', 2], ['lodowka', 5], ['zamrazarka', 14], ['piekarnik', 122]],
            'product_old_amount': 10,
            'product_name': name,
        }
        return render(request, 'server/change_amount.html', context)


# 3.1.2 my_cart/add_to_cart (adds product to cart)
# in: product id
# out: product added to database
def add_to_cart(request):
    name = request.GET.get('name', '')

    return my_cart(None)


# 3.1.2 my_cart/search (product matching name)
# in: name
# out: products matching name
def search(request):
    param = request.GET.get('phrase', '')
    if param == '':
        context = {
            'products_found': False,
        }
    else:
        # [product_name]
        context = {
            'products_list': ['mikrofala', 'lodowka', 'zamrazarka', 'piekarnik'],
            'products_found': True,
        }

    return render(request, 'server/search.html', context)


# 3.1.3 my_cart/remove
# in: productId, amount to decrease
# out: remove amount of product from cart, return all products in cart
def remove(request):
    name = request.GET.get('name', '')

    context = {
        'products_list': [['mikrofala', 2], ['lodowka', 5], ['zamrazarka', 14], ['piekarnik', 122]],
        'product_name': name,
    }

    return render(request, 'server/remove.html', context)


# 3.1.4 my_cart/order
# in:
# out: all products in cart
def order(request):
    context = {
        'products_list': [['mikrofala', 2], ['lodowka', 5], ['zamrazarka', 14], ['piekarnik', 122]],
    }
    return render(request, 'server/order.html', context)

# 3.1.4 my_cart/order_summary
# in: order data
# out: add order to database, return order data

# 3.1.5 my_cart/payment
# in:
# out: (just make a random function in the Template that displays success/ failed xD)

# 3.1.6 manager/panel
# in:
# out:

# 3.1.6 manager_panel/discount_creator (no data - display empty creator)
# in:
# out:

# 3.1.6 manager_panel/discount_creator
# in: discount data
# out: discount data on success (display confirmation alert)
#      or empty on failed (display failed message)

# 3.1.7 manager_panel/edit_products
# in:
# out:

# 3.1.7 manager_panel/edit_products/list
# in:
# out: all products

# 3.1.8 manager_panel/edit_products/add_product (no data - display empty creator)
# in:
# out:

# 3.1.8 manager_panel/edit_products/add_product
# in: product data
# out: 0 on success and added product data
#      1 on duplicate and duplicate product data
#      2 on incorrect data and to-be-added product data

# 3.1.8 manager_panel/edit_products/add_product/confirm
# in: product data
# out: add product to database

# 3.1.9 manager_panel/edit_products/remove
# in:
# out: all products

# 3.1.9 manager_panel/edit_products/remove
# in: id of product to remove
# out: remove product from database, return updated list of products
