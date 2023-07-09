from datetime import datetime

from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Client(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    comment = models.TextField()

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mailing(models.Model):
    START_TIME_CHOICES = [
        ('00:00', '00:00'),
        ('01:00', '01:00'),
        ('02:00', '02:00'),
        ('03:00', '03:00'),
        ('04:00', '04:00'),
        ('05:00', '05:00'),
        ('06:00', '06:00'),
        ('07:00', '07:00'),
        ('08:00', '08:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
        ('22:00', '22:00'),
        ('23:00', '23:00'),
    ]
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]
    STATUS_CHOICES = [
        ('completed', 'Завершено'),
        ('created', 'Создано'),
        ('started', 'Запущено'),
    ]

    start_time = models.CharField(
        max_length=5,
        choices=START_TIME_CHOICES,
        verbose_name='время начала'
    )
    frequency = models.CharField(
        max_length=255,
        choices=FREQUENCY_CHOICES,
        verbose_name='периодичность'
    )
    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        verbose_name='статус'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    clients = models.ManyToManyField(Client, verbose_name='клиенты')

    def send_messages(self):
        clients = self.clients.all()
        message = Message.objects.first()
        for client in clients:
            sent_datetime = datetime.now()
            try:
                # Отправка сообщения
                send_mail(message.subject, message.body, 'your_email@example.com', [client.email])
                status = 'отправлено'
                server_response = 'Сообщение отправлено успешно'
            except Exception as e:
                # Обработка ошибок отправки
                status = 'ошибка'
                server_response = str(e)

            DeliveryAttempt.objects.create(
                timestamp=sent_datetime,
                status=status,
                response=server_response,
                client=client,
                mailing=self,
                message=message
            )

    def start_scheduled_mailing(self):
        now = datetime.now().time()
        start_time = datetime.strptime(self.start_time, '%H:%M').time()

        if start_time <= now and self.status == 'created':
            self.status = 'started'
            self.save()
            self.send_messages()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.start_scheduled_mailing()

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='тема')
    body = models.TextField(verbose_name='тело')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class DeliveryAttempt(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='время')
    status = models.CharField(max_length=255, verbose_name='статус')
    response = models.TextField(verbose_name='ответ')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')

    class Meta:
        verbose_name = 'попытка доставки'
        verbose_name_plural = 'попытки доставки'
