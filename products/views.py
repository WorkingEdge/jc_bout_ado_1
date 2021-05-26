from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q # read the django query docs re 'Q'
from .models import Product, Category #Import the Product and Category model from the models.py module in teh same directory as this

# Create your views here


# Create your views here.
def all_products(request):
    """ View to show all products - to include sort and search """

    products = Product.objects.all() # products variable is all objects in the Product model/table. Product is imported from models.py above.
    query = None # To alow error-free loading of products page without an accompanying search term
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories) #this line works because category and product tables are related
# Initially, products = all the objects in Product model
# With lines above, products becomes a filtered set including products whose category is in 
# the categories variable, which is a list of the categories (name) passed to the view with the request
# based on the nav items setup ({% url 'products' %}?category=shirts)
            categories = Category.objects.filter(name__in=categories) # This line works because we have imported Category model above

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria.")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products, # Passing the products to the template
        'search_term': query,
        'current_categories': categories,
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