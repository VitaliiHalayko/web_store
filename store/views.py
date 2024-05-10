from django.shortcuts import render

from categories.models import Category
from store.models import Product, Value, Attribute


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

def category_products(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    attributes = Attribute.objects.filter(is_show=True)

    attributes_dict = {}
    for attribute in attributes:
        values = Value.objects.filter(attribute=attribute).values('value').distinct()
        attributes_dict[attribute] = values

    min_price = min(products.values_list('price', flat=True))
    max_price = max(products.values_list('price', flat=True))

    return render(request, 'store/index.html', {'min_price': min_price, 'max_price': max_price, 'products': products, 'attributes_dict': attributes_dict})


def product_page(request, product_name):
    product = Product.objects.get(name=product_name)
    return render(request, 'store/product.html', product)


