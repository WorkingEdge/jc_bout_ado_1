from django.shortcuts import render, get_object_or_404
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


def product_detail(request, product_id):
    """ View to show single product """
    #get the object with the pk matching passed in product_id from the Product model(table)
    product = get_object_or_404(Product, pk=product_id) 

    context = {
        'product': product, # Passing the product to the template
    }
    return render(request, 'products/product_detail.html', context)