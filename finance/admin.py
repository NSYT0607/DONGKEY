from django.contrib import admin
from .models import (
    Accounting,
    Classification,
    Income,
    Expenditure
    )

admin.site.register(Accounting)
admin.site.register(Classification)
admin.site.register(Income)
admin.site.register(Expenditure)

