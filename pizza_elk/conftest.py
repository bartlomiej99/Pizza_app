import django.contrib.admin.templatetags.admin_modify
import pytest
from django.contrib.auth.models import Permission
from pizza_app.models import Customer, Pizza, OrderPizza, Topping, BillingAddress, Cart
from django.utils import timezone


@pytest.fixture
def test_customer():
    customer = Customer.objects.create_user(username='Blizniak', password='blizniak1', email='oleole@o2.pl',
                                            first_name='Simon', last_name='Kolęda', date_of_birth='2000-08-19')
    return customer


@pytest.fixture
def unauthorized_customer():
    unauthorized_customer = Customer.objects.create_user("Szymon")
    return unauthorized_customer


@pytest.fixture
def auth_customer_add_pizza():
    authorized_customer = Customer.objects.create_user("Bartek")
    perm = Permission.objects.get(codename="add_pizza")
    authorized_customer.user_permissions.add(perm)
    return authorized_customer


@pytest.fixture
def test_topping():
    topping = Topping.objects.create(name_topping='Cheese', price=4)
    return topping


@pytest.fixture
def test_topping2():
    topping = Topping.objects.create(name_topping='Ham', price=7)
    return topping


@pytest.fixture
def auth_cust_delete_pizza():
    authorized_customer = Customer.objects.create_user("Bartek")
    perm = Permission.objects.get(codename="delete_pizza")
    authorized_customer.user_permissions.add(perm)
    return authorized_customer


@pytest.fixture
def auth_cust_add_topping():
    authorized_customer = Customer.objects.create_user("Bartek")
    perm = Permission.objects.get(codename="add_topping")
    authorized_customer.user_permissions.add(perm)
    return authorized_customer


@pytest.fixture
def auth_cust_edit_topping():
    authorized_customer = Customer.objects.create_user("Bartek")
    perm = Permission.objects.get(codename="change_topping")
    authorized_customer.user_permissions.add(perm)
    return authorized_customer


@pytest.fixture
def auth_cust_delete_topping():
    authorized_customer = Customer.objects.create_user("Bartek")
    perm = Permission.objects.get(codename="delete_topping")
    authorized_customer.user_permissions.add(perm)
    return authorized_customer


@pytest.fixture
def test_pizza():
    pizza = Pizza.objects.create(name='Margherita', price=40, size=40)
    return pizza


@pytest.fixture
def test_pizza_order():
    pizza_order = OrderPizza.objects.create(pizza_order=test_pizza)
    return pizza_order


@pytest.fixture
def test_cart():
    cart = Cart.objects.create(pizzas=test_pizza_order, customer=test_customer,
                               ordered=False, ordered_date=timezone.now())
    return cart
