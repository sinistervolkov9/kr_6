# Generated by Django 4.2.2 on 2024-08-21 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0005_remove_mailing_next_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('can_set_status', 'Can set status')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
