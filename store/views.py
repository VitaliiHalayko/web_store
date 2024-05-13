from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from categories.models import Category
from store.models import Product, Value, Attribute


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})


def category_products(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category).all()
    attributes = Attribute.objects.filter(is_show=True, category=category)

    min_price = min(products.values_list('price', flat=True))
    max_price = max(products.values_list('price', flat=True))

    if request.method == 'POST' and len(request.POST) > 1:
        data = request.POST

        attributes_values = []

        min_price = data.get('min_price')
        max_price = data.get('max_price')

        sort_option = data.get('sort_option')

        for attribute_name, values in data.lists():
            if attribute_name == 'csrfmiddlewaretoken' or attribute_name == 'min_price' or attribute_name == 'max_price' or attribute_name == 'sort_option' or not values:
                continue

            value_query = Q()

            for value in values:
                value_query |= Q(value__value=value, value__attribute__name=attribute_name)

            attributes_values.append(value_query)

        products_query = Product.objects.all()

        for query in attributes_values:
            products_query = products_query.filter(query)

        if min_price is not None:
            products_query = products_query.filter(price__gte=min_price)

        if max_price is not None:
            products_query = products_query.filter(price__lte=max_price)

        products = products_query.distinct()

        if sort_option == 'price_asc':
            products = products.order_by('price')
        elif sort_option == 'price_desc':
            products = products.order_by('-price')
        elif sort_option == 'name_asc':
            products = products.order_by('name')
        elif sort_option == 'name_desc':
            products = products.order_by('-name')

    attributes_dict = {}
    for attribute in attributes:
        values = Value.objects.filter(attribute=attribute).values('value').distinct()
        attribute_values = []
        for value in values:
            value_obj = {'value': value['value']}
            # Check if the value is selected based on the POST data
            if value['value'] in request.POST.getlist(attribute.name, []):
                value_obj['selected'] = True
            else:
                value_obj['selected'] = False
            attribute_values.append(value_obj)
        attributes_dict[attribute.name] = attribute_values


    return render(request, 'store/index.html', {
        'min_price': min_price,
        'max_price': max_price,
        'products': products,
        'attributes_dict': attributes_dict,
        'current_category': category_name
    })


def product_page(request, product_name):
    product = Product.objects.get(name=product_name)
    return render(request, 'store/product.html', product)
