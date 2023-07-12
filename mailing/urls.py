from django.urls import path
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
    HomeView,
    BlogListView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
)


app_name = 'mailing'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailing/list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/start/<int:pk>/', MailingStartView.as_view(), name='mailing_start'),
    path('mailing/stats/<int:pk>/', MailingStatsView.as_view(), name='mailing_stats'),
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]