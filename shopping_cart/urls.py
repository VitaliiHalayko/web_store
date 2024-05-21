from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/<int:quantity>', views.add_to_cart, name='add_to_cart'),
]
