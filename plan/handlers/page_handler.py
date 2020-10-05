#  Copyright (c) 2020. by Anton Nikitenko
#  All rights reserved.

from django.http import HttpResponse
from django.template import loader
from plan.models import Schedule


class PageHandler:

    @staticmethod
    def get_home_view(request):
        template = loader.get_template('base_home.html')

        context = {}
        if request.user.is_authenticated:
            context["schedules"] = Schedule.objects.filter(user=request.user)

        print(type(context["schedules"][0].term))
        http_response = HttpResponse(template.render(context, request))
        return http_response

    @staticmethod
    def get_program_view(request):
        template = loader.get_template('base_program.html')
        http_response = HttpResponse(template.render({}, request))
        return http_response

    @staticmethod
    def get_schedule_view(request):
        template = loader.get_template('base_schedule.html')
        http_response = HttpResponse(template.render({}, request))
        return http_response

    @staticmethod
    def get_schedule_add_view(request):
        template = loader.get_template('base_schedule_add.html')
        http_response = HttpResponse(template.render({}, request))
        return http_response

    @staticmethod
    def get_account_view(request):
        template = loader.get_template('base_account.html')
        http_response = HttpResponse(template.render({}, request))
        return http_response
