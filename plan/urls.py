from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_index, name='index'),
    path('schedule', views.view_schedule, name='schedule'),
    path('account', views.view_account, name='account'),
    path('api/account/authentication', views.account_authentication, name='account_authentication'),
    path('api/data/course', views.data_course, name='data_course'),
    path('api/data/program', views.data_program, name='data_program'),
    path('api/plan/course', views.plan_course, name='plan_course'),
    path('api/plan/program', views.plan_program, name='plan_program'),
    path('api/plan/sequence', views.plan_sequence, name='plan_sequence'),
    path('api/plan/term', views.plan_term, name='plan_term'),
    path('api/schedule/', views.schedule, name='schedule'),
    path('api/schedule/section', views.schedule_section, name='schedule_section')
]