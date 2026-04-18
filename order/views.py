from django.shortcuts import render, redirect
from .models import Order, Platform
from .forms import OrderForm, PlatformForm

def index(request):
    orders = Order.objects.all()
    return render(request, 'index.html', {'orders': orders})

def add_new_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order-index')
    else:
        form = OrderForm()
    return render(request, 'addNewOrder.html', {'form': form})

def add_new_platform(request):
    if request.method == 'POST':
        form = PlatformForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order-index')
    else:
        form = PlatformForm()
    return render(request, 'addNewPlatform.html', {'form': form})