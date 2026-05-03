from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, Platform, OrderItem, Payment, Shipment
from .forms import OrderForm, PlatformForm, OrderItemForm, PaymentForm, ShipmentForm

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def add_new_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/addNewOrder.html', {'form': form})

@login_required
def add_new_platform(request):
    if request.method == 'POST':
        form = PlatformForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = PlatformForm()
    return render(request, 'orders/addNewPlatform.html', {'form': form})

@login_required
def add_new_order_item(request):
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderItemForm()
    return render(request, 'orders/addNewOrderItem.html', {'form': form})

@login_required
def add_new_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = PaymentForm()
    return render(request, 'orders/addNewPayment.html', {'form': form})

@login_required
def add_new_shipment(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = ShipmentForm()
    return render(request, 'orders/addNewShipment.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        return redirect('index')
    return render(request, 'orders/editProfile.html', {'profile_user': request.user})