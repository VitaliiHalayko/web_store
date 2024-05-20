from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('popular_items/', views.popular_items, name='popular'),
    path('new/', views.new_arrivals, name='new'),
    path('<str:category_name>/', views.category_products, name='category_products'),
    path('<str:category_name>/<str:product_name>/', views.product_page, name='product')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)