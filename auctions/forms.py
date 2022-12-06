from django.forms import ModelForm 

from .models import Listing, Category, Condition

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "subtitle",
            "description",
            "price",
            "condition",
            "category",
            "image_url",
        ]

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # get category friendly names
        categories = Category.objects.all()
        friendly_names_category = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names_category

        # get condition friendly names
        conditions = Condition.objects.all()
        friendly_names_condition = [(c.id, c.get_friendly_name()) for c in conditions]
        self.fields['condition'].choices = friendly_names_condition

        # style form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control mb-3'
