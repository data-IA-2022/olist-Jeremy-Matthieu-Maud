from django import forms
from .models import product_category_name_translation

class TraductionForm(forms.ModelForm):
    product_category_name = forms.CharField(max_length=100)
    product_category_name_english = forms.CharField(max_length=100)
    product_category_name_french = forms.CharField(max_length=100)

    class Meta:
        model = product_category_name_translation
        fields = ['product_category_name', 'product_category_name_english', 'product_category_name_french']
