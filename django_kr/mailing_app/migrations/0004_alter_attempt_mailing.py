# Generated by Django 4.2.2 on 2024-08-17 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0003_remove_message_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='mailing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attempt', to='mailing_app.mailing', verbose_name='Рассылка'),
        ),
    ]
