from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_program, name='program'),
    path('schedule', views.view_schedule, name='schedule'),
    path('account', views.view_account, name='account'),
    path('api/account/authentication', views.api_account_authentication, name='account_authentication'),
    path('api/data/course', views.api_data_course, name='data_course'),
    path('api/data/program', views.api_data_program, name='data_program'),
    path('api/plan/course', views.api_plan_course, name='plan_course'),
    path('api/plan/program', views.api_plan_program, name='plan_program'),
    path('api/plan/sequence', views.api_plan_sequence, name='plan_sequence'),
    path('api/plan/term', views.api_plan_term, name='plan_term'),
    path('api/schedule/', views.api_schedule, name='schedule'),
    path('api/schedule/section', views.api_schedule_section, name='schedule_section')
]