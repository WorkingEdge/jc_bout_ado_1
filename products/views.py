from django.shortcuts import render
from .models import Product #Import the Product model from the models.py module in teh same directory as this

# Create your views here.from django.shortcuts import render


# Create your views here.
def all_products(request):
    """ View to show all products - to include sort and search """

    products = Product.objects.all() # products variable is all objects in the Product model/table. Product is imported from models.py above.

    context = {
        'products': products, # Passing the products to the template
    }
    return render(request, 'products/products.html', context)
