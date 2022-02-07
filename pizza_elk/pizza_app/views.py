from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Pizza, Customer, Cart, Topping, OrderPizza, BillingAddress
from .forms import CustomerAddForm, LoginForm, PizzaCreateForm, PizzaDeleteForm, ToppingAddForm,\
    ToppingEditForm, ToppingDeleteForm, AddToCartForm, CheckoutForm, ContactForm, CustomerEditForm
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
# Create your views here.


class HomePageView(View):
    """ Home page shows all the links to different views """
    def get(self, request):
        time = timezone.now()
        return render(request, 'base.html', {'time': time})


class AdminPageView(LoginRequiredMixin, View):
    """ Admin panel shows up if the person is logged in as admin. The View shows admin panel page"""
    def get(self, request):
        if request.user.is_superuser:
            return render(request, 'admin.html')
        else:
            return render(request, '403.html')


class AboutUsView(View):
    """ About us page shows all the information about the pizza place and how is it done in polish language"""
    def get(self, request):
        return render(request, 'about_us.html')


class CustomerAddView(View):
    """ After entering the site by method GET shows empty registration form,
     after entering the method POST form saves and sends information to the database if it is correct"""
    def get(self, request):
        form = CustomerAddForm()
        return render(request, 'add_customer.html', {'form': form})

    def post(self, request):
        form = CustomerAddForm(request.POST)
        if form.is_valid():
            try:
                Customer.objects.create_user(username=form.cleaned_data['username'],
                                             password=form.cleaned_data['password'],
                                             email=form.cleaned_data['email'],
                                             first_name=form.cleaned_data['first_name'],
                                             last_name=form.cleaned_data['last_name'],
                                             date_of_birth=form.cleaned_data['date_of_birth'])
                return redirect('/login/')
            except IntegrityError:
                return render(request, 'add_customer.html', {'form': form,
                                                             'info': 'Użytkownik o podanym loginie istnieje!'})
            except KeyError:
                return render(request, 'add_customer.html', {'form': form,
                                                             'info': 'Given password is invalid!'})
        else:
            return render(request, 'add_customer.html', {'form': form, 'info': 'Wypełnij poprawnie wszystkie pola!'})


class LoginView(View):
    """ After entering the login site by method GET shows empty form
     and method POST sends information and if the data is correct logs the user on page"""
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form, 'info': 'Błędny login lub hasło!'})
        else:
            return render(request, 'login.html', {'form': form, 'info': 'Wypełnij poprawnie formularz!'})


class LogoutView(LoginRequiredMixin, View):
    """ Method GET logs out current user"""
    def get(self, request):
        logout(request)
        return redirect('/')


class CustomerEditView(LoginRequiredMixin, View):
    """ Method GET shows empty form
    and method POST gets current login user by id,
    changes all the information that user wants to change and then saves it also redirects user to login again"""
    def get(self, request):
        form = CustomerEditForm()
        return render(request, 'customer_edit.html', {'form': form})

    def post(self, request):
        form = CustomerEditForm(request.POST)
        if form.is_valid():
            user = request.user
            customer = Customer.objects.get(id=user.id)
            customer.first_name = form.cleaned_data['first_name']
            customer.last_name = form.cleaned_data['last_name']
            customer.set_password(form.cleaned_data['password'])
            customer.save()
            return redirect('/login/')
        else:
            return render(request, 'customer_edit.html', {'info': 'Make sure you pass values correctly, try again!'})


class MenuView(View):
    """ Menu View get all the pizzas from the database """
    def get(self, request):
        pizza = Pizza.objects.filter(size=30).order_by('id')
        pizzas = Pizza.objects.all().order_by('id')
        return render(request, 'menu.html', {'pizza': pizza, 'pizzas': pizzas})


class PizzaCreateView(PermissionRequiredMixin, View):
    """ Permission is needed to enter this site method GET shows empty pizza create form,
    method POST create new pizza and saves all information to database """
    permission_required = 'pizza_app.add_pizza'
    permission_denied_message = 'You have not permission to create new pizza!'

    def get(self, request):
        form = PizzaCreateForm()
        return render(request, 'pizza_create.html', {'form': form})

    def post(self, request):
        form = PizzaCreateForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.has_perm('pizza_app.add_pizza'):
                pizza = Pizza.objects.create(name=form.cleaned_data['name'],
                                             price=form.cleaned_data['price'],
                                             size=form.cleaned_data['size'])
                topping = form.cleaned_data['toppings']
                pizza.toppings.set(topping)
                return redirect('/menu/')
        else:
            return render(request, 'pizza_create.html', {'form': form})


