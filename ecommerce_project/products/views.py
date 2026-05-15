from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Vendor
from categories.models import Category
from .forms import ProductForm

@login_required
def product_list(request):
    # Show ALL products from ALL vendors (public view)
    products = Product.objects.select_related('category', 'vendor').all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # Anyone can view product details
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def products_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    # Show ALL products in this category from all vendors
    products = category.products.all()
    return render(request, 'products/product_list.html', {'products': products, 'category': category})

@login_required
def add_product(request):
    if not hasattr(request.user, 'vendor'):
        messages.error(request, 'Only vendors can add products')
        return redirect('index')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Check if price is valid
            price = form.cleaned_data.get('price')
            if price <= 0:
                messages.error(request, '⚠️ Price must be greater than 0!')
                return render(request, 'products/addNewProduct.html', {'form': form})

            product = form.save(commit=False)
            # Auto-assign the logged-in vendor
            product.vendor = request.user.vendor
            product.save()
            messages.success(request, '✅ Product added successfully!')
            return redirect('products:product_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    return render(request, 'products/addNewProduct.html', {'form': form})

@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Only the vendor who owns the product can edit it
    if not hasattr(request.user, 'vendor') or product.vendor.user != request.user:
        messages.error(request, 'You don\'t have permission to edit this product')
        return redirect('products:product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            # Check if price is valid
            price = form.cleaned_data.get('price')
            if price <= 0:
                messages.error(request, '⚠️ Price must be greater than 0!')
                return render(request, 'products/update_product.html', {'form': form, 'product': product})

            form.save()
            messages.success(request, '✅ Product updated successfully!')
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/update_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Only the vendor who owns the product can delete it
    if not hasattr(request.user, 'vendor') or product.vendor.user != request.user:
        messages.error(request, 'You don\'t have permission to delete this product')
        return redirect('products:product_list')

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'✅ Product "{product_name}" deleted successfully!')
        return redirect('products:product_list')

    return render(request, 'products/delete_product.html', {'product': product})