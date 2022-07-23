from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There is nothing in your bag")
        return redirect (reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51L2hGJKW8hjxRzk2U8TUMAQ47r3qkGjCGie8h50YzmmKQfIIZhcOZJWzpo1BT7FpsN7oGeGHz2ALfjIq07WG9Sz9009T9Im3gI',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)