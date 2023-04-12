import csv
from django.shortcuts import render, redirect ,get_object_or_404
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
    form = []
    if request.method == 'POST':
        if 'afficher' in request.POST:
            donnees = product_category_name_translation.objects.all()
            afficher = True
        elif 'supprimer' in request.POST:
            traduction_id = request.POST.get('traduction_id')
            traduction = get_object_or_404(product_category_name_translation, product_category_name=traduction_id)
            traduction.delete()
            donnees = product_category_name_translation.objects.all()
            afficher = True
        else:
            form = TraductionForm(request.POST)
            if form.is_valid():
                form.save()
            donnees = []
            afficher = False
    else:
        form = TraductionForm()
        donnees = []
        afficher = False

    context = {'form': form, 'donnees': donnees, 'afficher': afficher}
    return render(request, 'test.html', context)

