from .models import Category 

def navbar_categories(request):
    return {
        "category_dropdown": Category.objects.exclude(name="please_select").order_by('name')
    }