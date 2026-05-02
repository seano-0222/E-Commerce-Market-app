from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Review


@login_required
def product_reviews(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.select_related('customer').all()

    # Check if user has already reviewed this product
    user_review = reviews.filter(customer=request.user).first()

    return render(request, 'reviews/review_list.html', {
        'product': product,
        'reviews': reviews,
        'user_review': user_review
    })


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')

        if Review.objects.filter(customer=request.user, product=product).exists():
            messages.error(request, 'You have already reviewed this product.')
            return redirect('reviews:product_reviews', product_id=product_id)

        Review.objects.create(
            rating=rating,
            comment=comment,
            customer=request.user,
            product=product
        )

        messages.success(request, 'Your review has been posted!')
        return redirect('reviews:product_reviews', product_id=product_id)

    return render(request, 'reviews/add_review.html', {'product': product})