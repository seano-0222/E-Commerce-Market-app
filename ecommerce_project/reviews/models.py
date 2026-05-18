from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings  # Change this
from products.models import Product

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')  # Change this
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5')

    def save(self, *args, **kwargs):
        # Check if customer already reviewed this product
        if Review.objects.filter(customer=self.customer, product=self.product).exists():
            raise ValidationError('A customer can review a product only once')

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['customer', 'product']

    def __str__(self):
        return f"Review by {self.customer.username} for {self.product.name}"