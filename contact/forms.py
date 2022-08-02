from django import forms
from .models import ContactForm

class Contact(forms.ModelForm):
    """
    Class to define the fields for contact form to instantiate
    onto a page when contact form is called.
    """
    class Meta:
        model = ContactForm
        fields = ('first_name', 'last_name', 'email', 'phone', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone': 'Contact Number',
            'message': 'Your Message',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
