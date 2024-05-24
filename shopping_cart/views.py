from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from store.models import Product
from .models import CartItem, Order, OrderItem


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


def del_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key

    CartItem.objects.filter(session_key=session_key, product=product).delete()
    items = CartItem.objects.filter(session_key=session_key)

    # Перенаправлення назад на ту ж сторінку
    return render(request, 'shopping_cart/cart.html', context={
        'items': items,
        'count': len(items),
        'total_sum_without_sales': sum(items)[0],
        'total_sum_with_sales': sum(items)[1]
    })


def change_quantity(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key

    if quantity > 0:
        CartItem.objects.filter(session_key=session_key, product=product).update(quantity=quantity)
    items = CartItem.objects.filter(session_key=session_key)

    return render(request, 'shopping_cart/cart.html', context={
        'items': items,
        'count': len(items),
        'total_sum_without_sales': sum(items)[0],
        'total_sum_with_sales': sum(items)[1]
    })


def create_order(request, lastName, firstName, email, city, address, postal):
    session_key = request.session.session_key
    items = CartItem.objects.filter(session_key=session_key)

    if len(items) == 0:
        messages.info(request, 'Ваша корзина пуста')
        return render(request, 'shopping_cart/cart.html', context={
        'items': items,
        'count': len(items),
        'total_sum_without_sales': sum(items)[0],
        'total_sum_with_sales': sum(items)[1]
    })

    order = Order.objects.create(
        last_name=lastName,
        first_name=firstName,
        email=email,
        city=city,
        address=address,
        postal_code=postal,
        amount=sum(items)[1]
    )

    items_list_from_email = ''

    for item in items:
        OrderItem.objects.create(
            product=item.product,
            order=order,
            quantity=item.quantity
        )

        items_list_from_email = items_list_from_email + str(item.product.name) + ': ' + str(item.product.price) + '\n'

    CartItem.objects.filter(session_key=session_key).delete()
    items = CartItem.objects.filter(session_key=session_key)

    messages.success(request, f'Замовлення створене! Очікуйте повідомлення на вказану пошту.')

    email_message = f'{lastName} {firstName}, ваше замовлення {order.id} створене на оброблене і вже прямує по адресу: {city} {address} {postal}. Список товарів: \n {items_list_from_email} Номер накладної ------'

    send_mail(
        'Магазин аксесуарів для ПК',
        email_message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )

    return render(request, 'shopping_cart/cart.html', context={
        'items': items,
        'count': len(items),
        'total_sum_without_sales': sum(items)[0],
        'total_sum_with_sales': sum(items)[1]
    })


def sum(items):
    total_sum_without_sales = 0
    total_sum_with_sales = 0

    for item in items:
        total_sum_without_sales += item.product.price * item.quantity
        if item.product.price_with_discount < item.product.price:
            total_sum_with_sales += item.product.price_with_discount * item.quantity
        else:
            total_sum_with_sales += item.product.price * item.quantity

    return total_sum_without_sales, total_sum_with_sales


def cart(request):
    items = CartItem.objects.filter(session_key=request.session.session_key)

    return render(request, 'shopping_cart/cart.html', context={
        'items': items,
        'count': len(items),
        'total_sum_without_sales': sum(items)[0],
        'total_sum_with_sales': sum(items)[1]
    })
