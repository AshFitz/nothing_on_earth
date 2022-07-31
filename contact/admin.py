from django.contrib import admin

from .models import ContactForm

class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'message',
    )


admin.site.register(ContactForm, ContactAdmin)

