from django.contrib import admin
from .models import Product, Attribute, Value


# Custom admin configuration for the Value model
class ValueAdmin(admin.ModelAdmin):
    # Exclude the 'selected' field from the admin form
    exclude = ['selected']


admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(Value, ValueAdmin)
