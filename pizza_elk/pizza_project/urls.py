"""pizzeria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pizza_app.views import CustomerAddView, LoginView, HomePageView, LogoutView, MenuView, PizzaCreateView,\
     PizzaDeleteView, ToppingAddView, ToppingView, ToppingEditView, ToppingDeleteView,\
     AddToCartView, AboutUsView, DeletePizzaFromCartView, OrderSummaryView, CheckoutView, OrderView, OrdersView,\
     AdminPageView, CustomerEditView, ContactView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home_page'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('admin_panel/', AdminPageView.as_view(), name='admin'),
    path('customer-add/', CustomerAddView.as_view(), name='customer_add'),
    path('customer-edit/', CustomerEditView.as_view(), name='customer_edit'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('pizza-create/', PizzaCreateView.as_view(), name='pizza_create'),
    path('pizza-delete/', PizzaDeleteView.as_view(), name='pizza_delete'),
    path('toppings/', ToppingView.as_view(), name='toppings'),
    path('topping-add/', ToppingAddView.as_view(), name='topping_add'),
    path('topping-edit/', ToppingEditView.as_view(), name='topping_edit'),
    path('topping-delete/', ToppingDeleteView.as_view(), name='topping_delete'),
    path('cart-pizza-delete/<int:order_pizza_id>/', DeletePizzaFromCartView.as_view(), name='cart'),
    path('cart-create/<str:pizza_name>/', AddToCartView.as_view(), name='cart_create'),
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-details/<int:cart_id>/', OrderView.as_view()),
    path('all-orders/', OrdersView.as_view()),
    path('contact/', ContactView.as_view(), name='contact'),
]
