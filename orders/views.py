from django.shortcuts import render, get_object_or_404
from .models import Order, Platform
from accounts.models import Customer


def order_list(request):
    customer = Customer.objects.first()  # TODO: replace with actual auth
    orders = Order.objects.filter(customer=customer).select_related('platform') if customer else []
    return render(request, 'orders/order_list.html', {'orders': orders, 'customer': customer})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})
