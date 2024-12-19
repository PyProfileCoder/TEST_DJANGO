from django.contrib import admin
from .models import Expenses

# Register the Expenses model in the admin
@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'amount', 'date')  # Fields to display in the list view
    search_fields = ('user__username', 'description')  # Allow searching by username and description
    list_filter = ('date',)  # Add filtering by date
