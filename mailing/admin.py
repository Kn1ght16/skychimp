from django.contrib import admin
from mailing.models import BlogArticle, Client, Mailing, Message, DeliveryAttempt

admin.site.register(BlogArticle)
admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Message)
admin.site.register(DeliveryAttempt)