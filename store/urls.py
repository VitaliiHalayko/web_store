from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:category_name>/', views.category_products, name='category_products'),
    path('product/<str:product_name>/', views.product_page, name='product')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)