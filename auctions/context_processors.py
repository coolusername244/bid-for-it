from .models import Category 

# This will enable the "Shop By Category" navbar tab to work across the app
# and be displayed in alphabetical order
def navbar_categories(request):
    return {
        "category_dropdown": Category.objects.exclude(name="please_select").order_by('name')
    }