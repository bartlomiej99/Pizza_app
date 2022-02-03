from django.core.exceptions import ValidationError
from .models import Customer, Topping, Pizza
import re


def validate_username(username):
    if Customer.objects.filter(username=username):
        raise ValidationError('Podany użytkownik już istnieje!')


def validate_first_name(first_name):
    if first_name != first_name.capitalize():
        raise ValidationError('Podane imię nie może zaczynać się małą literą')


def validate_last_name(last_name):
    if last_name != last_name.capitalize():
        raise ValidationError('Podane nazwisko nie może zaczynać się małą literą')


def validate_topping(name_topping):
    if Topping.objects.filter(name_topping=name_topping):
        raise ValidationError(f'Podany składnik o nazwie {name_topping} już istnieje!')


def validate_existing_pizza(name, size):
    pizza = Pizza.objects.get(name=name, size=size)
    if pizza.exists():
        raise ValidationError('This pizza exists!')
