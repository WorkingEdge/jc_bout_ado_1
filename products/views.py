from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q # read the django query docs re 'Q'
from django.db.models.functions import Lower #Needed to lower case the name in all_products(request)
from .models import Product, Category #Import the Product and Category model from the models.py module in teh same directory as this
from .forms import ProductForm

# Create your views here


# Create your views here.
def all_products(request):
    """ View to show all products - to include sort and search """

    products = Product.objects.all() # products variable is all objects in the Product model/table. Product is imported from models.py above.
    query = None # To alow error-free loading of products page without an accompanying search term
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey) # order_by() is a django method: https://docs.djangoproject.com/en/3.2/ref/models/querysets/


        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories) # this line works because category and product tables are related
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

    current_sorting = f'{sort}_{direction}'
    context = {
        'products': products, # Passing the products to the template
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting
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


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid:
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, f'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))