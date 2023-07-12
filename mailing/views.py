from datetime import timezone

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from .models import Mailing, Client, Message, DeliveryAttempt, BlogArticle
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'


class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    fields = '__all__'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        message_subject = self.request.POST.get('subject')
        message_body = self.request.POST.get('body')
        message = Message.objects.create(subject=message_subject, body=message_body)
        self.object = form.save(commit=False)
        self.object.message = message
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    fields = '__all__'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        message_subject = self.request.POST.get('subject')
        message_body = self.request.POST.get('body')
        message, created = Message.objects.get_or_create(subject=message_subject, body=message_body)
        self.object = form.save(commit=False)
        self.object.message = message
        self.object.save()
        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingStartView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        clients = mailing.clients.all()
        message = mailing.message
        sent_datetime = timezone.now()
        try:
            # Генерация текстового и HTML-сообщения
            text_message = render_to_string('mailing/email.txt', {'message': message})
            html_message = render_to_string('mailing/email.html', {'message': message})

            for client in clients:
                # Отправка сообщения
                email = EmailMultiAlternatives(
                    message.subject,
                    text_message,
                    'your_email@example.com',
                    [client.email]
                )
                email.attach_alternative(html_message, 'text/html')
                email.send()

                DeliveryAttempt.objects.create(
                    timestamp=sent_datetime,
                    status='отправлено',
                    response='Сообщение отправлено успешно',
                    client=client,
                    mailing=mailing,
                    message=message
                )

            status = 'отправлено'
        except Exception as e:
            status = 'ошибка'

        context = {'mailing': mailing, 'status': status}
        return render(request, 'mailing/mailing_start.html', context)

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        status = mailing.send_messages()  # Отправка сообщений и получение статуса выполнения
        context = {'mailing': mailing, 'status': status}  # Передача статуса в контекст
        return render(request, 'mailing/mailing_start.html', context)


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
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = '__all__'
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')


class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='started').count()
        context['unique_clients'] = Client.objects.count()
        context['random_articles'] = BlogArticle.objects.order_by('?')[:3]
        return context

    @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BlogListView(ListView):
    model = BlogArticle
    template_name = 'mailing/blog_list.html'
    context_object_name = 'articles'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogArticle
    template_name = 'mailing/blog_create.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('mailing:blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogArticle
    template_name = 'mailing/blog_update.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('mailing:blog_list')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_staff


class BlogDeleteView(DeleteView):
    model = BlogArticle
    template_name = 'mailing/blog_confirm_delete.html'
    success_url = reverse_lazy('mailing:blog_list')