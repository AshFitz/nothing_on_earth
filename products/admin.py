from django.contrib import admin
from .models import Product, Collection, Review


class ProductAdmin(admin.ModelAdmin):
    """
    Organising the list display names for easy reading for admin panel.
    """
    list_display = (
        'sku',
        'name',
        'collection',
        'price',
        'image',
    )
    
    ordering = ('sku',)

class CollectionAdmin(admin.ModelAdmin):
    """
    Collection Admin created to display friendly name or a category and the name.
    """
    list_display = (
        'friendly_name',
        'name',
    )

class ReviewAdmin(admin.ModelAdmin):
    """
    To display the below fields to the Review admin panel.
    """
    list_display = (
        'user',
        'product',
        'comment',
        'timestamp',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Review, ReviewAdmin)
