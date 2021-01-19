from django.shortcuts import render
from django.http import HttpResponse, Http404

from .database_operations import \
    order as order_op, \
    cart as cart_op, \
    product as product_op, \
    discount as discount_op, \
    delivery as delivery_op

class Memory():
    def __init__(self):
        self.codes_to_remove = []
        self.prods_to_remove = []
        self.add_product_data = []

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

    context = data

    if any(x == '' for x in data.values()):
        return order(request)

    delivery_op.add_delivery(1, address[:-1])
    products = cart_op.get_all_products_from_cart()
    total = order_op.calculate_total_cost()

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
            'link_': '/my_cart/confirm_order?confirm=yes',
        }
    elif status == 'no':
        context = {
            'message': 'Przepraszamy, operacja zakończona niepowodzeniem',
            'link_': '/my_cart/confirm_order?confirm=no',
        }
    else:
        context = {}

    return render(request, 'server/payment.html', context)


def confirm_order(request):
    confirm = request.GET.get('confirm', '')

    if confirm == 'yes':
        context = {
            'message': 'Dziękujemy za złożenie zamówienia'
        }
        cart_op.clean_cart()
    else:
        context = {
            'message': 'Niestety, nie udało się złożyć zamówienia :('
        }

    return render(request, 'server/confirm_order.html', context)


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
        login = "true"
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
            discount_op.add_discount(data["start"], data["koniec"],
                                     float(data["procent"]), int(data["koszt"]))
            return panel(request)
        else:
            # just go back
            return panel(request)

    # backend verifies if data is correct (and sets value is_good to 'good', 'bad' or 'no data')
    is_good = request.GET.get('nazwa', '')

    if is_good != '':
        try:
            if discount_op.is_valid(discount_op.timezone_parse_date(data["start"]),
                                    discount_op.timezone_parse_date(data["koniec"]),
                                    float(data["procent"]), int(data["koszt"])):
                is_good = 'good'
            else:
                is_good = 'bad'
        except ValueError:
            is_good = 'bad'

    # frontend sets appropriate data
    if is_good == 'good':
        context['confirm'] = 'good'
        context['message'] = "Czy chcesz potwierdzić podanie promocji?"
        context['params'] = "/panel/discount_creator?confirm=yes&" + ''.join(["&" + k + "=" + v for k, v in data.items()])
    elif is_good == 'bad':
        context['confirm'] = 'bad'
        context['message'] = "Weryfikacja nieudana, podano nieprawidłowe dane."

    return render(request, 'server/discount_creator.html', context)


# 3.1.7 manager_panel/edit_products
# in:
# out: all products
def edit_products(request):
    products_list = []
    for prod in product_op.get_all_products():
        products_list.append((prod.name, prod.price, prod.id))

    context = {
        'products_list': products_list
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
            p_data = Memory.add_product_data
            product_op.add_product(p_data['nazwa'], p_data['opis'], p_data['cena'])
            Memory.add_product_data = []
            return edit_products(request)
        else:
            # just go back
            return edit_products(request)

    # backend verifies if data is correct (and sets value is_good to 'good', 'bad' or 'no data')
    is_good = request.GET.get('nazwa', 'no data')
    if 'nazwa' in data:
        try:
            float(data['cena'])
            if product_op.get_product_duplicate(data['nazwa']):
                is_good = "bad"
            else:
                is_good = "good"
        except ValueError:
            is_good = 'bad'

    # frontend sets appropriate data
    if is_good == 'good':
        context['confirm'] = 'good'
        context['message'] = "Czy na pewno chcesz dodać produkt?"
        context['params'] = "/panel/edit_products/add_product?confirm=yes"
        Memory.add_product_data = data
    elif is_good == 'bad':
        context['confirm'] = 'bad'
        context['message'] = "Wprowadzone dane są niepoprawne!"

    return render(request, 'server/add_product.html', context)


# 3.1.9 manager_panel/edit_products/remove_checked
# in:
# out: all products
def remove_checked(request):
    data = {}

    # names of products that have been checked
    products = []

    for key in request.GET:
        data[key] = request.GET.get(key, '')
        if data[key] == "true":
            prod = product_op.get_product_by_name(key)
            products.append((prod.name, prod.id, prod.price))

    confirmed = request.GET.get('confirm', '')
    # data has list of product names that have been checked [name, price, code]
    context = {
        'products_list': products
    }

    if confirmed != '':
        for prod in Memory.prods_to_remove:
            prod
            product_op.remove_product(prod[1])

        Memory.prods_to_remove = []
        context['message'] = "Pomyślnie usunięto produkty."
    else:
        Memory.prods_to_remove = products


    return render(request, 'server/remove_checked.html', context)


# 3.1.9 manager_panel/edit_products/remove
# in: id of product to remove
# out: remove product from database, return updated list of products
def remove_from_entry(request):
    codes = request.GET.get('codes', '')
    confirm = request.GET.get('confirm', '')

    context = {}
    parsed_codes = codes.split(",")

    # check data validity
    if confirm == "yes":
        # backend stuff
        for code in Memory.codes_to_remove:
            try:
                prod_id = int(code)
                product_op.remove_product(prod_id)
            except ValueError:
                parsed_codes = []
        Memory.codes_to_remove = []
        return edit_products(request)
    elif confirm == "no":
        # just go back
        return edit_products(request)

    # backend verifies if data is correct (and sets value is_good to 'good', 'bad' or 'no data')
    is_good = request.GET.get('codes', 'no data')
    if len(parsed_codes) > 0 and is_good != 'no data':
        is_good = 'good'
        for code in parsed_codes:
            try:
                prod_id = int(code)
                if not product_op.get_product_by_id(prod_id):
                    is_good = 'bad'
                    break
            except ValueError:
                is_good = 'bad'


    # frontend sets appropriate data
    if is_good == 'good':
        context['confirm'] = 'good'
        context['message'] = "Czy na pewno chcesz usunąć produkty?"
        Memory.codes_to_remove = parsed_codes
    elif is_good == 'bad':
        context['confirm'] = 'bad'
        context['message'] = "Wprowadzone dane są niepoprawne!"

    return render(request, 'server/remove_from_entry.html', context)
