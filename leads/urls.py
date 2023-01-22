from django.urls import path
from .views import (
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, AssignAgentView
)

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lista'),
    path('create/', LeadCreateView.as_view(), name='crear'),
    path('<int:pk>/', LeadDetailView.as_view(), name='detalle'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='actualizar'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='borrar'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='asigna-agente')
]
