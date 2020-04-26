from .models import Author, Post
from django import forms

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('username', 'name', 'email')


