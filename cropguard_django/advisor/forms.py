from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .crops_data import SEASON_CHOICES
from .disease_data import SYMPTOMS


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=60, label="Your name")

    class Meta:
        model = User
        fields = ["first_name", "username", "password1", "password2"]


class RecommendForm(forms.Form):
    nitrogen = forms.FloatField(label="Nitrogen (N)", required=False,
                                 widget=forms.NumberInput(attrs={"placeholder": "e.g. 80"}))
    phosphorus = forms.FloatField(label="Phosphorus (P)", required=False,
                                   widget=forms.NumberInput(attrs={"placeholder": "e.g. 45"}))
    potassium = forms.FloatField(label="Potassium (K)", required=False,
                                  widget=forms.NumberInput(attrs={"placeholder": "e.g. 40"}))
    ph = forms.FloatField(label="Soil pH", required=False,
                           widget=forms.NumberInput(attrs={"placeholder": "e.g. 6.5", "step": "0.1"}))
    temperature = forms.FloatField(label="Temperature (°C)", required=False,
                                    widget=forms.NumberInput(attrs={"placeholder": "e.g. 26"}))
    humidity = forms.FloatField(label="Humidity (%)", required=False,
                                 widget=forms.NumberInput(attrs={"placeholder": "e.g. 65"}))
    rainfall = forms.FloatField(label="Expected rainfall (mm, season)", required=False,
                                 widget=forms.NumberInput(attrs={"placeholder": "e.g. 900"}))
    season = forms.ChoiceField(label="Season", choices=[(s, s) for s in SEASON_CHOICES])


class DiseaseForm(forms.Form):
    symptoms = forms.MultipleChoiceField(
        choices=SYMPTOMS,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="",
    )