class PizzaDeleteView(PermissionRequiredMixin, View):
    """ If user has permissions, by method GET he will see empty pizza delete form,
    after entering POST method pizza will be deleted from the database """
    permission_required = 'pizza_app.delete_pizza'
    permission_denied_message = "You haven't got permission to delete existing pizza!"

    def get(self, request):
        form = PizzaDeleteForm()
        return render(request, 'pizza_delete.html', {'form': form})

    def post(self, request):
        form = PizzaDeleteForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.has_perm('pizza_app.delete_pizza'):
                pizza = Pizza.objects.filter(name=form.cleaned_data['name'])
                pizza.delete()
                return redirect('/menu/')
            else:
                return render(request, 'pizza_delete.html', {'form': form})
        else:
            return render(request, 'pizza_delete.html', {'form': form, 'info': 'Wypełnij poprawnie formularz!'})


class ToppingView(LoginRequiredMixin, View):
    """ To enter by method GET user has to be superuser and the VIew shows all toppings """
    def get(self, request):
        if request.user.is_superuser:
            toppings = Topping.objects.all().order_by('name_topping')
            return render(request, 'toppings.html', {'toppings': toppings})
        else:
            return render(request, '403.html')


class ToppingAddView(PermissionRequiredMixin, View):
    """ Only user with permission can see this View, method GET shows empty form,
    method POST create new topping only if user has permission to create new topping """
    permission_required = 'pizza_app.add_topping'
    permission_denied_message = "You haven't got permission to add new topping!"

    def get(self, request):
        form = ToppingAddForm()
        return render(request, 'topping_add.html', {'form': form})

    def post(self, request):
        form = ToppingAddForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.has_perm('pizza_app.add_topping'):
                Topping.objects.create(name_topping=form.cleaned_data['name_topping'], price=form.cleaned_data['price'])
                return redirect('/toppings/')
            else:
                return render(request, 'topping_add.html', {'form': form})
        else:
            return render(request, 'topping_add.html', {'form': form, 'info': 'Wypełnij poprawnie formularz!'})


class ToppingEditView(PermissionRequiredMixin, View):
    """ Only user with permission can see this View, method GET shows empty form,
    method POST edit topping that user choose only if user has permission to edit topping """
    permission_required = 'pizza_app.change_topping'
    permission_denied_message = "You haven't got permission to edit toppings!"

    def get(self, request):
        form = ToppingEditForm()
        return render(request, 'topping_edit.html', {'form': form})

    def post(self, request):
        form = ToppingEditForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.has_perm('pizza_app.change_topping'):
                topping = Topping.objects.get(name_topping=form.cleaned_data['name_topping'])
                topping.price = form.cleaned_data['price']
                topping.save()
                return redirect('/toppings/')
            else:
                return render(request, 'topping_edit.html', {'form': form})
        else:
            return render(request, 'topping_edit.html', {'form': form, 'info': 'Wypełnij poprawnie formularz!'})


class ToppingDeleteView(PermissionRequiredMixin, View):
    """ Only user with permission can see this View, method GET shows empty form,
        method POST delete topping only if user has permission to delete topping """
    permission_required = 'pizza_app.delete_topping'
    permission_denied_message = "You haven't got permission to delete topping!"

    def get(self, request):
        form = ToppingDeleteForm()
        return render(request, 'topping_delete.html', {'form': form})

    def post(self, request):
        form = ToppingDeleteForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.has_perm('pizza_app.delete_topping'):
                topping = Topping.objects.filter(name_topping=form.cleaned_data['name_topping'])
                topping.delete()
                return redirect('/toppings/')
            else:
                return render(request, 'topping_delete.html', {'form': form})
        else:
            return render(request, 'topping_delete.html', {'form': form})


class DeletePizzaFromCartView(LoginRequiredMixin, View):
    """ Only logged user is able to see this page, if user click on "X" in cart than it deletes pizza from his cart"""
    def get(self, request, order_pizza_id):
        user = request.user
        pizza = get_object_or_404(Pizza, id=order_pizza_id)
        cart_qs = Cart.objects.filter(customer=user, ordered=False)
        if cart_qs.exists():
            cart = cart_qs[0]
            if cart.pizzas.filter(pizza_order=order_pizza_id).exists():
                pizza_order = OrderPizza.objects.filter(
                    pizza_order=pizza,
                    customer=user,
                    ordered=False
                )[0]
                pizza_order.quantity = 1
                cart.pizzas.remove(pizza_order)
                pizza_order.save()
                return redirect('/order-summary/')
            else:
                return redirect(request, '/order-summary/', {'info': 'You do not have an order!'})
        else:
            return redirect(request, '/order-summary/', {'info': 'You do not have an active order!'})


