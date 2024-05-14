from django.contrib import admin
from .models import Product, Attribute, Value


class ValueAdmin(admin.ModelAdmin):
    exclude = ['selected']


admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(Value, ValueAdmin)
