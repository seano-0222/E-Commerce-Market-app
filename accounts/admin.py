from django.contrib import admin
from .models import Person, Customer, Vendor


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display  = ['person_id', 'first_name', 'last_name', 'email', 'get_username', 'get_role', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'user__username']

    def get_username(self, obj):
        return obj.user.username if obj.user else '—'
    get_username.short_description = 'Username'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'person']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_id', 'person', 'store_name']