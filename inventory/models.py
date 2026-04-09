from django.db import models
from django.core.exceptions import ValidationError


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    capacity = models.IntegerField()

    def clean(self):
        if self.capacity < 0:
            raise ValidationError('Capacity must be 0 or greater.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.OneToOneField(
        'products.Product', on_delete=models.CASCADE, related_name='inventory'
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='inventory_items'
    )
    stock_level = models.IntegerField(default=0)
    reorder_threshold = models.IntegerField(default=10)
    last_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.stock_level < 0:
            raise ValidationError('Stock level cannot be negative.')
        if self.reorder_threshold < 0:
            raise ValidationError('Reorder threshold cannot be negative.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def needs_reorder(self):
        return self.stock_level <= self.reorder_threshold

    def __str__(self):
        return f"{self.product.name} @ {self.warehouse.name} ({self.stock_level} units)"

