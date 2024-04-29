from django.shortcuts import render

def cart(request):
    content = {}
    return render(request, 'shopping_cart/cart.html', content)
