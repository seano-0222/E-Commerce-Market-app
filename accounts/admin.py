

from django.contrib import admin

from .models import Person, Customer, Vendor




@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin view for the Person supertype."""

    # Columns shown in the change-list table
    list_display  = ('person_id', 'first_name', 'last_name', 'email', 'display_role', 'created_at')
    # Fields searched by the search box
    search_fields = ('first_name', 'last_name', 'email')
    # Right-side filter panel
    list_filter   = ('created_at',)
    # Default sort order
    ordering      = ('last_name', 'first_name')

    @admin.display(description='Role')
    def display_role(self, obj):
        """Return the person's role (Customer / Vendor / Unassigned)."""
        return obj.get_role()


# ---------------------------------------------------------------------------
# Customer Admin
# ---------------------------------------------------------------------------

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin view for the Customer subtype."""

    list_display  = ('customer_id', 'get_full_name', 'get_email')
    search_fields = ('person__first_name', 'person__last_name', 'person__email')

    # ------------------------------------------------------------------
    # Custom columns that read from the related Person record
    # ------------------------------------------------------------------

    @admin.display(description='Full Name')
    def get_full_name(self, obj):
        """Return the customer's full name via their linked Person."""
        return f"{obj.person.first_name} {obj.person.last_name}"

    @admin.display(description='Email')
    def get_email(self, obj):
        """Return the customer's email via their linked Person."""
        return obj.person.email


# ---------------------------------------------------------------------------
# Vendor Admin
# ---------------------------------------------------------------------------

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    """Admin view for the Vendor subtype."""

    list_display  = ('vendor_id', 'get_full_name', 'get_email', 'store_name')
    search_fields = ('person__first_name', 'person__last_name', 'person__email', 'store_name')
    list_filter   = ('store_name',)

  

    @admin.display(description='Full Name')
    def get_full_name(self, obj):
        """Return the vendor's full name via their linked Person."""
        return f"{obj.person.first_name} {obj.person.last_name}"

    @admin.display(description='Email')
    def get_email(self, obj):
        """Return the vendor's email via their linked Person."""
        return obj.person.email
