from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51J0tVwGXFBy9KvEyyA4IB4EpQDGsAaN1IP3rXj4zJRyiTWECYhcjoN4uPmului3nRZ8MdgutiSs2aU2Wy1Ob9iyZ00QlVoIzIB',
        'client_secret': 'test value',
    }

    return render(request, template, context)
