from django.utils import timezone
from django.db.models import Sum
from server.models import Order, Cart_Product, Product
from .cart import cart_exist, get_all_products_from_cart, get_product_by_id

def get_order_data(order_id=1):
    """Returns dictionary with Order's data\n
    'products' -> list of Product objects from Cart\n
    'amounts' -> list of ints indicating Products' amounts in Cart\n
    'order_date' -> date of Order\n
    'total_cost' -> float total cost of Order\n
    'email' -> Order's email"""

    try:
        order = Order.objects.get(id__exact=order_id)
    except Order.DoesNotExist:
        return None

    products = get_all_products_from_cart(order.cart_id)
    return {
        'products' : products[0],
        'amounts' : products[1],
        'order_date' : order.order_date,
        'total_cost' : float(order.total_cost),
        'email' : order.email
    }

def calculate_total_cost(cart_id):
    """Database querry to calculate total cost for Cart with cart_id"""

    total = 0
    cart_products = Cart_Product.objects.filter(cart_id__exact=cart_id)
    for cart_product in cart_products:
        total += cart_product.amount * get_product_by_id(cart_product.product_id).price

    return total

def is_email_valid(email):
    """Validate email using Django's EmailValidator"""

    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def add_order(email, cart_id=1):
    """Adds new order with passed email, sets date to now,
       sums the cost of products in cart.\n
       Returns True on success\n
       Returns False when Cart doesn't exist or
               Cart is empty or
               Email is incorrect"""

    if not is_email_valid(email):
        return False

    if cart_exist(cart_id):
        total = calculate_total_cost(cart_id)
        if total == 0:
            return False

        date = timezone.localtime(timezone.now())
        Order.objects.create(cart_id=cart_id, order_date=date,
                             total_cost=total, email=email)
        return True
    return False
