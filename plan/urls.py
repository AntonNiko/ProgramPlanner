from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_home, name='home'),
    path('program', views.view_program, name='program'),
    path('schedule', views.view_schedule, name='schedule'),
    path('schedule/add', views.view_schedule_add, name='schedule_add'),
    path('account', views.view_account, name='account'),
    path('account/login', views.account_login, name='account_login'),
    path('account/logout', views.account_logout, name='account_logout'),
    path('account/register', views.account_register, name='account_register'),
    path('api/data/course', views.api_data_course, name='api_data_course'),
    path('api/data/program', views.api_data_program, name='api_data_program'),
    path('api/plan/course', views.api_plan_course, name='api_plan_course'),
    path('api/plan/program', views.api_plan_program, name='api_plan_program'),
    path('api/plan/sequence', views.api_plan_sequence, name='api_plan_sequence'),
    path('api/plan/term', views.api_plan_term, name='api_plan_term'),
    path('api/schedule/add', views.api_schedule_add, name='api_schedule_add'),
    path('api/schedule/get', views.api_schedule_get, name='api_schedule_get'),
    path('api/schedule/remove', views.api_schedule_remove, name='api_schedule_remove'),
    #path('api/schedule/section', views.api_schedule_section, name='api_schedule_section'),
    path('api/section/get', views.api_section_get, name='api_section_get')
]