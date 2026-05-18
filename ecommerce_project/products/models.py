from django.db import models
from django.core.exceptions import ValidationError
from categories.models import Category
from django.conf import settings  # Change this import


class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='vendor')  # Change this
    store_name = models.CharField(max_length=200, unique=True)
    vendor_trust_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    bio = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.store_name

    def clean(self):
        if self.vendor_trust_score < 0 or self.vendor_trust_score > 5:
            raise ValidationError('Vendor trust score must be between 0.00 and 5.00')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Vendors"


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')

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


class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    products = models.ManyToManyField(Product, related_name='discounts')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.percentage}%"