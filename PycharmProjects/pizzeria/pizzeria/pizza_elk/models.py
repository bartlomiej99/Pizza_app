from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class Topping(models.Model):
    name_topping = models.CharField(max_length=64,  verbose_name="Nazwa składniku")
    price = models.FloatField(verbose_name='Cena składnika')

    def __str__(self):
        return self.name_topping


PIZZA_SIZES = (
    (60, '60cm'),
    (50, '50cm'),
    (40, '40cm'),
    (30, '30cm')
)


class Pizza(models.Model):
    name = models.CharField(max_length=64, verbose_name="Nazwa pizzy")
    size = models.IntegerField(choices=PIZZA_SIZES, verbose_name='Rozmiar pizzy')
    price = models.FloatField(verbose_name='Cena pizzy')
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return f'{self.name} - {self.size} cm'


class Customer(AbstractUser):
    date_of_birth = models.DateField(verbose_name='Data urodzenia', null=True)


class OrderPizza(models.Model):
    pizza_order = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.pizza_order.name

    def get_total_pizza_order_price(self):
        return self.quantity * self.pizza_order.price


DELIVERY = (
    ('t', 'take away'),
    ('d', 'delivery to the house'),
    ('i', 'in the restaurant')
)


class Cart(models.Model):
    pizzas = models.ManyToManyField(OrderPizza)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(default=timezone.now)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.customer.username


class BillingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=128)
    apartment_address = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    additional_information = models.CharField(max_length=128)

    def __str__(self):
        return self.customer.username
