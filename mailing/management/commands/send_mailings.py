from django.core.management.base import BaseCommand
from mailing.models import Mailing


class Command(BaseCommand):
    help = 'Send mailings'

    def handle(self, *args, **options):
        # Получение всех активных рассылок
        mailings = Mailing.objects.filter(status='created')

        for mailing in mailings:
            mailing.start_scheduled_mailing()