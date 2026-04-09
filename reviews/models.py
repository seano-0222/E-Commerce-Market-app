from django.db import models
from django.core.exceptions import ValidationError
# Uses accounts.Customer (Person-based identity system, not Django default User)
from accounts.models import Customer
from products.models import Product


class Review(models.Model):
    review_id   = models.AutoField(primary_key=True)
    rating      = models.IntegerField()
    comment     = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    # ForeignKey to accounts.Customer - matches ERD: Customer -> Review (1:M)
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    product     = models.ForeignKey(Product,  on_delete=models.CASCADE, related_name='reviews')

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5')

    def save(self, *args, **kwargs):
        # Check if customer already reviewed this product
        if Review.objects.filter(customer=self.customer, product=self.product).exists():
            raise ValidationError('A customer can review a product only once')
        self.full_clean()
        super().save(*args, **kwargs)

    def has_customer_purchased_product(self):
        # ORDER APP NOT YET INTEGRATED - placeholder returns True
        # Once Capendit Order/OrderItem app is merged, replace with:
        # from orders.models import OrderItem
        # return OrderItem.objects.filter(
        #     order__customer=self.customer,
        #     product=self.product,
        #     order__status='completed'
        # ).exists()
        return True

    class Meta:
        unique_together = ['customer', 'product']

    def __str__(self):
        return f"Review by {self.customer.person.first_name} for {self.product.name}"
