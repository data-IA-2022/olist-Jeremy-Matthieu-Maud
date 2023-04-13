import csv
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from .models import product_category_name_translation, TraductionSerializer
from .forms import TraductionForm



import requests

def ajouter_traduction(request):
    if request.method == 'POST':
        form = TraductionForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            product_category_name = form.cleaned_data['product_category_name']
            product_category_name_english = form.cleaned_data['product_category_name_english']
            product_category_name_french = form.cleaned_data['product_category_name_french']

            # Envoyer une requête POST à l'API pour enregistrer la traduction
            data = {
                'product_category_name': product_category_name,
                'product_category_name_english': product_category_name_english,
                'product_category_name_french': product_category_name_french,
            }
            response = requests.post('http://localhost:8000/trad/', data=data)

            # Vérifier la réponse de l'API
            if response.status_code == 201:
                # Rediriger vers la page de succès
                return redirect('succes')
            else:
                form.add_error(None, 'Une erreur est survenue lors de l\'enregistrement de la traduction.')
    else:
        form = TraductionForm()
    return render(request, 'ajouter_traduction.html', {'form': form})



def home(request):
    data = pd.read_csv("/home/matthieu/Formation_IA/Briefs/olist-Jeremy-Matthieu-Maud/archive/product_category_name_translation.csv")
    data_dict = data.to_dict('records')
    return render(request, 'home.html', {'data': data_dict})


@csrf_exempt
def test(request):
    form = TraductionForm()
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


class Traduction(APIView):
    """
    API endpoint that allows Traductions to be viewed or edited.
    """
    """authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]"""

    def get(self, request, format=None):
        traductions = product_category_name_translation.objects.all()
        serializer = TraductionSerializer(traductions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TraductionSerializer(data=request.data)
        if serializer.is_valid():
            product_category_name = serializer.validated_data.get('product_category_name')
            product_category_name_english = serializer.validated_data.get('product_category_name_english')
            product_category_name_french = serializer.validated_data.get('product_category_name_french')

            traduction = product_category_name_translation(
                product_category_name=product_category_name,
                product_category_name_english=product_category_name_english,
                product_category_name_french=product_category_name_french
            )

            traduction.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, format=None):
        product_category_name = request.data.get('product_category_name')
        traduction = product_category_name_translation.objects.filter(product_category_name=product_category_name)
        if traduction:
            traduction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
