from django.shortcuts import render
from django.http import HttpResponse, Http404

from .database_operations import \
    order as order_op, \
    cart as cart_op, \
    product as product_op, \
    discount as discount_op, \
    delivery as delivery_op

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
    products = cart_op.get_all_products_from_cart()
    context = {
        'products_list': products,
    }
    return render(request, 'server/index.html', context)


# 3.1.1 my_cart/change_amount (all products in cart + chosen product)
# in: productId
# out: all products in cart with updated product amount
def change_amount(request):
    name = request.GET.get('name', '')
    amount = request.GET.get('amount', '')

    if amount != '':
        cart_op.set_amount_of_product_in_cart(amount, name)
        return my_cart(None)

    products = cart_op.get_all_products_from_cart()

    old_amount = 0
    for prod in products:
        if prod[0] == name:
            old_amount = prod[1]

    context = {
        'products_list': products,
        'product_old_amount': old_amount,
        'product_name': name
    }

    return render(request, 'server/change_amount.html', context)


# 3.1.2 my_cart/add_to_cart (adds product to cart)
# in: product id
# out: product added to database
def add_to_cart(request):
    name = request.GET.get('name', '')
    cart_op.add_product_to_cart(1, name)
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
        results = product_op.get_products_from_search(param)
        products_list = []
        for r in results:
            products_list.append(r.name)
        context = {
            'products_list': products_list,
            'products_found': True,
        }

    return render(request, 'server/search.html', context)


# 3.1.3 my_cart/remove
# in: productId, amount to decrease
# out: remove amount of product from cart, return all products in cart
def remove(request):
    name = request.GET.get('name', '')
    confirm = request.GET.get('confirm', '')

    if confirm != '':
        cart_op.remove_product_from_cart_by_name(name[:-3])
        return my_cart(None)
    else:
        products = cart_op.get_all_products_from_cart()
        context = {
            'products_list': products,
            'product_name': name,
        }

        return render(request, 'server/remove.html', context)


# 3.1.4 my_cart/order
# in:
# out: all products in cart
def order(request):
    products = cart_op.get_all_products_from_cart()
    total = order_op.calculate_total_cost()

    context = {
        'products_list': products,
        'sum': total,
    }
    return render(request, 'server/order.html', context)


# 3.1.4 my_cart/order_summary
# in: order data
# out: add order to database, return order data
def order_summary(request):
    data = {}
    address = ""

    for key in request.GET:
        data[key] = request.GET.get(key, '')
        address+=f"{data[key]};"

    delivery_op.add_delivery(1, address[:-1])
    products = cart_op.get_all_products_from_cart()
    total = order_op.calculate_total_cost()

    context = data
    context['products_list'] = products
    context['sum'] = total

    return render(request, 'server/order_summary.html', context)


# 3.1.5 my_cart/payment
# in:
# out: (just make a random function in the Template that displays success/ failed xD)
def payment(request):
    status = request.GET.get('status', '')

    if status == 'yes':
        context = {
            'message': 'Operacja zakończona sukcesem',
        }
    elif status == 'no':
        context = {
            'message': 'Przepraszamy, operacja zakończona niepowodzeniem',
        }
    else:
        context = {}

    return render(request, 'server/payment.html', context)


# 3.1.6 manager/panel
# in:
# out:
def panel(request):
    authentication = request.GET.get('authentication', '')
    login = request.GET.get('login', '')
    password = request.GET.get('password', '')

    context = {}

    if authentication != '':
        # login form
        context['authentication'] = 'true'
    elif login != '' and password != '':
        # backend validates stuff and properly sets correct_credentials
        if login == "true":
            correct_credentials = True
        else:
            correct_credentials = False

        # now frontend does its magic
        if correct_credentials:
            context['message'] = "Tożsamość potwierdzona!"
            context['link_'] = "/panel/edit_products"
        else:
            context['message'] = "Niepoprawne dane logowania!"
            context['link_'] = "/panel"

    return render(request, 'server/panel.html', context)


# 3.1.6 manager_panel/discount_creator (no data - display empty creator)
# in:
# out:
def discount_creator(request):
    data = {}

    for key in request.GET:
        data[key] = request.GET.get(key, '')

    context = {}

    # check first if discount is confirmed
    if 'confirm' in data:
        if data['confirm'] == "yes":
            # backend stuff
            return panel(request)
        else:
            # just go back
            return panel(request)

    # backend verifies if data is correct (and sets value is_good to 'good', 'bad' or 'no data')
    is_good = request.GET.get('nazwa', 'no data')

    # frontend sets appropriate data
    if is_good == 'good':
        context['confirm'] = 'good'
        context['message'] = "Czy chcesz potwierdzić podanie promocji?"
    elif is_good == 'bad':
        context['confirm'] = 'bad'
        context['message'] = "Weryfikacja nieudana, podano nieprawidłowe dane."

    return render(request, 'server/discount_creator.html', context)


# 3.1.7 manager_panel/edit_products
# in:
# out: all products
def edit_products(request):
    context = {
        'products_list': [['mikrofala', 2, 12893], ['lodowka', 5, 28912], ['zamrazarka', 14, 89124], ['piekarnik', 122, 73894]]
    }

    return render(request, 'server/edit_products.html', context)


# 3.1.8 manager_panel/edit_products/add_product (no data - display empty creator)
# in:
# out:
def add_product(request):
    data = {}

    for key in request.GET:
        data[key] = request.GET.get(key, '')

    context = {}

    # check data validity
    if 'confirm' in data:
        if data['confirm'] == "yes":
            # backend stuff
            return edit_products(request)
        else:
            # just go back
            return edit_products(request)

    # backend verifies if data is correct (and sets value is_good to 'good', 'bad' or 'no data')
    is_good = request.GET.get('nazwa', 'no data')

    # frontend sets appropriate data
    if is_good == 'good':
        context['confirm'] = 'good'
        context['message'] = "Czy na pewno chcesz dodać produkt?"
    elif is_good == 'bad':
        context['confirm'] = 'bad'
        context['message'] = "Wprowadzone dane są niepoprawne!"

    return render(request, 'server/add_product.html', context)


# 3.1.9 manager_panel/edit_products/remove_checked
# in:
# out: all products
def remove_checked(request):
    data = {}

    for key in request.GET:
        data[key] = request.GET.get(key, '')

    confirmed = request.GET.get('confirm', '')

    # data has list of product names that have been checked
    context = {
        'products_list': [['mikrofala', 2, 12893], ['lodowka', 5, 28912], ['zamrazarka', 14, 89124],
                          ['piekarnik', 122, 73894]]
    }

    if confirmed != '':
        context['message'] = "Pomyślnie usunięto produkty."

    return render(request, 'server/remove_checked.html', context)


# 3.1.9 manager_panel/edit_products/remove
# in: id of product to remove
# out: remove product from database, return updated list of products
def remove_from_entry(request):
    codes = request.GET.get('codes', '')
    confirm = request.GET.get('confirm', '')

    context = {}

    # check data validity
    if confirm == "yes":
        # backend stuff
        return edit_products(request)
    elif confirm == "no":
        # just go back
        return edit_products(request)

    # backend verifies if data is correct (and sets value is_good to 'good', 'bad' or 'no data')
    is_good = codes

    # frontend sets appropriate data
    if is_good == 'good':
        context['confirm'] = 'good'
        context['message'] = "Czy na pewno chcesz usunąć produkty?"
    elif is_good == 'bad':
        context['confirm'] = 'bad'
        context['message'] = "Wprowadzone dane są niepoprawne!"

    return render(request, 'server/remove_from_entry.html', context)
