from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('review_id', 'get_customer_name', 'product', 'rating', 'review_date')
    search_fields = ('customer__person__first_name', 'customer__person__last_name', 'product__name')
    list_filter   = ('rating',)

    @admin.display(description='Customer')
    def get_customer_name(self, obj):
        return str(obj.customer.person)
