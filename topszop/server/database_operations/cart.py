from server.models import Cart, Cart_Product
from .product import get_product_by_id, get_product_by_name

def add_cart():
    """Adds new Cart to database with incremental ID and the useless cartID is set to 0"""

    Cart.objects.create(cartID=0)

def cart_exist(cart_id):
    try:
        Cart.objects.get(id__exact=cart_id)
        return True
    except Cart.DoesNotExist:
        return False

def get_all_products_from_cart(cart_id=1):
    """Returns list of all products and their amounts in the cart in form of a tuple.
       [(product.name, amount)]"""

    products = []

    cart_products = Cart_Product.objects.filter(cart_id__exact=cart_id)
    for cart_product in cart_products:
        products.append((get_product_by_id(cart_product.product_id).name, cart_product.amount))
    return products

def set_amount_of_product_in_cart(amount, product_name, cart_id=1):
    """Find Cart by cart_id, find Product by product_id and set its amount to amount.
       Returns True on success and False on failure."""

    product = get_product_by_name(product_name)
    if not product:
        return False

    num = Cart_Product.objects.filter(cart_id__exact=cart_id) \
                              .filter(product_id__exact=product.id) \
                              .update(amount=amount)
    return True if num > 0 else False

def add_product_to_cart(amount, product_name, cart_id=1):
    """Add amount of new Product with product_name to Cart with cart_id
       Returns True on success and False on failure."""

    product = get_product_by_name(product_name)
    if not product:
        return False

    try:
        Cart.objects.get(id__exact=cart_id)
    except Cart.DoesNotExist:
        return False

    if Cart_Product.objects.filter(cart_id=cart_id) \
                           .filter(product_id=product.id).exists():
        return False

    Cart_Product.objects.create(cart_id=cart_id, product_id=product.id, amount=amount)

    return True

def remove_product_from_cart_by_name(name, cart_id=1):
    """Remove Cart_Product with matching product name and cart_id <=> remove Product from Cart
       Returns True on success and False on failure."""

    product = get_product_by_name(name)

    if not product:
        return False

    return remove_product_from_cart(product.id, cart_id)

def remove_product_from_cart(product_id, cart_id=1):
    """Remove Cart_Product with matching product_id and cart_id <=> remove Product from Cart
       Returns True on success and False on failure."""

    del_num = Cart_Product.objects.filter(cart_id__exact=cart_id) \
                                  .filter(product_id__exact=product_id).delete()
    return True if del_num[0] > 0 else False

def get_product_from_cart(product_id, cart_id=1):
    """Returns full product and its amount in Cart
       Returns None and amount=0 when product is not in the cart or cart doesn't exist."""
    try:
        cart_product = Cart_Product.objects.filter(cart_id__exact=cart_id) \
                                           .get(product_id__exact=product_id)
        return get_product_by_id(product_id), cart_product.amount
    except Cart_Product.DoesNotExist:
        return None, 0

def clean_cart(cart_id=1):
    """Removed all products from a specified Cart"""

    del_num = Cart_Product.objects.filter(cart_id__exact=cart_id).delete()
    return True if del_num[0] > 0 else False
