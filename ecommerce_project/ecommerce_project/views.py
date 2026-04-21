# ecommerce_project/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from products.models import Product
from categories.models import Category


@login_required
def index(request):
    # Use 'products' instead of 'product' (plural form)
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).all()

    context = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'recent_products': Product.objects.order_by('-product_id')[:5],
        'categories': categories,
    }
    return render(request, 'index.html', context)