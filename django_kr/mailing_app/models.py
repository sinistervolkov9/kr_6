from django.db import models
from django.conf import settings
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}

PERIODICITY_CHOICES = (
    ('one time', 'разовая'),
    ('day', 'Раз в день'),
    ('week', 'Раз в неделю'),
    ('month', 'Раз в месяц'),
)

STATUS_CHOICES = (
    ('created', 'Создана'),
    ('started', 'Запущена'),
    ('completed', 'Завершена'),
)

STATUS_ATTEMPT = (
    ('ok', 'Успешно'),
    ('false', 'Ошибка'),
)


class Client(models.Model):
    email = models.EmailField(verbose_name='Почта', unique=True)
    full_name = models.CharField(max_length=150, verbose_name='Ф. И. О.')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, related_name='clients',
                             verbose_name='Пользователь')

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема')
    text = models.TextField(verbose_name='Содержание')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', default=1, on_delete=models.CASCADE,
                             verbose_name='пользователь')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50)
    date_time = models.DateTimeField(default=timezone.now, verbose_name="Дата и время для разовых", **NULLABLE)

    start_date = models.DateTimeField(default=timezone.now, verbose_name="Начало периода", **NULLABLE)
    next_date = models.DateTimeField(default=timezone.now, verbose_name="Следующая отправка")  # А зачем?
    end_date = models.DateTimeField(default=timezone.now, verbose_name="Конец периода", **NULLABLE)
    periodicity = models.CharField(default='one time', max_length=50, verbose_name="Периодичность", choices=PERIODICITY_CHOICES)

    client = models.ManyToManyField(Client, verbose_name='Клиент')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='newsletters', on_delete=models.CASCADE,
                             verbose_name='Пользователь')

    def __str__(self):
        return f'{self.message}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    permissions = [
        (
            'set_status',
            'Can change status'
        )
    ]


class Attempt(models.Model):
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='Рассылка', related_name='attempt', **NULLABLE)

    attempt_time = models.DateTimeField(default=timezone.now, verbose_name="Время последней рассылки", **NULLABLE)
    status = models.CharField(max_length=50, choices=STATUS_ATTEMPT, verbose_name='Статус')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='logs', on_delete=models.CASCADE,
                             verbose_name='Пользователь')

    def __str__(self):
        return f'Отправлено: {self.attempt_time}\nСтатус: {self.status}'

    class Meta:
        verbose_name = 'Попытка рассыкли'
        verbose_name_plural = 'Попытки рассылки'
