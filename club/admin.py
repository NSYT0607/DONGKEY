from django.contrib import admin

from .models import Club
from .models import ClubRule
from .models import ApplyList
# Register your models here.


admin.site.register(Club)
admin.site.register(ApplyList)
admin.site.register(ClubRule)
