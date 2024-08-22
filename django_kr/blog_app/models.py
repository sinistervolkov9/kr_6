from django.db import models
from django.conf import settings
from django.utils.text import slugify

NULLABLE = {'blank': True, 'null': True}


class BlogPost(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    content = models.TextField(verbose_name='Содержимое статьи', )
    image = models.ImageField(verbose_name='Изображение', **NULLABLE, upload_to='blog_images/', default='img.png')
    views = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)
    published_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, related_name='blogs',
                             verbose_name='Пользователь')

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
