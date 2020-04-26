from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_index, name='index'),
    path('schedule', views.view_schedule, name='schedule'),
    path('account', views.view_account, name='account'),
    path('api/account/authentication/login', views.account_authentication_login, name='login'),
    path('api/account/authentication/logout', views.account_authentication_logout, name='logout'),
    path('api/data/course', views.data_course_get, name='course'),
    path('api/data/program', views.data_program_get, name='program'),
    path('api/plan/course/add', views.plan_course_add, name='course_add'),
    path('api/plan/course/remove', views.plan_course_remove, name='course_remove'),
    path('api/plan/program', views.plan_program, name='program_get'),
    path('api/plan/program/add', views.plan_program_add, name='program_add'),
    path('api/plan/program/remove', views.plan_program_remove, name='program_remove'),
    path('api/plan/sequence', views.plan_sequence, name='sequence'),
    path('api/plan/term/add', views.plan_term_add, name='term_add'),
    path('api/plan/term/remove', views.plan_term_remove, name='term_remove'),
    path('api/schedule/', views.schedule, name='schedule'),
    path('api/schedule/section/add', views.schedule_section_add, name='section_add'),
    path('api/schedule/section/remove', views.schedule_section_remove, name='section_remove')
]