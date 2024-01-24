from django import forms
from django.contrib.auth.forms import UserCreationForm
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from .models import *


class ChickenFigureForm(forms.ModelForm):
    class Meta:
        model = ChickenFigures_b
        fields = ('chicken_in',)


class ChickenOutForm(forms.ModelForm):
    class Meta:
        model = ChickenFigures_b
        fields = ('customer', 'chicken_out', 'chicken_out_kilogram', 'chicken_out_unit_price',)


class ChickenSlaughteredForm(forms.ModelForm):
    class Meta:
        model = ChickenFigures_b
        fields = ('chicken_slaughtered',)


class ChickenMortalityForm(forms.ModelForm):
    class Meta:
        model = ChickenFigures_b
        fields = ('chicken_mortality',)


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed_b
        fields = ('feed_description', 'feed_quantity', 'feed_cost')


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drugs_b
        fields = ('drug_description', 'drug_cost')


class NecessitiesForm(forms.ModelForm):
    class Meta:
        model = Necessities_b
        fields = ('necessities_description', 'necessities_cost')


class ColdRoomInForm(forms.ModelForm):
    class Meta:
        model = ColdRoomIn_b
        fields = ('chickens_in_freezer',)


class ColdRoomOutForm(forms.ModelForm):
    class Meta:
        model = ColdRoomIn_b
        fields = ('total_coldroom',)


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production_b
        fields = ('production_description', 'production_cost')


class ImprestForm(forms.ModelForm):
    class Meta:
        model = Imprest_b
        fields = ('imprest',)


class TotalImprestForm(forms.ModelForm):
    class Meta:
        model = Imprest_b
        fields = ('total_imprest',)


class NotePadForm(forms.ModelForm):
    note = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = NotePad_b
        fields = ('title', 'note')


class OffalsForm(forms.ModelForm):
    class Meta:
        model = Offals_b
        fields = ('offals_description', 'offals_cost')


class ProfitForm(forms.ModelForm):
    class Meta:
        model = Profit_b
        fields = ('income', 'expenditure', 'calculate')


class ChickenForm(forms.ModelForm):
    class Meta:
        model = ChickenFigures_b
        fields = ('total_chicken',)
