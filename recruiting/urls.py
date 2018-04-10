from django.urls import path
from . import views

app_name = 'recruiting'

urlpatterns = [
    # 지원서 양식 관리 리스트 ##ADMIN
    path('<int:club_pk>/admin_resume_list/for_admin', views.admin_resume_list_for_admin,
         name='admin_resume_list_for_admin'),

    # 지원서 만들고 항목 작성 ##ADMIN
    path('<int:club_pk>/create_admin', views.create_admin_resume, name='create_admin_resume'),
    path('<int:club_pk>/<int:resume_pk>/read_admin', views.read_admin_resume, name='read_admin_resume'),
    path('<int:club_pk>/<int:resume_pk>/create_question/', views.create_question,
         name='create_question'),
    path('<int:question_pk>/update_question', views.update_question,
         name='update_question'),
    path('<int:question_pk>/delete_question', views.delete_question,
         name='delete_question'),

    # 지원서 양식 별 지원자 관리_해당 지원서 양식의 지원자 리스트 & 개별 지원자 지원서 보기 ##ADMIN
    path('<int:club_pk>/<int:resume_pk>/applicant_list/', views.read_applicant_resume_list,
         name='read_applicant_resume_list'),
    path('<int:club_pk>/<int:resume_pk>/read_applicant/for_admin',
         views.read_applicant_resume_for_admin, name='read_applicant_resume_for_admin'),
    path('<int:resume_pk>/accept_applicant', views.accept_applicant, name='accept_applicant'),

    # 지원서 양식 별 지원서 작성하기_지원서 양식 리스트 & 지원서 작성 ##APPLICANT
    path('<int:club_pk>/admin_resume_list/for_applicant', views.admin_resume_list_for_applicant,
         name='admin_resume_list_for_applicant'),
    path('<int:club_pk>/<int:resume_pk>/create_applicant/', views.create_applicant_resume,
         name='create_applicant_resume'),
    path('<int:club_pk>/<int:resume_pk>/read_applicant/', views.read_applicant_resume_for_applicant,
         name='read_applicant_resume_for_applicant'),
    path('<int:resume_pk>/delete_applicant/', views.delete_applicant_resume,
         name='delete_applicant_resume'),
]
