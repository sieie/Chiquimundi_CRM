from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse
from leads.models import Agent, User
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin

User = get_user_model()

class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    
    
class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    
    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        # Guarda el formulario de agente sin cometerlo a la base de datos
        agent = form.save(commit=False)
        
        # Obtiene o crea el usuario asociado al agente por su nombre
        user, created = User.objects.get_or_create(
            username=agent.nombre,
            defaults={
                'email': agent.email,
                'is_agent': True,
                'is_organisor': False,
            }
        )

        # Asigna el usuario al agente
        agent.user = user
        agent.organisation = self.request.user.userprofile
        agent.save()

        return super(AgentCreateView, self).form_valid(form)
    
    def form_invalid(self, form):
        return render(self.request, 'agents/agent_create_error.html')



class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    
    
class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    
    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"
    
    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)