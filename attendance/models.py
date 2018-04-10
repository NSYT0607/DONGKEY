from django.db import models
from club.models import Club
from member.models import Member


class Event(models.Model):
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        )
    title = models.CharField(max_length=50, verbose_name='일정 제목')
    description = models.TextField(verbose_name='일정 내용', blank=True)
    event_at = models.DateTimeField(verbose_name='일정 시간')
    absent_member = models.ManyToManyField(Member, blank=True, default=None)

