# ecommerce_project/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
from categories.models import Category

@login_required
def index(request):
    context = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'recent_products': Product.objects.order_by('-product_id')[:5],
        'categories': Category.objects.all(),
    }
    return render(request, 'index.html', context)