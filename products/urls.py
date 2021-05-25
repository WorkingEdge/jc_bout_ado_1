from django.urls import path
from . import views

# urls below need to be included in urls.py at project level
urlpatterns = [
    path('', views.all_products, name='products')
]