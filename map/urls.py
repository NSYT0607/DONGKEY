from django.urls import path
from . import views

app_name = 'map'

urlpatterns = [
    path('', views.map, name='map'),
    path('search/<str:mapx>/<str:mapy>/', views.return_coord, name='return_coord'),
]
