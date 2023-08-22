from django.shortcuts import render, get_object_or_404, redirect
from maps.models import *
from django import forms
from django.contrib.gis.db.models import PointField
from leaflet.forms.widgets import LeafletWidget
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

class GeneroForm(forms.ModelForm):
    genero = forms.ModelChoiceField(queryset=Genero.objects.all(), empty_label='Selecione um gênero')
    
    class Meta:
        model = Genero
        fields = ('genero',)
        
class GeneroCreationForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ('genero',)
        
class MapForm(forms.ModelForm):
    
    class Meta:
        model = Local
        fields = ('latitude', 'longitude', 'especie')
        
class EspecieCreationForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = ('__all__')



def mapa(request):
    genero_selecionado = request.GET.get('genero')
    especie_selecionada = request.GET.get('especie')
    form = GeneroForm(request.GET)
    
    if genero_selecionado:
        especies = Especie.objects.filter(genero_id=genero_selecionado)
    else:
        especies = Especie.objects.none()
    
    if especie_selecionada:
        pontos = Local.objects.filter(especie_id=especie_selecionada)
    else:
        pontos = Local.objects.none()
    
    context = {
        'pontos': pontos,
        'especies': especies,
        'form': form,
        'especie_selecionada': especie_selecionada
    }
    
    return render(request, 'mapa.html', context)

@login_required()
def create_genero(request):
    
    if request.method == 'POST':
        
        form = GeneroCreationForm(request.POST)
        
        context = { 
            'form': form,
        }
        
        if form.is_valid:
            genero = form.save()
            messages.success(request, 'Genero criado com sucesso!')
            return redirect('index')
    
        return render(request, 'add_genero.html', context)
    
    context = { 
        'form': GeneroCreationForm(),
    }
    
    return render(request, 'add_genero.html', context)

@login_required()
def criar_especie(request):
    if request.method == 'POST':
        form = EspecieCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EspecieCreationForm()

    context = {
        'form': form
    }
    return render(request, 'add_especie.html', context)

@login_required()
def criar_local(request):
    genero_selecionado = request.GET.get('genero')
    especie_selecionada = request.GET.get('especie')
    genero = GeneroForm(request.GET)
    especie = Especie.objects.filter(especie=especie_selecionada)
    
    if genero_selecionado:
        especies = Especie.objects.filter(genero_id=genero_selecionado)
    else:
        especies = Especie.objects.none()
    
    if request.method == 'POST':
        form = MapForm(request.POST)
        if form.is_valid():
            local = form.save(commit=False)
            local.owner = request.user
            local.save()
            return redirect('index')
    else:
        form = MapForm()

    context = {
        'form': form,
        'genero': genero,
        'especie': especie,
        'especies': especies
    }
    return render(request, 'add_local.html', context)


def login(request):

    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            auth.login(request, form.get_user())
            messages.success(request, 'Logado com sucesso!')
            return redirect('login')
        #TODO: mudar o redirect

    context = {
        'form': form
    }

    return render(request, 'login.html', context)

def index(request):
    
    return render(request, 'index.html')
