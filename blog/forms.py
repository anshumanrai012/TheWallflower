from .models import Post, Author
from django import forms


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'email', 'gender', 'bio', 'picture'

                  ]
