# Generated by Django 4.2.2 on 2024-08-22 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_user_verify_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verify_code',
            field=models.CharField(default='816743', max_length=6, verbose_name='Код верификации'),
        ),
    ]
