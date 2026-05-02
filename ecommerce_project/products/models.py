from django.db import models
from django.core.exceptions import ValidationError
from categories.models import Category


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def clean(self):
        if self.price <= 0:
            raise ValidationError('Price must be greater than 0')
        if self.stock_qty < 0:
            raise ValidationError('Stock quantity must be 0 or positive')
        if not self.name or self.name.strip() == '':
            raise ValidationError('Product name cannot be null')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Discount model for multiple discount offers
class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    products = models.ManyToManyField(Product, related_name='discounts')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.percentage}%"