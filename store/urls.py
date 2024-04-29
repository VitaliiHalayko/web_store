from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.product_page, name='product'),
    path('cart/', views.cart, name='cart')
]