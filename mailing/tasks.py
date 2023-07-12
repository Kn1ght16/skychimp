from django_cron import CronJobBase, Schedule
from .models import Mailing


class SendScheduledMailings(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'mailing.send_scheduled_mailings'

    def do(self):
        mailings = Mailing.objects.filter(status='created')
        for mailing in mailings:
            mailing.send_messages()
