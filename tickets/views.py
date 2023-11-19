from django.urls import reverse_lazy
from django.views.generic.list import ListView #Lista objetos desde una bd
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Ticket, Tech
from .forms import TicketForm
from django.http import Http404
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'tickets/home.html')

@method_decorator(login_required, name='dispatch')
class TicketListView(ListView):
    model = Ticket
    #Opcional
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    
    def get_queryset(self):
        return Ticket.objects.filter(tech=Tech.objects.get(user=self.request.user))
    
# @method_decorator(login_required, name='dispatch')
# class TicketDetailView(DetailView):
#     model = Ticket
#     template_name = 'tickets/ticket_detail.html'
#     context_object_name = 'ticket'
    
#     def get_object(self, queryset=None):
#         """Sobrescribe el método estándar para asegurarase de que el ticket pertenece al técnico."""
#         ticket = super().get_object(queryset)
#         #Verifica siel ticket está asignado al usuario final
#         if ticket.tech == Tech.objects.get(user=self.request.user):
#             return ticket
#         else:
#             raise Http404("No tienes permiso para ver este ticket.")
@method_decorator(login_required, name='dispatch')
class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'
    
    def get_object(self, queryset=None):
        """Sobrescribe el método estándar para asegurarase de que el ticket pertenece al técnico."""
        ticket = super().get_object(queryset)
        # Verifica si el ticket está asignado al usuario final
        if ticket.tech == Tech.objects.get(user=self.request.user):
            return ticket
        else:
            # Redirige a la página de error 404 personalizada
            return redirect('custom_404_view')

        
        
@method_decorator(login_required, name='dispatch')
class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket_list')
    
    def form_valid(self, form):
        tech_instance = Tech.objects.get(user=self.request.user)
        form.instance.tech = tech_instance
        self.object = form.save()
        response = super().form_valid(form)
        return response

class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket_list')
    
class TicketDeleteView(DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket_list')


def custom_404_view(request, exception=None):
    return render(request, 'tickets/404.html', status=404)

