from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Min, Max
from categories.models import Category
from store.models import Product, Value, Attribute


def index(request):
    """
    View function for the homepage.

    Fetches all products and renders the homepage with the list of products.
    """
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})


def get_filtered_products(data, category):
    """
    Helper function to filter products based on the POST data.
    """
    attributes_values = []

    min_price = data.get('min_price')
    max_price = data.get('max_price')
    sort_option = data.get('sort_option')

    for attribute_name, values in data.lists():
        if attribute_name in ['csrfmiddlewaretoken', 'min_price', 'max_price', 'sort_option'] or not values:
            continue

        value_query = Q()
        for value in values:
            value_query |= Q(value__value=value, value__attribute__name=attribute_name)
        attributes_values.append(value_query)

    products_query = Product.objects.filter(category=category)

    for query in attributes_values:
        products_query = products_query.filter(query)

    if min_price:
        products_query = products_query.filter(price_with_discount__gte=min_price)
    if max_price:
        products_query = products_query.filter(price_with_discount__lte=max_price)

    products_query = products_query.distinct()

    if sort_option == 'price_asc':
        products_query = products_query.order_by('price')
    elif sort_option == 'price_desc':
        products_query = products_query.order_by('-price')
    elif sort_option == 'name_asc':
        products_query = products_query.order_by('name')
    elif sort_option == 'name_desc':
        products_query = products_query.order_by('-name')

    return products_query


def get_attributes_dict(attributes, data):
    """
    Helper function to create a dictionary of attributes and their possible values.
    """
    attributes_dict = {}
    for attribute in attributes:
        values = Value.objects.filter(attribute=attribute).values('value').distinct()
        attribute_values = [
            {'value': value['value'], 'selected': value['value'] in data.getlist(attribute.name, [])}
            for value in values
        ]
        attributes_dict[attribute.name] = attribute_values
    return attributes_dict


def category_products(request, category_name):
    """
    View function for displaying products in a specific category.

    Filters products based on category, price range, attributes, and sort options.
    Handles both GET and POST requests for filtering and sorting.
    """
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)

    attributes = Attribute.objects.filter(is_show=True, category=category)

    prices = products.aggregate(min_price=Min('price_with_discount'), max_price=Max('price_with_discount'))
    min_price, max_price = prices['min_price'], prices['max_price']

    current_min_price, current_max_price = min_price, max_price

    if request.method == 'POST' and len(request.POST) > 1:
        products = get_filtered_products(request.POST, category)
        current_min_price = request.POST.get('min_price', min_price)
        current_max_price = request.POST.get('max_price', max_price)

    attributes_dict = get_attributes_dict(attributes, request.POST)

    return render(request, 'store/index.html', {
        'min_price': min_price,
        'max_price': max_price,
        'current_min_price': current_min_price,
        'current_max_price': current_max_price,
        'products': products,
        'attributes_dict': attributes_dict,
        'current_category': category_name
    })


def product_page(request, product_name):
    """
    View function for displaying a single product page.

    Fetches the product by name and renders the product detail page.
    """
    product = Product.objects.get(name=product_name)
    return render(request, 'store/product.html', {'product': product})
