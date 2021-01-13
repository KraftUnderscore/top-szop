from server.models import Product

def get_all_products():
    pass

def add_product():
    pass

def get_product():
    pass

def get_duplicate():
    pass

def remove_product():
    pass

def get_product_from_search(querry):
    """Find all Products which names match the querry. Returns a list of models.Product"""

    return list(Product.objects.filter(name__icontains=querry))