class AddToCartView(LoginRequiredMixin, View):
    """ Method GET shows empty form and method POST saves information, create OrderPizza object, filter through carts,
    and find cart that is current user log in than add it to the cart and redirects to order summary"""
    def get(self, request, pizza_name):
        form = AddToCartForm()
        pizza = Pizza.objects.filter(name=pizza_name, size=30)
        return render(request, 'cart_add.html', {'pizza': pizza, 'form': form})

    def post(self, request, pizza_name):
        form = AddToCartForm(request.POST)
        if form.is_valid():
            user = request.user
            pizza = get_object_or_404(Pizza, name=pizza_name, size=form.cleaned_data['size'])
            pizza_order, created = OrderPizza.objects.get_or_create(
                pizza_order=pizza,
                customer=user,
                ordered=False
            )
            cart_qs = Cart.objects.filter(customer=user, ordered=False)
            if cart_qs.exists():
                cart = cart_qs[0]
                if cart.pizzas.filter(pizza_order=pizza.id).exists():
                    pizza_order.quantity += 1
                    pizza_order.save()
                    return redirect('/order-summary/')
                else:
                    cart.pizzas.add(pizza_order)
            else:
                order_date = timezone.now()
                cart = Cart.objects.create(customer=user, ordered_date=order_date)
                cart.pizzas.add(pizza_order)
            return redirect('/order-summary/')
        else:
            return render(request, 'cart_add.html', {'form': form})


class OrderSummaryView(LoginRequiredMixin, View):
    """ This View filter through carts and find current user log in cart show all the information about order"""
    def get(self, request):
        try:
            cart = Cart.objects.get(customer=request.user, ordered=False)
            total = 0
            for p in cart.pizzas.all():
                total += p.pizza_order.price * p.quantity
        except ObjectDoesNotExist:
            pizza = Pizza.objects.filter(size=30).order_by('id')
            pizzas = Pizza.objects.all().order_by('id')
            return render(request, 'menu.html', {'info':
                                                 'You have nothing in your cart please add pizza to create your cart!',
                                                 'pizza': pizza, 'pizzas': pizzas})
        return render(request, 'order_summary.html', {'cart': cart, 'total': total})


class CheckoutView(LoginRequiredMixin, View):
    """ Method GET show empty form and show cart with all pizzas,
    method POST saves information from form,
    create BillingAddress object and saves it to current user,
    than sends all the info about order to pizza site email"""
    def get(self, request):
        form = CheckoutForm()
        cart = Cart.objects.get(customer=request.user, ordered=False)
        total = 0
        for p in cart.pizzas.all():
            total += p.pizza_order.price * p.quantity
        return render(request, 'checkout.html', {'form': form, 'cart': cart, 'total': total})

    def post(self, request):
        form = CheckoutForm(request.POST)
        try:
            cart = Cart.objects.get(customer=request.user, ordered=False)
            if form.is_valid():
                total = 0
                for p in cart.pizzas.all():
                    total += p.pizza_order.price * p.quantity
                user = request.user
                street_address = form.cleaned_data['street_address']
                apartment_address = form.cleaned_data['apartment_address']
                phone_number = form.cleaned_data['phone_number']
                additional_information = form.cleaned_data['additional_information']
                billing_address = BillingAddress(
                    customer=user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    phone_number=phone_number,
                    additional_information=additional_information,
                )
                billing_address.save()
                cart.billing_address = billing_address
                cart.save()
                html_content = render_to_string('order.html', {
                     'user': user,
                     'cart': cart,
                     'total': total,
                 })
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    'New Order',
                    text_content,
                    user.email,
                    ['nerf0@o2.pl'],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return redirect(f'/order-details/{cart.id}/')
        except ObjectDoesNotExist:
            return redirect(request, '/')


class OrdersView(PermissionRequiredMixin, LoginRequiredMixin, View):
    """ Only user that has permission can see this View, page shows all orders created """
    permission_required = 'pizza_app.view_cart'
    permission_denied_message = "You don't have permission to see orders!"

    def get(self, request):
        user = request.user
        if user.has_perm('pizza_app.view_cart'):
            cart = Cart.objects.all().order_by('id')
            return render(request, 'all_orders.html', {'cart': cart})


class OrderView(LoginRequiredMixin, View):
    """ View shows details about order """
    def get(self, request, cart_id):
        cart = Cart.objects.get(id=cart_id)
        total = 0
        for p in cart.pizzas.all():
            total += p.pizza_order.price * p.quantity
        return render(request, 'order_details.html', {'cart': cart, 'total': total})


class ContactView(View):
    """ Method GET show empty contact form, method POST saves info to html content and sends it to pizza email site """
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            html_content = render_to_string('contact.html', {
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            })
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                f"{form.cleaned_data['subject']}",
                text_content,
                form.cleaned_data['email'],
                ['nerf0@o2.pl'],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            return redirect('/')
        else:
            return render(request, 'contact.html', {'info': 'Something went wrong try again!'})
