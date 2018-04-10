from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('<int:pk>/accounting/', views.club_accounting, name='club_accounting'),
    path('<int:pk>/accounting/search_by_date/', views.search_by_date, name='search_by_date'),

    path('<int:pk>/accounting/non_admin', views.non_admin_club_accounting,
         name='non_admin_club_accounting'),
]