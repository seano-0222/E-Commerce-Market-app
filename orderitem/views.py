from django.shortcuts import render, redirect
from order.models import OrderItem
from .forms import OrderItemForm

def index(request):
    items = OrderItem.objects.all()
    return render(request, 'orderitem_index.html', {'items': items})

def add_new_order_item(request):
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orderitem-index')
    else:
        form = OrderItemForm()
    return render(request, 'addNewOrderItem.html', {'form': form})