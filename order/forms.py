from django import forms
from .models import Order, Platform

class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = ['name', 'description']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'platform', 'status', 'total_amount']