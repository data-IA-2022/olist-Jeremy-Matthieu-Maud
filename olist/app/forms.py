from django import forms
from .models import product_category_name_translation

class TraductionForm(forms.ModelForm):
    class Meta:
        model = product_category_name_translation
        fields = ['product_category_name', 'product_category_name_english', 'product_category_name_french']
