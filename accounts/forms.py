from django import forms
from django.core.exceptions import ValidationError

from .models import Person, Customer, Vendor


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'address': 'Address',
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['person']
        labels = {
            'person': 'Select Person',
        }

    def clean(self):
        cleaned_data = super().clean()
        person = cleaned_data.get('person')

        if person:
            if hasattr(person, 'vendor'):
                raise ValidationError(
                    f"'{person}' is already registered as a Vendor. "
                    "A person cannot be both a Customer and a Vendor."
                )
            if hasattr(person, 'customer'):
                raise ValidationError(
                    f"'{person}' is already registered as a Customer."
                )

        return cleaned_data


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['person', 'store_name']
        labels = {
            'person': 'Select Person',
            'store_name': 'Store Name',
        }

    def clean(self):
        cleaned_data = super().clean()
        person = cleaned_data.get('person')

        if person:
            if hasattr(person, 'customer'):
                raise ValidationError(
                    f"'{person}' is already registered as a Customer. "
                    "A person cannot be both a Vendor and a Customer."
                )
            if hasattr(person, 'vendor'):
                raise ValidationError(
                    f"'{person}' is already registered as a Vendor."
                )

        return cleaned_data


VendorFullForm = VendorForm
CustomerFullForm = CustomerForm
