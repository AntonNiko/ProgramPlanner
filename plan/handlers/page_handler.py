from django.http import HttpResponse
from django.template import loader


class PageHandler:

    @staticmethod
    def get_home_view(request):
        template = loader.get_template('base_home.html')
        http_response = HttpResponse(template.render({}, request))
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
    def get_account_view(request):
        template = loader.get_template('base_account.html')
        http_response = HttpResponse(template.redner({}, request))
        return http_response
