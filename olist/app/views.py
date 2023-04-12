import csv
from django.shortcuts import render, redirect
import pandas as pd
from .models import product_category_name_translation
from .forms import TraductionForm
from django.views.decorators.csrf import csrf_exempt

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



@csrf_exempt

def test(request):
    afficher = False
    if request.method == 'POST':
        form = TraductionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('test')
    else:
        form = TraductionForm()

    donnees = []
    afficher = False
    if 'afficher' in request.POST:
        donnees = product_category_name_translation.objects.all()
        afficher = True
    elif 'masquer' in request.POST:
        afficher = False

    context = {'form': form, 'donnees': donnees, 'afficher': afficher}
    return render(request, 'test.html', context)

