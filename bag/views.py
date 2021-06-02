from django.shortcuts import render, redirect, reverse

# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """
    return render (request, 'bag/bag.html')


def add_to_bag(request, item_id):
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
    
    """
    Add/update the current bag to the session
    """
    request.session['bag'] = bag
    
    # Return user to the same page but with the updated info
    return redirect(redirect_url) 

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
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop[item_id]
    request.session['bag']=bag
    return redirect(reverse('view_bag'))
       