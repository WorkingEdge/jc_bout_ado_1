from django.shortcuts import render, redirect, reverse, HttpResponse

from django.contrib import messages

from products.models import Product

# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """
    return render (request, 'bag/bag.html')


def add_to_bag(request, item_id):

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    
    """
    Get the bag value from the session object. If there is no bag, create it as empty dict
    Session variables can be accessed anywhere the request object can be accessed.
    It is a 'readable and writable, dictionary-like object that represents the current session'.
    See: https://docs.djangoproject.com/en/3.2/topics/http/sessions/
    """
    bag = request.session.get('bag', {}) # see https://docs.djangoproject.com/en/3.2/topics/http/sessions/
   
    """Handle sizes"""
    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')
    
    """
    Add/update the current bag to the session
    """
    request.session['bag'] = bag
    
    # Return user to the same page but with the updated info
    return redirect(redirect_url) 
# ----------------------------------------------- Adjust Bag
def adjust_bag(request, item_id):
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    bag = request.session.get('bag', {}) # see https://docs.djangoproject.com/en/3.2/topics/http/sessions/
   
    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)

    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)
    
    request.session['bag']=bag
    return redirect(reverse('view_bag'))

# -------------------------------------------------- Remove from bag
def remove_from_bag(request, item_id):
    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']

        bag = request.session.get('bag', {}) 
        """
        If the bag dict has a size value for this item in the items_by_size dict, delete it
        bag - dict, item_id - key, items_by_size - dict, size - key
        If this means the items_by_size dict is now empty, delete the item from the bag altogether

        If there is no items_by_size dict for this item, remove the item_id (key) from the bag dict
        """
        if size: 
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id) 
        else:
            bag.pop(item_id)

        request.session['bag'] = bag

        return HttpResponse(status=200) # Return 200 to the js function
    except Exception as e:
        return HttpResponse(status=500) # If the try doesn't work, return 500 to the js function  
       