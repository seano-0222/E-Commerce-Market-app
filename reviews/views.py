from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from accounts.models import Customer
from .models import Review


@login_required
def product_reviews(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.select_related('customer').all()
    customer = Customer.objects.first()  # TODO: replace with real session customer
    user_review = reviews.filter(customer=customer).first() if customer else None
    return render(request, 'reviews/review_list.html', {
        'product': product,
        'reviews': reviews,
        'user_review': user_review
    })


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    customer = Customer.objects.first()  # TODO: replace with real session customer

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')

        if not customer:
            messages.error(request, 'No customer profile found.')
            return redirect('reviews:product_reviews', product_id=product_id)

        if Review.objects.filter(customer=customer, product=product).exists():
            messages.error(request, 'You have already reviewed this product.')
            return redirect('reviews:product_reviews', product_id=product_id)

        try:
            Review.objects.create(
                rating=rating,
                comment=comment,
                customer=customer,
                product=product
            )
            messages.success(request, 'Your review has been posted!')
        except Exception as e:
            messages.error(request, f'Error posting review: {str(e)}')

        return redirect('reviews:product_reviews', product_id=product_id)

    return render(request, 'reviews/add_review.html', {'product': product})