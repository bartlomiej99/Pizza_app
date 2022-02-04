import pytest
from pizza_app.models import Customer, Pizza, Cart, OrderPizza, BillingAddress, Topping
from django.contrib.auth import  authenticate

# Create your tests here.


@pytest.mark.django_db
def test_customer_add(client):
    response = client.post('/customer-add/', {'username': 'wisienka', 'password': 'friend99', 'password1': 'friend99',
                                              'email': 'player@o2.pl', 'first_name': 'Kacper', 'last_name': 'Kozłowski',
                                              'date_of_birth': '2000-02-25'})
    assert Customer.objects.count() == 1


@pytest.mark.django_db
def test_login(client):
    response = client.post('/login/', {'username': 'wisienka', 'password': 'friend99'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_authenticate(client):
    user = authenticate(username='wisienka', password='padawan')
    if user is None:
        response = client.post('/login/', {'username': 'Blizniak', 'password': 'blizniak1'})
        assert response.status_code == 200


@pytest.mark.django_db
def test_customer_edit(client, test_customer):
    client.force_login(test_customer)
    response = client.post('/customer-edit/', {'first_name': 'Kuba', 'last_name': 'Kowalski',
                                               'password': 'padawan1', 'password1': 'padawan1'})
    assert response.status_code == 302


@pytest.mark.django_db
def test_pizza_create_has_perm(client, auth_customer_add_pizza, test_topping, test_topping2):
    client.force_login(auth_customer_add_pizza)
    response = client.post('/pizza-create/', {'name': 'Caciatore', 'price': 25,
                                              'toppings': [test_topping.id, test_topping2.id], 'size': '30cm'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_pizza_create_has_no_perm(client, unauthorized_customer, test_topping, test_topping2):
    client.force_login(unauthorized_customer)
    response = client.post('/pizza-create/', {'name': 'Caciatore', 'price': 25,
                                              'toppings': [test_topping.id, test_topping2.id], 'size': '30cm'})
    assert response.status_code == 403


@pytest.mark.django_db
def test_pizza_delete_has_perm(client, auth_cust_delete_pizza):
    client.force_login(auth_cust_delete_pizza)
    response = client.post('/pizza-delete/', {'name': 'Caciatore'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_pizza_delete_has_no_perm(client, unauthorized_customer):
    client.force_login(unauthorized_customer)
    response = client.post('/pizza-delete/', {'name': 'Caciatore'})
    assert response.status_code == 403


@pytest.mark.django_db
def test_topping_create_has_perm(client, auth_cust_add_topping, test_topping):
    client.force_login(auth_cust_add_topping)
    response = client.post('/topping-add/', {'name_topping': [test_topping.name_topping],
                                             'price': 6})
    assert response.status_code == 200


@pytest.mark.django_db
def test_topping_create_has_no_perm(client, unauthorized_customer, test_topping):
    client.force_login(unauthorized_customer)
    response = client.post('/topping-add/', {'name_topping': [test_topping.name_topping],
                                             'price': 6})
    assert response.status_code == 403


@pytest.mark.django_db
def test_topping_edit_has_perm(client, auth_cust_edit_topping, test_topping2):
    client.force_login(auth_cust_edit_topping)
    response = client.post('/topping-edit/', {'name_topping': [test_topping2.name_topping], 'price': 9})
    assert response.status_code == 200


@pytest.mark.django_db
def test_topping_edit_has_no_perm(client, unauthorized_customer, test_topping2):
    client.force_login(unauthorized_customer)
    response = client.post('/topping-edit/', {'name_topping': [test_topping2.name_topping], 'price': 9})
    assert response.status_code == 403


@pytest.mark.django_db
def test_topping_delete_has_perm(client, auth_cust_delete_topping, test_topping):
    client.force_login(auth_cust_delete_topping)
    response = client.post('/topping-delete/', {'name_topping': [test_topping.name_topping]})
    assert response.status_code == 200


@pytest.mark.django_db
def test_topping_delete_has_no_perm(client, unauthorized_customer, test_topping):
    client.force_login(unauthorized_customer)
    response = client.post('/topping-delete/', {'name_topping': [test_topping.name_topping]})
    assert response.status_code == 403


@pytest.mark.django_db
def test_cart_pizza_add(client, test_customer, test_pizza):
    client.force_login(test_customer)
    response = client.post(f'/cart-create/{test_pizza.name}/', {'size': '40cm'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_checkout_is_authenticated(client, test_customer):
    if test_customer.is_authenticated:
        response = client.post('/checkout/', {'street_address': 'Jana Pawła II 22/7',
                                              'apartment_address': 'Jana Pawła II 22/7',
                                              'phone_number': 609980765, 'additional_information': '7th floor'})

        assert response.status_code == 302


@pytest.mark.django_db
def test_contact(client, test_customer):
    response = client.post('/')