from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Category
from .forms import CategoryForm


@login_required
def category_list(request):
    # Show ALL categories (public view)
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).all()
    return render(request, 'categories/category_list.html', {'categories': categories})


@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'categories/category_detail.html', {'category': category})


def add_category(request):
    # Only superusers/admin can add categories
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators can add categories')
        return redirect('categories:category_list')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('categories:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()

    return render(request, 'categories/addCategory.html', {'form': form})


@login_required
def update_category(request, category_id):
    # Only superusers/admin can update categories
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators can update categories')
        return redirect('categories:category_list')

    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('categories:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'categories/update_category.html', {'form': form, 'category': category})


@login_required
def delete_category(request, category_id):
    # Only superusers/admin can delete categories
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators can delete categories')
        return redirect('categories:category_list')

    category = get_object_or_404(Category, pk=category_id)

    # Check if category has products
    if category.products.count() > 0:
        messages.error(request,
                       f'Cannot delete "{category.name}" because it has {category.products.count()} products. Move or delete the products first.')
        return redirect('categories:category_list')

    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('categories:category_list')

    return render(request, 'categories/delete_category.html', {'category': category})