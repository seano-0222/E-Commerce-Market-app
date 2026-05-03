from django import forms
from .models import Order, Platform, OrderItem, Payment, Shipment

ORDER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
    ('Refunded', 'Refunded'),
]

PAYMENT_METHOD_CHOICES = [
    ('Cash', 'Cash'),
    ('GCash', 'GCash'),
    ('Bank Transfer', 'Bank Transfer'),
    ('Credit Card', 'Credit Card'),
    ('PayMaya', 'PayMaya'),
]

SHIPMENT_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
    ('Failed', 'Failed'),
    ('Returned', 'Returned'),
]

class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = ['name', 'description']

class OrderForm(forms.ModelForm):
    status = forms.ChoiceField(choices=ORDER_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Order
        fields = ['customer', 'platform', 'status', 'total_amount']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']

class PaymentForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Payment
        fields = ['order', 'amount', 'payment_method']

class ShipmentForm(forms.ModelForm):
    status = forms.ChoiceField(choices=SHIPMENT_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    shipment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Shipment
        fields = ['order', 'shipment_date', 'status', 'delivery_address', 'quantity']