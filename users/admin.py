from django.contrib import admin
from users.models import User, BlogArticle
from mailing.models import Mailing

admin.site.register(User)
admin.site.register(Mailing)
admin.site.register(BlogArticle)
