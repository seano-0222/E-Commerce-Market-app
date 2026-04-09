from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category

@login_required
def category_list(request):
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'categories/category_list.html', {'categories': categories})

@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'categories/category_detail.html', {'category': category})