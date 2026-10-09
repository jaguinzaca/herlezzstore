from django.shortcuts import render
from .models import Product


def catalog_view(request):
    products = Product.objects.filter(is_active=True).order_by('price')
    return render(request, 'products/catalog.html', {'products': products})
