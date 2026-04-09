"""
Forms for the accounts app.

Each form maps to one registration flow:
    - PersonForm    → /register/person/
    - CustomerForm  → /register/customer/
    - VendorForm    → /register/vendor/

Validation in each form's clean() mirrors the model-level clean() so
that errors are surfaced in the form UI with friendly messages before
the data ever reaches the database.
"""

from django import forms
from django.core.exceptions import ValidationError

from .models import Person, Customer, Vendor


# ---------------------------------------------------------------------------
# PersonForm
# ---------------------------------------------------------------------------

class PersonForm(forms.ModelForm):
    """
    Form for registering a new Person.

    The Person record must be created BEFORE assigning them as a
    Customer or Vendor (the other two forms select an existing Person).
    """

    class Meta:
        model  = Person
        fields = ['first_name', 'last_name', 'email', 'address']
        widgets = {
            # Use a Textarea with fewer rows for address
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name':  'Last Name',
            'email':      'Email Address',
            'address':    'Address',
        }


# ---------------------------------------------------------------------------
# CustomerForm
# ---------------------------------------------------------------------------

class CustomerForm(forms.ModelForm):
    """
    Form for assigning an existing Person as a Customer.

    Validation prevents a Person who is already a Vendor from being
    registered as a Customer (enforcing the exclusive subtype rule).
    """

    class Meta:
        model  = Customer
        fields = ['person']
        labels = {
            'person': 'Select Person',
        }

    def clean(self):
        """
        Enforce the Customer-OR-Vendor exclusivity rule at the form level.

        Checks:
          1. The selected Person is not already a Vendor.
          2. The selected Person is not already a Customer.
        """
        cleaned_data = super().clean()
        person = cleaned_data.get('person')

        if person:
            # Rule: Person cannot be both Customer and Vendor
            if hasattr(person, 'vendor'):
                raise ValidationError(
                    f"'{person}' is already registered as a Vendor. "
                    "A person cannot be both a Customer and a Vendor."
                )
            # Rule: Person cannot be registered as Customer twice
            if hasattr(person, 'customer'):
                raise ValidationError(
                    f"'{person}' is already registered as a Customer."
                )

        return cleaned_data


# ---------------------------------------------------------------------------
# VendorForm
# ---------------------------------------------------------------------------

class VendorForm(forms.ModelForm):
    """
    Form for assigning an existing Person as a Vendor.

    Validation prevents a Person who is already a Customer from being
    registered as a Vendor (enforcing the exclusive subtype rule).
    """

    class Meta:
        model  = Vendor
        fields = ['person', 'store_name']
        labels = {
            'person':     'Select Person',
            'store_name': 'Store Name',
        }

    def clean(self):
        """
        Enforce the Customer-OR-Vendor exclusivity rule at the form level.

        Checks:
          1. The selected Person is not already a Customer.
          2. The selected Person is not already a Vendor.
        """
        cleaned_data = super().clean()
        person = cleaned_data.get('person')

        if person:
            # Rule: Person cannot be both Vendor and Customer
            if hasattr(person, 'customer'):
                raise ValidationError(
                    f"'{person}' is already registered as a Customer. "
                    "A person cannot be both a Vendor and a Customer."
                )
            # Rule: Person cannot be registered as Vendor twice
            if hasattr(person, 'vendor'):
                raise ValidationError(
                    f"'{person}' is already registered as a Vendor."
                )

        return cleaned_data
