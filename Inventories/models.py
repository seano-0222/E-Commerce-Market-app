from django.db import models
from django.core.exceptions import ValidationError


class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(
        help_text='Maximum number of stock units this warehouse can hold.'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.name or self.name.strip() == '':
            raise ValidationError('Warehouse name cannot be null or empty.')
        if not self.location or self.location.strip() == '':
            raise ValidationError('Warehouse location cannot be null or empty.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.location})'

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        ordering = ['name']


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)

    # Relationships — referenced by name strings to avoid circular imports,
    # since Product lives in a sibling app maintained by a teammate.
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='inventories',
        help_text='The product being tracked in this inventory record.'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='inventories',
        help_text='The warehouse where this stock is stored.'
    )

    quantity = models.PositiveIntegerField(
        default=0,
        help_text='Current stock quantity available in this warehouse.'
    )
    reorder_threshold = models.PositiveIntegerField(
        default=10,
        help_text='Minimum quantity before a restock is triggered.'
    )
    reorder_quantity = models.PositiveIntegerField(
        default=50,
        help_text='How many units to order when restocking.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.reorder_threshold is not None and self.reorder_quantity is not None:
            if self.reorder_quantity <= 0:
                raise ValidationError('Reorder quantity must be greater than zero.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_low_stock(self):
        """Returns True when current quantity is at or below the reorder threshold."""
        return self.quantity <= self.reorder_threshold

    def __str__(self):
        return f'Inventory [{self.product}] @ {self.warehouse} — qty: {self.quantity}'

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
        # Each product should have at most one inventory record per warehouse.
        unique_together = ('product', 'warehouse')
        ordering = ['warehouse', 'product']
