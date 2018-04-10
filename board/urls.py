from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('admin/list/<int:club_pk>/', views.article_list, name='article_list_admin'),
    path('list/<int:club_pk>/', views.article_list, name='article_list'),
    path('ctg/<int:club_pk>/<int:ctg_pk>/', views.article_list, name='article_list_by_ctg'),
    path('admin/create/<int:club_pk>', views.article_create_admin, name='article_create_admin'),
    path('create/<int:club_pk>', views.article_create, name='article_create'),
    path('admin/<int:pk>/', views.article_detail_admin, name='article_detail_admin'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    path('admin/update/<int:pk>/', views.article_update_admin, name='article_update_admin'),
    path('update/<int:pk>/', views.article_update, name='article_update'),
    path('admin/delete/<int:pk>/', views.article_delete_admin, name='article_delete_admin'),
    path('delete/<int:pk>/', views.article_delete, name='article_delete'),
    path('like/<int:pk>/', views.article_like, name='article_like'),
    path('comment_like/<int:pk>/', views.comment_like, name='comment_like'),

]