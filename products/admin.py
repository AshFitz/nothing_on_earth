from django.contrib import admin
from .models import Product, Collection


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'collection',
        'price',
        'image',
    )
    
    ordering = ('sku',)

class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
