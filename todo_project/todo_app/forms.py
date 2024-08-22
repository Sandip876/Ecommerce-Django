from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    creation_code = forms.CharField(max_length=10, required=True, widget=forms.PasswordInput)

    class Meta:
        model = Todo
        fields = ['title', 'description', 'completed']


class TodoDeleteForm(forms.Form):
    deletion_key = forms.UUIDField(widget=forms.TextInput(attrs={'type': 'password'}))