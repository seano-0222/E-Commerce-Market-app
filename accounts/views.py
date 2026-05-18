"""
Views for the accounts app.

URL → View mapping:
    /register/person/   → register_person
    /register/customer/ → register_customer
    /register/vendor/   → register_vendor
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
=======
from django.urls import reverse
>>>>>>> 827cfe0f4065836dd040e1de6a34ee991ea04f14

from .forms import PersonForm, CustomerForm, VendorForm


# ---------------------------------------------------------------------------
# View: index (HOME PAGE)
# ---------------------------------------------------------------------------
@login_required
def index(request):
    """
    Main landing page (HOME after login).
    Requires login (session).
    """
    return render(request, "accounts/index.html")


# ---------------------------------------------------------------------------
# View: login_view
# ---------------------------------------------------------------------------
def login_view(request):
    """
    Login page.

    Authenticates a user using Django's built-in auth system.
    On success, redirects to the HOME page.
    """
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)  # ✅ SESSION STARTS HERE
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


# ---------------------------------------------------------------------------
# View: logout_view
# ---------------------------------------------------------------------------
def logout_view(request):
    """Log out the current user and redirect to the login page."""
    logout(request)  # ✅ SESSION ENDS HERE
    return redirect("login")


# ---------------------------------------------------------------------------
# NEW: edit_profile
# ---------------------------------------------------------------------------
@login_required
def edit_profile(request):
    return render(request, "accounts/edit_profile.html")


# ---------------------------------------------------------------------------
# NEW: add_record
# ---------------------------------------------------------------------------
@login_required
def add_record(request):
    return render(request, "accounts/add_record.html")


# ---------------------------------------------------------------------------
# View: register_person
# ---------------------------------------------------------------------------
@login_required
def register_person(request):
<<<<<<< HEAD
    if request.method == "POST":
=======
    """
    Register a brand-new Person record.

    A Person must exist BEFORE they can be assigned as a Customer or Vendor.
    After a successful registration the user is redirected back to this page
    so they can continue by registering the person as a Customer or Vendor.
    """

    if request.method == 'POST':
>>>>>>> 827cfe0f4065836dd040e1de6a34ee991ea04f14
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            messages.success(
                request,
<<<<<<< HEAD
                f"Person '{person.first_name} {person.last_name}' "
                "was registered successfully. "
                "You can now assign them as a Customer or Vendor.",
            )
            return redirect("register_person")
    else:
        form = PersonForm()

    return render(request, "accounts/person_register.html", {"form": form})
=======
                f"Person '{person.first_name} {person.last_name}' registered! "
                "Now assign them as a Customer or Vendor."
            )
            # Redirect to customer registration with person pre-selected
            return redirect(
                reverse('register_customer') + f'?person={person.person_id}'
            )
    else:
        form = PersonForm()
    return render(request, 'accounts/person_register.html', {'form': form})
>>>>>>> 827cfe0f4065836dd040e1de6a34ee991ea04f14


# ---------------------------------------------------------------------------
# View: register_customer
# ---------------------------------------------------------------------------
@login_required
def register_customer(request):
<<<<<<< HEAD
    if request.method == "POST":
=======
    """
    Assign an existing Person as a Customer.

    Validation (in CustomerForm.clean) blocks the action if the selected
    Person is already a Vendor, enforcing the exclusive subtype rule.
    """

    if request.method == 'POST':
>>>>>>> 827cfe0f4065836dd040e1de6a34ee991ea04f14
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(
                request,
                f"'{customer.person}' has been registered as a Customer.",
            )
<<<<<<< HEAD
            return redirect("register_customer")
=======
            return redirect('login')
>>>>>>> 827cfe0f4065836dd040e1de6a34ee991ea04f14
    else:
        initial = {}
        person_id = request.GET.get('person')
        if person_id:
            initial['person'] = person_id
        form = CustomerForm(initial=initial)

    return render(request, "accounts/customer_register.html", {"form": form})


# ---------------------------------------------------------------------------
# View: register_vendor
# ---------------------------------------------------------------------------
@login_required
def register_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save()
            messages.success(
                request,
                f"'{vendor.person}' has been registered as a Vendor "
                f"with store '{vendor.store_name}'.",
            )
<<<<<<< HEAD
            return redirect("register_vendor")
    else:
        form = VendorForm()

    return render(request, "accounts/vendor_register.html", {"form": form})
=======
            return redirect('login')  # done — send them to login
    else:
        initial = {}
        person_id = request.GET.get('person')
        if person_id:
            initial['person'] = person_id
        form = VendorForm(initial=initial)
    return render(request, 'accounts/vendor_register.html', {'form': form})
>>>>>>> 827cfe0f4065836dd040e1de6a34ee991ea04f14
