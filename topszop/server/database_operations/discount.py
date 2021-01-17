import pytz
from django.utils.dateparse import parse_datetime
from server.models import Discount, Discount_Product
from .product import get_product_by_id

def timezone_parse_date(date):
    """Parse date passed in string format to timezone aware date format"""

    naive_date = parse_datetime(date)
    if not naive_date:
        return ""
    return pytz.timezone("Europe/Warsaw").localize(naive_date, is_dst=None)

def is_date_overlapping(date):
    """Check if the date is within other Discount's duration"""

    overlaps = Discount.objects.filter(start_date__lte=date) \
                               .filter(end_date__gte=date)
    return True if overlaps.exists() else False

def contains_other_duration(star_date, end_date):
    """Check if there is another Discount inside this Discount's duration"""

    overlaps = Discount.objects.filter(start_date__gte=star_date) \
                               .filter(end_date__lte=end_date)
    return True if overlaps.exists() else False

def add_discount(start_date, end_date, value, cost):
    """Add discount to database.\n Returns True on success and False on failure"""

    if value < 0 or cost < 0:
        return False

    tz_start = timezone_parse_date(start_date)
    tz_end = timezone_parse_date(end_date)

    if tz_start == "" or tz_end == "":
        return False

    if is_date_overlapping(tz_start) or is_date_overlapping(tz_end):
        return False

    if contains_other_duration(tz_start, tz_end):
        return False

    Discount.objects.create(start_date=tz_start, end_date=tz_end,
                            value=value, cost=cost)

    return True

def get_discount(discount_id):
    """Returns Discount object with given discount_id or None when no match found"""

    try:
        return Discount.objects.get(id__exact=discount_id)
    except Discount.DoesNotExist:
        return None

def add_product_to_discount(product_id, discount_id):
    """Add Product to existing Discount object.\nReturns True on success and False on failure."""

    if not get_discount(discount_id):
        return False

    if not get_product_by_id(product_id):
        return False

    Discount_Product.objects.create(discount_id=discount_id, product_id=product_id)
    return True

def get_discount_data(discount_id):
    """Returns Discount data or None when Discount is not found"""

    disc = get_discount(discount_id)

    if not disc:
        return None

    products = Discount_Product.objects.filter(discount_id__exact=discount_id)
    return {
        'products' : list(products),
        'start_date' : disc.start_date,
        'end_date' : disc.end_date,
        'value' : float(disc.value),
        'cost' : disc.cost
    }
