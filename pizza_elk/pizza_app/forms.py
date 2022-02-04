import django.forms as forms
from django.core.validators import EmailValidator, ValidationError
from .validators import validate_username, validate_first_name, validate_last_name, validate_topping
from .models import Pizza, Topping, PIZZA_SIZES


class CustomerAddForm(forms.Form):
    username = forms.CharField(validators=[validate_username], label='Login')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Repeat Password')
    first_name = forms.CharField(validators=[validate_first_name], label='Name')
    last_name = forms.CharField(validators=[validate_last_name], label='Surname')
    email = forms.CharField(validators=[EmailValidator()], label='Email')
    date_of_birth = forms.DateField(label='Date of birth')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password1']:
            raise ValidationError('Password is not the same!')
        else:
            return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label='Login')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')


class CustomerEditForm(forms.Form):
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Surname')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Repeat password')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password1']:
            raise ValidationError('Hasło nie jest takie same!')
        else:
            return cleaned_data


class PizzaCreateForm(forms.Form):
    name = forms.CharField(max_length=64, label='Pizza name')
    price = forms.FloatField(label='Pizza price')
    toppings = forms.ModelMultipleChoiceField(queryset=Topping.objects.all(), label='Toppings')
    size = forms.ChoiceField(choices=PIZZA_SIZES, label='Pizza size')


class PizzaDeleteForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Pizza.objects.all(), label='Pizza name')


class ToppingAddForm(forms.Form):
    name_topping = forms.CharField(validators=[validate_topping], max_length=64, label='Nazwa składnika')
    price = forms.FloatField(label='Cena składnika')


class ToppingEditForm(forms.Form):
    name_topping = forms.ModelChoiceField(queryset=Topping.objects.all(), label='Skladnik')
    price = forms.FloatField(label='Cena składnika')


class ToppingDeleteForm(forms.Form):
    name_topping = forms.ModelChoiceField(queryset=Topping.objects.all(), label='Skladnik')


class AddToCartForm(forms.Form):
    size = forms.ChoiceField(choices=PIZZA_SIZES)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(max_length=128)
    apartment_address = forms.CharField(max_length=128, required=False)
    phone_number = forms.IntegerField()
    additional_information = forms.CharField(widget=forms.Textarea(), max_length=128, required=False)


class ContactForm(forms.Form):
    email = forms.CharField(validators=[EmailValidator()], label='Email')
    subject = forms.CharField(max_length=64, label='Subject')
    message = forms.CharField(widget=forms.Textarea(), label='Message')
