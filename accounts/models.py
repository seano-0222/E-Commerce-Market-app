"""
Models for the accounts app.

This module defines the Person supertype and Customer/Vendor subtypes
for the e-commerce identity system.

ERD Summary:
    Person (supertype)
        └── Customer (subtype) — OneToOne → Person
        └── Vendor   (subtype) — OneToOne → Person

Business Rules:
    - Every Person must be EITHER a Customer OR a Vendor, never both.
    - A Person cannot be simultaneously linked to both Customer and Vendor.
    - Email must be unique across all Person records.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# ---------------------------------------------------------------------------
# Supertype: Person
# ---------------------------------------------------------------------------

class Person(models.Model):
    user       = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='person'
    )
    person_id  = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    address    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # ------------------------------------------------------------------
    # Bonus method: returns "Customer", "Vendor", or "Unassigned"
    # ------------------------------------------------------------------
    def get_role(self):
        """
        Return the role of this person.

        Uses reverse OneToOne accessors created by Customer.person
        and Vendor.person (related_name='customer' / 'vendor').
        """
        if hasattr(self, 'customer'):
            return 'Customer'
        elif hasattr(self, 'vendor'):
            return 'Vendor'
        return 'Unassigned'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name        = 'Person'
        verbose_name_plural = 'Persons'
        ordering            = ['last_name', 'first_name']


# ---------------------------------------------------------------------------
# Subtype: Customer
# ---------------------------------------------------------------------------

class Customer(models.Model):
    """
    Subtype of Person for buyers in the e-commerce platform.

    Future relationships (handled by other apps):
        - Cart    → OneToOne  back-reference from Cart app
        - Order   → OneToMany back-reference from Orders app
        - Review  → OneToMany back-reference from Reviews app
    """

    customer_id = models.AutoField(primary_key=True)
    person      = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        related_name='customer',   # allows person.customer reverse lookup
    )

    # ------------------------------------------------------------------
    # Validation: enforce the Customer-OR-Vendor exclusivity rule
    # ------------------------------------------------------------------
    def clean(self):
        """
        Prevent a Person from being both a Customer and a Vendor.

        Called automatically by full_clean(), which is triggered in save().
        Raises ValidationError if the linked Person already has a Vendor.
        """
        # hasattr uses the related_name 'vendor' defined on Vendor.person
        if hasattr(self.person, 'vendor'):
            raise ValidationError(
                f"'{self.person}' is already registered as a Vendor. "
                "A person cannot be both a Customer and a Vendor."
            )

    def save(self, *args, **kwargs):
        """Run full model validation before every save."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Customer: {self.person.first_name} {self.person.last_name}"

    class Meta:
        verbose_name        = 'Customer'
        verbose_name_plural = 'Customers'


# ---------------------------------------------------------------------------
# Subtype: Vendor
# ---------------------------------------------------------------------------

class Vendor(models.Model):
    """
    Subtype of Person for sellers in the e-commerce platform.

    Future relationships (handled by other apps):
        - Product → OneToMany back-reference from Products app
    """

    vendor_id  = models.AutoField(primary_key=True)
    person     = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        related_name='vendor',   # allows person.vendor reverse lookup
    )
    store_name = models.CharField(max_length=150)

    # ------------------------------------------------------------------
    # Validation: enforce the Customer-OR-Vendor exclusivity rule
    # ------------------------------------------------------------------
    def clean(self):
        """
        Prevent a Person from being both a Vendor and a Customer.

        Called automatically by full_clean(), which is triggered in save().
        Raises ValidationError if the linked Person already has a Customer.
        """
        # hasattr uses the related_name 'customer' defined on Customer.person
        if hasattr(self.person, 'customer'):
            raise ValidationError(
                f"'{self.person}' is already registered as a Customer. "
                "A person cannot be both a Vendor and a Customer."
            )

    def save(self, *args, **kwargs):
        """Run full model validation before every save."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Vendor: {self.person.first_name} {self.person.last_name} "
            f"| Store: {self.store_name}"
        )

    class Meta:
        verbose_name        = 'Vendor'
        verbose_name_plural = 'Vendors'
