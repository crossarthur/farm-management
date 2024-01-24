from django import forms
from django.contrib.auth.forms import UserCreationForm
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from .models import *


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)


class ChickenForm(forms.ModelForm):
    class Meta:
        model = ChickenFigures
        fields = ('total_chicken',)


class ChickenFigureForm(forms.ModelForm):
    class Meta:
        model = ChickenFigures
        fields = ('chicken_in',)


class ChickenOutForm(forms.ModelForm):
    class Meta:
        model = ChickenFigures
        fields = ('customer', 'chicken_out', 'chicken_out_kilogram', 'chicken_out_unit_price',)


class ChickenSlaughteredForm(forms.ModelForm):
    class Meta:
        model = ChickenFigures
        fields = ('chicken_slaughtered',)


class ChickenMortalityForm(forms.ModelForm):
    class Meta:
        model = ChickenFigures
        fields = ('chicken_mortality',)


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ('feed_description', 'feed_quantity', 'feed_cost')


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drugs
        fields = ('drug_description', 'drug_cost')


class NecessitiesForm(forms.ModelForm):
    class Meta:
        model = Necessities
        fields = ('necessities_description', 'necessities_cost')


class ColdRoomInForm(forms.ModelForm):
    class Meta:
        model = ColdRoomIn
        fields = ('chickens_in_freezer',)


class ColdRoomOutForm(forms.ModelForm):
    class Meta:
        model = ColdRoomIn
        fields = ('total_coldroom',)


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ('production_description', 'production_cost')


class ProfitForm(forms.ModelForm):
    class Meta:
        model = Profit
        fields = ('income', 'expenditure', 'calculate')


'''class BookForm(forms.Form):
    author_name = forms.CharField(max_length=100)
    author_nationality = forms.CharField(max_length=100)
    book_title = forms.CharField(max_length=100)
    book_genre = forms.CharField(max_length=100)

    def save(self):
        # Get form data
        author_name = self.cleaned_data['author_name']
        author_nationality = self.cleaned_data['author_nationality']
        book_title = self.cleaned_data['book_title']
        book_genre = self.cleaned_data['book_genre']

        # Create Author instance
        new_author = Author.objects.create(name=author_name, nationality=author_nationality)

        # Create Book instance associated with the author
        new_book = Book.objects.create(title=book_title, genre=book_genre, author=new_author)

        return new_author, new_book'''


class ImprestForm(forms.ModelForm):
    class Meta:
        model = Imprest
        fields = ('imprest',)


class TotalImprestForm(forms.ModelForm):
    class Meta:
        model = Imprest
        fields = ('total_imprest',)


class NotePadForm(forms.ModelForm):
    note = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = NotePad
        fields = ('title', 'note')


class OffalsForm(forms.ModelForm):
    class Meta:
        model = Offals
        fields = ('offals_description', 'offals_cost')
