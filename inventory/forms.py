from django import forms
from .models import Warehouse, Inventory


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Main Warehouse',
            }),
            'location': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Cebu City, Philippines',
                'rows': 3,
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. 500',
                'min': 0,
            }),
        }
        labels = {
            'name': 'Warehouse Name',
            'location': 'Location',
            'capacity': 'Capacity (units)',
        }


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['warehouse', 'stock_level', 'reorder_threshold']
        widgets = {
            'warehouse': forms.Select(attrs={
                'class': 'form-input',
            }),
            'stock_level': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. 100',
                'min': 0,
            }),
            'reorder_threshold': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. 10',
                'min': 0,
            }),
        }
        labels = {
            'warehouse': 'Warehouse',
            'stock_level': 'Stock Level',
            'reorder_threshold': 'Reorder Threshold',
        }
