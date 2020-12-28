from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import FilmForm, DodatkoweInfoForm
from .models import Film, DodatkoweInfo


# Create your views here.


def wszystkie_filmy(request):
    # return HttpResponse("<h1>To jest test.</h1>")
    # test = "to jest coś we views"
    # return render(request, 'filmy/filmy.html', {'text': test})
    wszystkie = Film.objects.all()
    return render(request, 'filmy/filmy.html', {'filmy': wszystkie})

@login_required
def nowy_film(request):
    form_film = FilmForm(request.POST or None, request.FILES or None)
    form_dodatkowe = DodatkoweInfoForm(request.POST or None)

    if all((form_film.is_valid(), form_dodatkowe.is_valid())):
        film = form_film.save(commit=False)
        dodatkowe = form_dodatkowe.save()
        film.dodatkowe = dodatkowe
        film.save()
        return redirect(wszystkie_filmy)
    return render(request, 'filmy/film_form.html', {'form': form_film, 'form_dodatkowe': form_dodatkowe, 'nowy': True} )

@login_required
def edytuj_film(request, id):
    film = get_object_or_404(Film, pk=id)
    try:
        dodatkowe = DodatkoweInfo.objects.get(film=film.id)
    except DodatkoweInfo.DoesNotExist:
        dodatkowe = None

    form_film = FilmForm(request.POST or None, request.FILES or None, instance=film)
    form_dodatkowe = DodatkoweInfoForm(request.POST or None, instance=dodatkowe)

    if all((form_film.is_valid(), form_dodatkowe.is_valid())):
        film = form_film.save(commit=False)
        dodatkowe = form_dodatkowe.save()
        film.dodatkowe = dodatkowe
        film.save()
        return redirect(wszystkie_filmy)
    return render(request, 'filmy/film_form.html', {'form': form_film, 'form_dodatkowe': form_dodatkowe, 'nowy': False})

@login_required
def usun_film(request, id):
    film = get_object_or_404(Film, pk=id)

    if request.method == 'POST':
        film.delete()
        return redirect(wszystkie_filmy)

    return render(request, 'filmy/potwierdz.html', {'film': film})
