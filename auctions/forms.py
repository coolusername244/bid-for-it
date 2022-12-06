from django.forms import ModelForm 

from .models import Listing, Category

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "subtitle",
            "description",
            "price",
            "category",
            "image_url",
        ]

        widgets = {

        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control mb-3'
            if self.fields['category'] == 14:
                field.widget.attrs["class"] = "text-red"