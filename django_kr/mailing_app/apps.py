from django.apps import AppConfig

scheduler = None

class MailingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing_app'
