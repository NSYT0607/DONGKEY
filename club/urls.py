from django.urls import path
from . import views

app_name = 'club'

urlpatterns = [
    path('create/', views.create_club, name='create_club'),
    path('update/<int:club_pk>', views.update_club, name='update_club'),

    path('read_admin_club/<str:club>/<int:ctg_pk>/', views.read_admin_club, name='read_admin_club_ctg'),

    path('<int:pk>/', views.ClubView.as_view(), name='club_view'),
    path('read_admin_club/<str:club>/', views.read_admin_club, name='read_admin_club'),
    path('read_non_admin_club/<str:club>/<int:ctg_pk>/', views.read_non_admin_club, name='read_non_admin_club_ctg'),
    path('read_non_admin_club/<str:club>/', views.read_non_admin_club, name='read_non_admin_club'),
    path('apply/<str:club>/', views.apply_club, name='apply_club'),
    path('admit/<int:club>/<int:pk>/', views.admit, name='admit'),
    path('update_is_admin/<int:club_pk>/<int:user_pk>/', views.update_is_admin, name='update_is_admin'),

    path('manage/<int:club_pk>/', views.manage_member, name='manage_member'),
    path('member_list/<int:club_pk>/non_admin', views.member_list_for_non_admin,
         name='member_list_for_non_admin'),

    path('create/club/rule/<str:club>/', views.create_club_rule, name='create_club_rule'),

    path('read/admin_club/apply_list/<str:club>/', views.read_apply_list, name='read_apply_list'),

    path('read/admin_club/rule/<str:club>/', views.read_admin_club_rule, name='read_admin_club_rule'),
    path('read/non_admin_club/rule/<str:club>/', views.read_non_admin_club_rule, name='read_non_admin_club_rule'),
    path('update/club/rule/<str:club>/<int:rule_pk>/', views.update_club_rule, name='update_club_rule'),
    path('delete/club/rule/<str:club>/<int:rule_pk>/', views.delete_club_rule, name='delete_club_rule'),
    path('exit_club/<int:club_pk>/<int:user_pk>/', views.exit_club, name='exit_club'),
]

