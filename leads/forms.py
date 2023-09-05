from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from .models import Lead, User, Agent, Category

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'nombre',
            'apellido',
            'telefono',
            'agente',
            'email',
            'category',
            'description',
        )
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'telefono': 'Teléfono',
            'agente': 'Agente de venta',
            'email': 'Correo electrónico',
            'category': 'Estado de Lead',
            'description': 'Descripción',
        }

# class LeadForm(forms.Form):
#     nombre = forms.CharField()
#     apellido = forms.CharField()
#     telefono = forms.CharField()
#     agente = forms.ChoiceField(choices='')
#     email = forms.EmailField()
#     estado = forms.ChoiceField(choices='')
#     descripcion = forms.CharField()
    
    
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
        
        
class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
            )
        
        
class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )