from django.contrib import admin
from .models import Product, Attribute, Value


class AttributeAdmin(admin.ModelAdmin):
    exclude = ['name_for_admin_page']


class ValueAdmin(admin.ModelAdmin):
    exclude = ['name_for_admin_page']


admin.site.register(Product)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Value, ValueAdmin)
