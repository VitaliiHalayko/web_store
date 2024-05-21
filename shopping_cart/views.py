from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from store.models import Product
from .models import CartItem


def add_to_cart(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, f'Товар додано до кошика!')

    # Перенаправлення назад на ту ж сторінку
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def cart(request):
    content = {}
    return render(request, 'shopping_cart/cart.html', content)
