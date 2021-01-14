from server.models import Cart, Cart_Product, Product

def get_all_product_from_cart(cart_id=1):
    """Returns list of all products and their amounts in the cart.
    amounts - list of ints
    products - list of models.Product"""

    products = []
    amounts = []

    cart_products = Cart_Product.objects.filter(cart_id__exact=cart_id)
    for cart_product in cart_products:
        products.append(Product.objects.get(id__exact=cart_product.product_id))
        amounts.append(cart_product.amount)

    return products, amounts

def set_amount_of_product_in_cart(amount, product_id, cart_id=1):
    """Find Cart by cart_id, find Product by product_id and set its amount to amount"""

    Cart_Product.objects.filter(cart_id__exact=cart_id) \
                        .filter(product_id__exact=product_id) \
                        .update(amount=amount)

def add_product_to_cart(amount, product_id, cart_id=1):
    """Add amount of new Product with product_id to Cart with cart_id"""

    Cart_Product.objects.create(cart_id=cart_id, product_id=product_id, amount=amount)

def remove_product_from_cart(product_id, cart_id=1):
    """Remove Cart_Product with matching product_id and cart_id <=> remove Product from Cart"""

    Cart_Product.objects.filter(cart_id__exact=cart_id).filter(product_id__exact=product_id).delete()
