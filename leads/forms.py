from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from .models import Lead, User, Agent

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'nombre',
            'apellido',
            'telefono',
            'agent',
        )
        

class LeadForm(forms.Form):
    nombre = forms.CharField()
    apellido = forms.CharField()
    telefono = forms.CharField()
    #email = forms.EmailField()
    #agente = forms.ChoiceField(choices='')
    
    
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
        
        
class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents