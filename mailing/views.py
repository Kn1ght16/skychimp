from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Mailing, Client
from django.http import JsonResponse


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'


class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    fields = '__all__'
    success_url = reverse_lazy('mailing:list')


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    fields = '__all__'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:list')


class MailingStartView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.send_messages()
        return JsonResponse({'status': 'success'})


class MailingStatsView(View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        delivery_attempts = mailing.deliveryattempt_set.all()
        stats = {
            'sent': delivery_attempts.filter(status='отправлено').count(),
            'error': delivery_attempts.filter(status='ошибка').count(),
        }
        return JsonResponse(stats)


def mailing_dashboard(request):
    last_error_timestamp = handle_external_service_error()
    context = {'last_error_timestamp': last_error_timestamp}
    return render(request, 'mailing/mailing_dashboard.html', context)


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'


class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = '__all__'
    success_url= reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = '__all__'
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')
