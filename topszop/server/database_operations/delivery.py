from server.models import Delivery, Order
from .order import get_order_data

def add_delivery(order_id, delivery_data):
    """Add new Delivery.\n Returns True on success and False on failure."""

    order = Order.objects.filter(id__exact=order_id)
    if not order:
        return False

    Delivery.objects.create(order_id=order_id, delivery_data=delivery_data)
    return True

def get_delivery_data(delivery_id):
    """Get delivery data.\n
       Returns tuple order_data (dictionary, same as in get_order_data() in order.py),
       delivery_data (address) on success\n
       Returns None, None on failure."""

    try:
        delivery = Delivery.objects.get(id__exact=delivery_id)
    except Delivery.DoesNotExist:
        return None, None

    order_data = get_order_data(delivery.order_id)
    return order_data, delivery.delivery_data
