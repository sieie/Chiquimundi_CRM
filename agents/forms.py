from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from leads.models import Agent

User = get_user_model()

class AgentModelForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = (
            'cedula',
            'nombre',
            'apellido',
            'telefono',
            'email',            
        )