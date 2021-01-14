from server.models import Product
from django.db import IntegrityError

def get_all_products():
    """Return list of all models.Product from database"""

    return list(Product.objects.all())

def add_product(name, description, price):
    """Adds new Product to database"""

    try:
        Product.objects.create(name=name, description=description, price=price)
        return True
    except IntegrityError:
        return False

def get_product_by_id(product_id):
    """Returns models.Product by matching product_id
       and returns None when no match found"""

    try:
        match = Product.objects.get(id__exact=product_id)
    except Product.DoesNotExist:
        match = None
    return match

def get_product_duplicate(querry):
    """Find product which name matches the querry.
       Returns models.Product of found duplicate"""

    matches = get_products_from_search(querry)
    if len(matches) == 0:
        return None
    return matches[0]

def remove_product(product_id):
    """Delete Product with given id"""

    del_num = Product.objects.filter(id__exact=product_id).delete()
    return True if del_num[0] > 0 else False

def get_products_from_search(querry):
    """Find all Products which names match the querry.
       Returns a list of models.Product"""

    return list(Product.objects.filter(name__icontains=querry))
