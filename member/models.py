from django.db import models
from django.conf import settings


class Member(models.Model):
    club = models.ForeignKey(
            'club.Club',
            on_delete=models.CASCADE,
        )
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
        )
    is_admin = models.BooleanField(
            default=False,
        )
    # positon False=member, True=admin

    def __str__(self):
        return '{0} : {1}'.format(self.club, self.user)