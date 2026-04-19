from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category
from django.shortcuts import render, redirect
from .forms import CategoryForm

@login_required
def category_list(request):
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'categories/category_list.html', {'categories': categories})

@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'categories/category_detail.html', {'category': category})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories:category_list')  # or homepage
    else:
        form = CategoryForm()

    return render(request, 'categories/addCategory.html', {'form': form})