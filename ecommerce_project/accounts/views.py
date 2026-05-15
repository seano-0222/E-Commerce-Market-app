from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model  # Change this import
from products.models import Product, Vendor
from reviews.models import Review

# Get the custom user model
User = get_user_model()


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('accounts:register')

        # Check password length
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return redirect('accounts:register')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('accounts:register')

        # Check if email exists
        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('accounts:register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Make specific username admin (e.g., 'admin' or 'superadmin')
        if username.lower() in ['admin', 'superadmin', 'administrator']:
            user.is_superuser = True
            user.is_staff = True
            user.save()
            messages.info(request, f'✅ {username} registered as ADMIN with vendor privileges')

        # Create vendor profile for all users
        vendor = Vendor.objects.create(
            user=user,
            store_name=f"{username}'s Store",
            vendor_trust_score=5.0 if user.is_superuser else 0.00,  # 5.0 for admins
            bio="",
            contact_number=""
        )

        login(request, user)
        messages.success(request, f'Welcome {username}! Your account has been created.')
        return redirect('index')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('login')


@login_required
def vendor_profile(request):
    # Check if user has a vendor profile
    if not hasattr(request.user, 'vendor'):
        messages.error(request, 'Vendor profile not found')
        return redirect('index')

    # Get ONLY products for the logged-in vendor (for profile page)
    products = Product.objects.filter(vendor__user=request.user)

    # Get reviews for vendor's products
    product_ids = products.values_list('product_id', flat=True)
    reviews = Review.objects.filter(product_id__in=product_ids).select_related('customer', 'product')

    context = {
        'vendor': request.user.vendor,
        'products': products,
        'reviews': reviews,
        'total_products': products.count(),
        'total_reviews': reviews.count(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    if not hasattr(request.user, 'vendor'):
        messages.error(request, 'Vendor profile not found')
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')

        # Check if username is taken (but allow current user)
        if User.objects.exclude(id=request.user.id).filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose another one.')
            return redirect('accounts:edit_profile')

        # Update user
        request.user.username = username
        request.user.name = name
        request.user.email = email
        request.user.save()

        # Update vendor profile
        vendor = request.user.vendor
        vendor.bio = bio
        vendor.contact_number = contact_number
        vendor.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:vendor_profile')

    context = {
        'user': request.user,
        'vendor': request.user.vendor,
    }
    return render(request, 'accounts/edit_profile.html', context)