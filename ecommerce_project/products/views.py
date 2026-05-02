from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Discount
from categories.models import Category
from django.shortcuts import render, redirect
from .forms import ProductForm

@login_required
def product_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def products_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = category.products.all()
    return render(request, 'products/product_list.html', {'products': products, 'category': category})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()

    return render(request, 'products/addNewProduct.html', {'form': form})