from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'store/index.html', context)


def product_page(request):
    context = {}
    return render(request, 'store/product.html', context)


