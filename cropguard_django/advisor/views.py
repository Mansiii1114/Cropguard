from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm

from .forms import SignUpForm, RecommendForm, DiseaseForm
from .models import RecommendationHistory
from .crops_data import recommend, CROPS, get_crop
from .disease_data import diagnose


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'advisor/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        error = 'Username or password is incorrect.'
    else:
        form = AuthenticationForm()
    return render(request, 'advisor/login.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    history = request.user.history.all()[:5]
    latest = history[0] if history else None
    context = {
        'count': request.user.history.count(),
        'latest': latest,
    }
    return render(request, 'advisor/dashboard.html', context)


@login_required
def recommend_view(request):
    results = None
    if request.method == 'POST':
        form = RecommendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            results = recommend(cd['nitrogen'], cd['phosphorus'], cd['potassium'], cd['ph'],
                                 cd['temperature'], cd['humidity'], cd['rainfall'], cd['season'])
            best = results[0]
            RecommendationHistory.objects.create(
                user=request.user, crop=best['name'], match_score=best['score10'],
                risk_label=best['risk_label'], risk_score=best['risk_score'],
                nitrogen=cd['nitrogen'], phosphorus=cd['phosphorus'], potassium=cd['potassium'],
                ph=cd['ph'], temperature=cd['temperature'], humidity=cd['humidity'],
                rainfall=cd['rainfall'], season=cd['season'],
            )
    else:
        form = RecommendForm()
    return render(request, 'advisor/recommend.html', {'form': form, 'results': results})


@login_required
def disease_view(request):
    results = None
    checked = []
    if request.method == 'POST':
        form = DiseaseForm(request.POST)
        if form.is_valid():
            checked = form.cleaned_data['symptoms']
            results = diagnose(checked)
    else:
        form = DiseaseForm()
    return render(request, 'advisor/disease.html', {'form': form, 'results': results, 'checked': checked})


@login_required
def history_view(request):
    history = request.user.history.all()
    return render(request, 'advisor/history.html', {'history': history})


def library_view(request):
    return render(request, 'advisor/library.html', {'crops': CROPS})


def crop_detail_view(request, crop_name):
    crop = get_object_or_404_crop(crop_name)
    return render(request, 'advisor/crop_detail.html', {'c': crop})


def get_object_or_404_crop(name):
    crop = get_crop(name)
    if crop is None:
        from django.http import Http404
        raise Http404('Crop not found')
    return crop
