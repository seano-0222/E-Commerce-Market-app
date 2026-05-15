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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .forms import PersonForm, CustomerForm, VendorForm, EditPersonForm
from .models import Person


# ---------------------------------------------------------------------------
# View: index
# ---------------------------------------------------------------------------

def index(request):
    """
    Main landing page of the E-Commerce Market project.
    Provides navigation to all app sections.
    """
    return render(request, 'accounts/index.html')


# ---------------------------------------------------------------------------
# View: login_view
# ---------------------------------------------------------------------------

def login_view(request):
    """
    Login page. Authenticates a user using Django's built-in auth system.
    On success, redirects to the index page.
    """
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


# ---------------------------------------------------------------------------
# View: logout_view
# ---------------------------------------------------------------------------

def logout_view(request):
    """Log out the current user and redirect to the login page."""
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def edit_profile(request):
    """Allow a logged-in user to edit their Person profile details."""
    person = Person.objects.filter(email=request.user.email).first()
    if not person:
        messages.error(request, 'No Person profile could be found for your account.')
        return redirect('index')

    if request.method == 'POST':
        form = EditPersonForm(request.POST, instance=person)
        if form.is_valid():
            updated_person = form.save()
            request.user.email = updated_person.email
            request.user.username = updated_person.email
            request.user.first_name = updated_person.first_name
            request.user.last_name = updated_person.last_name
            request.user.save()
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('index')
    else:
        form = EditPersonForm(instance=person)

    return render(request, 'accounts/edit_profile.html', {'form': form})


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
            User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            messages.success(
                request,
                f"Person '{person.first_name} {person.last_name}' was registered successfully. "
                "Please log in with the email address you provided."
            )
            return redirect('login')
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
