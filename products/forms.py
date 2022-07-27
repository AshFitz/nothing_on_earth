from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Collection


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image 1', required=False, widget=CustomClearableFileInput)
    image2 = forms.ImageField(label='', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        collection = Collection.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in collection]

        self.fields['collection'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-0'