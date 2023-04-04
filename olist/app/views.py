import csv
from django.shortcuts import render
import pandas as pd

def home(request):
    data = pd.read_csv("/home/matthieu/Formation_IA/Briefs/olist-Jeremy-Matthieu-Maud/archive/product_category_name_translation.csv")
    data_dict = data.to_dict('records')
    return render(request, 'home.html', {'data': data_dict})
