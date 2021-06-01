from django.shortcuts import render, redirect

# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """
    return render (request, 'bag/bag.html')


def add_to_bag(request, item_id):
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    
    """
    Get the bag value from the session object. If there is no bag, create it as empty dict
    """
    bag = request.session.get('bag', {}) # see https://docs.djangoproject.com/en/3.2/topics/http/sessions/
   
    """
    make a list of the keys in the bag dict. 
    If the list contains the required item_id already, add the current quantity to it
    If not, add an element to the dictionary as item_id = quantity
    """
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
    
    """
    Add/update the current bag to the session
    """
    request.session['bag'] = bag
    print(request.session['bag'])
    # Return user to the same page but with the updated info
    return redirect(redirect_url) 