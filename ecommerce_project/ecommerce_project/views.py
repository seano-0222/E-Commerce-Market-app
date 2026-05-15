from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from products.models import Product
from categories.models import Category


@login_required
def index(request):
    # Show ALL products from all vendors on homepage
    total_products = Product.objects.count()
    recent_products = Product.objects.order_by('-product_id')[:5]
    categories = Category.objects.annotate(
        product_count=Count('products')
    )
    total_categories = categories.count()

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'recent_products': recent_products,
        'categories': categories,
    }
    return render(request, 'index.html', context)