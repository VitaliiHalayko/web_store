from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/<int:quantity>', views.add_to_cart, name='add_to_cart'),
    path('del_from_cart/<int:product_id>', views.del_from_cart, name='del_from_cart'),
    path('change_quantity/<int:product_id>/<int:quantity>', views.change_quantity, name='change_quantity'),
    path('create_order', views.create_order, name='create_order')
]
