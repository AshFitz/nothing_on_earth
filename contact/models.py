from django.db import models

class ContactForm(models.Model):
    """
    Model to define the fields required to create a contact form request in the database
    """
    first_name = models.CharField(max_length=80, blank=False, null=False)
    last_name = models.CharField(max_length=80, blank=False, null=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False, default='')
    message = models.TextField(null=False, blank=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.message}'
