from django.db import models
from django.dispatch import receiver
from django.conf import settings
from schedule.models import Calendar

from finance.models import Accounting


class Club(models.Model):
    name = models.CharField(
            max_length=50,
            verbose_name='동아리 이름',
        )
    image = models.ImageField(
            verbose_name='동아리 이미지',
            upload_to='club/%Y/%m/%d/',
            blank=True,
            null=True,
        )
    description = models.TextField(
            verbose_name='동아리 설명',
            blank=True,
            null=True,
        )
    calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


@receiver(models.signals.post_save, sender=Club)
def create_accounting(sender, instance, **kwargs):
    if not hasattr(instance, 'accounting'):
        Accounting.objects.create(club=instance)


class ApplyList(models.Model):
    club = models.ForeignKey(
            Club,
            on_delete=models.CASCADE,
        )
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
        )

    def __str__(self):
        return '{0} : {1}'.format(self.club, self.user)


class ClubRule(models.Model):
    main_theme = models.CharField(
            max_length=30,
            verbose_name='회칙 항목 대분류',
        )
    sub_theme = models.CharField(
            max_length=30,
            verbose_name='회칙 항목 소분류',
            blank=True,
            null=True,
        )
    rule = models.TextField(verbose_name='회칙 내용')
    club = models.ForeignKey(
            Club,
            on_delete=models.CASCADE,
        )

    def __str__(self):
        return self.main_theme
