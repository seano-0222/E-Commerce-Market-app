from django import forms
from order.models import Shipment

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['order', 'shipment_date', 'status', 'delivery_address', 'quantity']