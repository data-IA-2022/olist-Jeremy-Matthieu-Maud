import csv
from django.shortcuts import render, redirect
import pandas as pd
from .models import product_category_name_translation
from .forms import TraductionForm

def ajouter_traduction(request):
    if request.method == 'POST':
        form = TraductionForm(request.POST)
        if form.is_valid():
            # Créer une nouvelle instance du modèle à partir des données du formulaire
            traduction = form.save(commit=False)
            traduction.save()
            # Rediriger vers la page de succès
            return redirect('succes')
    else:
        form = TraductionForm()
    return render(request, 'ajouter_traduction.html', {'form': form})

def home(request):
    data = pd.read_csv("/home/matthieu/Formation_IA/Briefs/olist-Jeremy-Matthieu-Maud/archive/product_category_name_translation.csv")
    data_dict = data.to_dict('records')
    return render(request, 'home.html', {'data': data_dict})

def test(request):
    donnees = product_category_name_translation.objects.all()
    return render(request, 'test.html', {'donnees': donnees})

"""def afficher_tout(request):
    donnees = product_category_name_translation.objects.all()
    context = {
        'donnees': donnees
    }
    return render(request, 'test.html', context)"""