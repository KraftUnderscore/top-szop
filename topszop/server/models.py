from django.db import models

class Discount(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    value = models.DecimalField(decimal_places=2, max_digits=4)
    cost = models.IntegerField()

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"

class Product(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.CharField(max_length=30)
    name = models.TextField(max_length=255, unique=True)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name

class Discount_Product(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} {self.discount}"

class Cart(models.Model):
    cartID = models.IntegerField()

class Cart_Product(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.amount} of {self.product}"

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField()
    total_cost = models.DecimalField(decimal_places=2, max_digits=10)
    email = models.EmailField()

    def __str__(self):
        return f"Order on {self.order_date} for {self.total_cost}"

class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    delivery_data = models.TextField()

    def __str__(self):
        return f"Delivery: {self.delivery_data}"
