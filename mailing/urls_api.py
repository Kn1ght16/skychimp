from django.urls import path
from .views import MailingStartView, MailingStatsView

app_name = 'mailing'

urlpatterns = [
    path('start/<int:pk>/', MailingStartView.as_view(), name='start'),
    path('stats/<int:pk>/', MailingStatsView.as_view(), name='stats'),
]