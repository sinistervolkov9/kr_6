# Generated by Django 4.2.2 on 2024-08-21 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_alter_blogpost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, default='img.png', null=True, upload_to='blog_images/', verbose_name='Изображение'),
        ),
    ]
