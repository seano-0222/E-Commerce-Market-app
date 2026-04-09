"""
Views for the accounts app.

URL → View mapping:
    /register/person/   → register_person
    /register/customer/ → register_customer
    /register/vendor/   → register_vendor

Each view follows the standard Django POST/GET pattern:
    - GET  → display an empty form
    - POST → validate, save, and redirect (PRG pattern prevents double-submit)
"""

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import PersonForm, CustomerForm, VendorForm


# ---------------------------------------------------------------------------
# View: register_person
# ---------------------------------------------------------------------------

def register_person(request):
    """
    Register a brand-new Person record.

    A Person must exist BEFORE they can be assigned as a Customer or Vendor.
    After a successful registration the user is redirected back to this page
    so they can continue by registering the person as a Customer or Vendor.
    """
    if request.method == 'POST':
        form = PersonForm(request.POST)

        if form.is_valid():
            person = form.save()
            messages.success(
                request,
                f"Person '{person.first_name} {person.last_name}' "
                "was registered successfully. "
                "You can now assign them as a Customer or Vendor."
            )
            # PRG redirect — prevents duplicate submission on browser refresh
            return redirect('register_person')
    else:
        # GET request — show an empty form
        form = PersonForm()

    return render(request, 'accounts/person_register.html', {'form': form})


# ---------------------------------------------------------------------------
# View: register_customer
# ---------------------------------------------------------------------------

def register_customer(request):
    """
    Assign an existing Person as a Customer.

    Validation (in CustomerForm.clean) blocks the action if the selected
    Person is already a Vendor, enforcing the exclusive subtype rule.
    """
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            customer = form.save()
            messages.success(
                request,
                f"'{customer.person}' has been registered as a Customer."
            )
            return redirect('register_customer')
    else:
        form = CustomerForm()

    return render(request, 'accounts/customer_register.html', {'form': form})


# ---------------------------------------------------------------------------
# View: register_vendor
# ---------------------------------------------------------------------------

def register_vendor(request):
    """
    Assign an existing Person as a Vendor.

    Validation (in VendorForm.clean) blocks the action if the selected
    Person is already a Customer, enforcing the exclusive subtype rule.
    """
    if request.method == 'POST':
        form = VendorForm(request.POST)

        if form.is_valid():
            vendor = form.save()
            messages.success(
                request,
                f"'{vendor.person}' has been registered as a Vendor "
                f"with store '{vendor.store_name}'."
            )
            return redirect('register_vendor')
    else:
        form = VendorForm()

    return render(request, 'accounts/vendor_register.html', {'form': form})
