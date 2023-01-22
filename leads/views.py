from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Agent, Lead
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")


# HOME LOANDING
class LandingPageView(generic.TemplateView):
    template_name = "landing.html"      

def landing_page(request):
    return render(request, "landing.html")


# LISTA DE CLIENTES
class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # inicia la consulta de los leads si el usuario es organizador
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
                agent__isnull=False
            )
            # filtro para el agente logeado
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })    
        return context
        

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "leads/lead_list.html", context)


# DETALLE DE CLIENTES
class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detalle.html"
    context_object_name = "lead"
  
    def get_queryset(self):
        user = self.request.user
        # inicia la consulta de los leads si el usuario es organizador
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filtro de agentes conectados
            queryset = queryset.filter(agent__user=user)
        return queryset
  
    
def lead_detalle(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detalle.html", context)



# CREACIÓN DE LEAD
class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lista")
    
    def form_valid(self, form):
        # TODO ENVIO DE EMAILS
        send_mail(
            subject="Haz creado un nuevo Lead!!",
            message="Ingresa al CRM para visualizarlo",
            from_email="eedelgado@est.istgg.edu.ec",
            recipient_list=["testsieie@gmail.com"]
        )
        return super(LeadCreateView, self).form_valid(form)
    
    
def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)


# ACTUALIZACIÓN/MODIFICACIÓN DE LEAD
class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
    
    def get_success_url(self):
        return reverse("leads:lista")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)     
    
# BORRAR LEAD
class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_success_url(self):
        return reverse("leads:lista")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")
    
    
# Asigna un agente de ventas a un lead
class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lista")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)



    
    
    #forma larga para setear los valores de las variables en la db    
    
        # apellido = form.cleaned_data['apellido']
        # nombre = form.cleaned_data['nombre']
        # telefono = form.cleaned_data['telefono']
        # agent = form.cleaned_data['agent']
        # lead.nombre = nombre
        # lead.apellido = apellido
        # lead.telefono = telefono
        # lead.agent = agent 
                


# def lead_create(request):
#   form = LeadForm()
#   if request.method == "POST":
#       form = LeadForm(request.POST)
#         if form.is_valid():
#           nombre = form.cleaned_data['nombre']
#           apellido = form.cleaned_data['apellido']
#           telefono = form.cleaned_data['telefono']
#           agent = Agent.objects.first()
#           Lead.objects.create(
#               nombre=nombre,
#               apellido=apellido,
#               telefono=telefono,
#               agent=agent
#             )
#             return redirect("/leads")
#     context = {
#         "form": form
#     }
#     return render(request, "leads/lead_create.html", context)