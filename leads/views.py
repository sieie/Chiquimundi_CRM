from django.db import transaction
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Lead, Category, Proforma
from .forms import ArticuloForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm, ProformaForm

from django.template.loader import get_template

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
                agente__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
                agente__isnull=False
            )
            # filtro para el agente logeado
            queryset = queryset.filter(agente__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agente__isnull=True
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
            queryset = queryset.filter(agente__user=user)
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
        return reverse("leads:list")
    
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        # ENVIO DE EMAILS
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
        return reverse("leads:list")


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
        return reverse("leads:list")

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
        return reverse("leads:list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_organisor:
            leads_queryset = Lead.objects.filter(
                organisation=user.userprofile, 
            )
        else:
            leads_queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
            )
        
        categories_with_lead_counts = []
        
        for category in self.get_queryset():
            lead_count = leads_queryset.filter(category=category).count()
            categories_with_lead_counts.append({
                "category": category,
                "lead_count": lead_count
            })
        
        context.update({
            "unassigned_lead_count": leads_queryset.filter(category__isnull=True).count(),
            "categories_with_lead_counts": categories_with_lead_counts
        })
        return context
    
    def get_queryset(self):
        user = self.request.user
        # inicia la consulta de los leads si el usuario es organizador
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile, 
            )
        else:
            leads_queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
            )
            # filtro para el agente logeado
            leads_queryset = leads_queryset.filter(agent__user=user)
            
            # Obtén todas las categorías de los leads del queryset filtrado
            queryset = Category.objects.filter(leads__in=leads_queryset).distinct()
            
        return queryset



class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"
    
    def get_context_data(self, **kwargs):
        # queryset de los leads sin asignar un agente
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        leads = self.get_object().leads.all()        
        context.update({
            "leads": leads
        })
        return context
    
    def get_queryset(self):
        user = self.request.user
        # inicia la consulta de los leads si el usuario es organizador
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile, 
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
            )
            # filtro para el agente logeado
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm
    
    def get_queryset(self):
        user = self.request.user
        # inicia la consulta de los leads si el usuario es organizador
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
            )
            # filtro para el agente logeado
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:detail", kwargs={"pk": self.get_object().id})
    

#CREAR PROFORMA
class CrearProformaView(generic.TemplateView):
    template_name = 'leads/crear_proforma.html'

    def post(self, request, *args, **kwargs):
        form = ProformaForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                proforma = form.save(commit=False)
                articulos_seleccionados = form.cleaned_data['articulos']
                proforma.save()
                proforma.articulos.set(articulos_seleccionados)

                # Agregar un mensaje de éxito
                messages.success(request, 'La proforma se creó correctamente.')

                # Renderizar el PDF y proporcionar el enlace en la respuesta
                response = self.generate_pdf_response(proforma)
                return response

        return self.render_to_response({'form': form})

    def get(self, request, *args, **kwargs):
        form = ProformaForm()
        return self.render_to_response({'form': form})

    def generate_pdf_response(self, proforma):
        # Carga la plantilla HTML para la proforma
        template = get_template('leads/proforma_template.html')
        context = {'proforma': proforma}

        # Obtener los nombres de los artículos y agregarlos al contexto
        articulos = proforma.articulos.all()
        context['articulo_names'] = [articulo.nombre for articulo in articulos]

        # Renderiza el HTML usando el contexto
        html = template.render(context)

        # Crea un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=proforma_{proforma.id}.pdf'

        # Crea el PDF a partir del HTML renderizado
        pisa.CreatePDF(html, dest=response)
        
        return response
    

#CREAR ARTICULO
def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leads:list') 
    else:
        form = ArticuloForm()
    
    return render(request, 'leads/articulo_create.html', {'form': form})