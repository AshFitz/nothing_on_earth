from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
    name = models.CharField(max_length=254,null=True, blank=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    collection = models.ForeignKey('Collection', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    details = models.TextField(max_length=254, null=True, blank=True)
    has_sizes = models.BooleanField(default=True, null=True, blank=True)
    sale = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image2_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=True, blank=True,related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                            related_name='user_review')
    comment = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.user.username
