from django.contrib import admin

from .models import AdminResume, ApplicantResume, Question, ShortAnswer, LongAnswer

admin.site.register(AdminResume)
admin.site.register(ApplicantResume)
admin.site.register(Question)
admin.site.register(ShortAnswer)
admin.site.register(LongAnswer)