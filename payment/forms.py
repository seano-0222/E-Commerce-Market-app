from django import forms
from order.models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['order', 'amount', 'payment_method']