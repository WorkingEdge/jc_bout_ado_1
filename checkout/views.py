from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from django.conf import settings
from bag.contexts import bag_contents #Makes the bag_contents() functions available here

import stripe #First need to install it using 'pip3 install stripe'


def checkout(request):
    """
    Set values for stripe public and secret keys. These are from the settings file (imported above) and settings gets them from the environment, set on gitpod settings
    The secret key is used further down for the stripe api key
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    """
    get the current bag from the bag_contents() function. This functions returns a dictionary and the dict has a key of 'grand_total'. This can be used to give the total. For stripe, this needs to be rounded and converted to an integer (*100): 
    """
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total*100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY, 
    )

    

    order_form = OrderForm()
    
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Dis you forget to set it in your environment?')
    
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
