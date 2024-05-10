from django.shortcuts import render

from categories.models import Category
from store.models import Product


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

def category_products(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'store/index.html', {'products': products})


def product_page(request, product_name):
    product = Product.objects.get(name=product_name)
    return render(request, 'store/product.html', product)


