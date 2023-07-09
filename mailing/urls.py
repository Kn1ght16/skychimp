from django.urls import path
from django.views.generic import RedirectView
from .views import (
    MailingListView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingStartView,
    MailingStatsView,
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
)


app_name = 'mailing'

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('start/<int:pk>/', MailingStartView.as_view(), name='mailing_start'),
    path('stats/<int:pk>/', MailingStatsView.as_view(), name='mailing_stats'),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('', RedirectView.as_view(url='mailing/', permanent=False)),
]