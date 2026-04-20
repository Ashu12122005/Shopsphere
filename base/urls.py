from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name = 'home'),
    path('addtocart/<int:pk>',addtocart,name='addtocart'),
    path('cart/',cart,name='cart'),
    path('remove/<int:pk>',remove,name='remove'),
    path('add/<int:pk>',add,name='add'),
    path('sub/<int:pk>',sub,name='sub'),
    path("myorders/", my_orders, name="my_orders"),
    path("checkout/", checkout, name="checkout"),
   path("knowus/", knowus, name="knowus"),
   path("support/", support, name="support"),
    path("buy-now/<int:pk>/", buy_now, name="buy_now"),
    path("payment-success/", payment_success, name="payment_success"),
]