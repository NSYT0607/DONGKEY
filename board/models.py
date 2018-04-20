from django.db import models
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=15, verbose_name='카테고리명')

    def __str__(self):
        return self.name


class Article(models.Model):
    club = models.ForeignKey(
        'club.CLub',
        on_delete=models.CASCADE,
        )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=20, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    hit = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name = 'hit_article_set',
        )
    coordinate = models.CharField(max_length=100, null=True, blank=True, verbose_name='좌표')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    liker_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_article_set',
    )

    def __str__(self):
        return '{0}:{1}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse('board:article_detail', kwargs={'pk': self.pk, })


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )

    liker_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_comment_set',
    )

    content = models.CharField(max_length=100, verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
