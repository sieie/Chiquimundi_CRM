from django.urls import path
from .views import (
    AgentListView, AgentCreateView, AgentDetailView, AgentUpdateView, AgentDeleteView
    )

app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent-lista'),
    path('create/', AgentCreateView.as_view(), name='agent-crear'),
    path('<int:pk>/', AgentDetailView.as_view(), name='agent-detalle'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agent-actualizar'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='agent-borrar'),
]