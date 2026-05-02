"""
Models for the cart app.

ERD Relationships:
    Customer → Cart     (OneToOne)   — each customer has exactly one cart
    Cart     → CartItem (OneToMany)  — a cart holds many cart items
    Product  → CartItem (OneToMany)  — a product can appear in many cart items

Assigned to: Malubay
"""

from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import Customer
from products.models import Product


# ---------------------------------------------------------------------------
# Cart
# ---------------------------------------------------------------------------

class Cart(models.Model):
    """
    A shopping cart belonging to exactly one Customer.

    Relationship: Customer → Cart (OneToOne)
    """

    cart_id    = models.AutoField(primary_key=True)
    customer   = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        """Return the total price of all items in this cart."""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_item_count(self):
        """Return the total number of items (quantities summed) in this cart."""
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.customer.person.first_name} {self.customer.person.last_name}"

    class Meta:
        verbose_name        = 'Cart'
        verbose_name_plural = 'Carts'


# ---------------------------------------------------------------------------
# CartItem
# ---------------------------------------------------------------------------

class CartItem(models.Model):
    """
    A single line item inside a Cart, linking a Product with a quantity.

    Relationships:
        Cart    → CartItem (OneToMany)
        Product → CartItem (OneToMany)
    """

    cart_item_id = models.AutoField(primary_key=True)
    cart         = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product      = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
    )
    quantity     = models.PositiveIntegerField(default=1)
    added_at     = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validate quantity is at least 1."""
        if self.quantity < 1:
            raise ValidationError('Quantity must be at least 1.')
        # Ensure requested quantity does not exceed available stock
        if self.quantity > self.product.stock_qty:
            raise ValidationError(
                f'Only {self.product.stock_qty} units of "{self.product.name}" are in stock.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_subtotal(self):
        """Return price × quantity for this line item."""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product.name} (Cart #{self.cart.cart_id})"

    class Meta:
        verbose_name        = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        # A product can only appear once per cart — increase qty instead
        unique_together = ['cart', 'product']

