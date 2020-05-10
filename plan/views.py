from django.http import JsonResponse, HttpResponse
from django.template import loader
from .handlers import AccountHandler, DataHandler, PageHandler, PlanHandler

JSON_RESPONSE_BASE = {'method': None, 'response': None}


def view_home(request):
    http_response = PageHandler.get_home_view(request)
    return http_response


def view_program(request):
    http_response = PageHandler.get_program_view(request)
    return http_response


def view_schedule(request):
    http_response = PageHandler.get_schedule_view(request)
    return http_response


def view_account(request):
    http_response = PageHandler.get_account_view(request)
    return http_response


def api_account_authentication(request):
    # TODO: Better validation
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'account_authentication'

    action = request.GET.get('action')
    if action == 'login':
        assert request.method == 'POST'
        response_json['response'] = AccountHandler.login(request)
    elif action == 'logout':
        assert request.method == 'GET'
        response_json['response'] = AccountHandler.logout(request)

    return JsonResponse(response_json)


def api_data_course(request):
    # TODO: Better validation
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'data_course'

    assert request.method == 'GET'

    response_json['response'] = DataHandler.get_course_data(request)

    return JsonResponse(response_json)


def api_data_program(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'data_program'

    action = request.GET.get('action')
    if action == 'get':
        assert request.method == 'GET'
        response_json['response'] = DataHandler.get_program_data(request)

    return JsonResponse(response_json)


def api_plan_course(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'plan_course'

    action = request.GET.get('action')
    if action == 'add':
        assert request.method == 'GET'
        response_json['response'] = PlanHandler.add_course_to_active_sequence(request)
    elif action == 'remove':
        assert request.method == 'GET'
        response_json['response'] = PlanHandler.remove_course_from_active_sequence(request)
    else:
        response_json['response'] = 'unsupported parameters'

    return JsonResponse(response_json)


def api_plan_program(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'plan_program'

    action = request.GET.get('action')
    if action == 'add':
        response_json['response'] = PlanHandler.add_program(request)
    elif action == 'get':
        pass
    elif action == 'evaluate':
        pass
    elif action == 'remove':
        pass

    return JsonResponse(response_json)


def api_plan_sequence(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'plan_sequence'

    action = request.GET.get('action')
    if action == 'add':
        response_json['response'] = PlanHandler.add_active_sequence(request)
    elif action == 'get':
        response_json['response'] = PlanHandler.get_active_sequence(request)

    return JsonResponse(response_json)


def api_plan_term(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'plan_term'

    action = request.GET.get('action')
    if action == 'add':
        response_json['response'] = PlanHandler.add_term(request)
    elif action == 'remove':
        response_json['response'] = PlanHandler.remove_term(request)

    return JsonResponse(response_json)


def api_schedule(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'schedule'

    action = request.GET.get('action')
    # TODO: Complete
    if action == 'add':
        pass
    elif action == 'remove':
        pass

    return JsonResponse(response_json)


def api_schedule_section(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'schedule_section'

    action = request.GET.get('action')
    # TODO: Complete 
    if action == 'add':
        pass
    elif action == 'remove':
        pass

    return JsonResponse(response_json)
