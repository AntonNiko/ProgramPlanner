from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import render
from .handlers import AccountHandler, DataHandler, PlanHandler

JSON_RESPONSE_BASE = {'method': None, 'response_data': None}

# Create your views here.
def view_index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def view_schedule(request):    
    template = loader.get_template('schedule.html')
    return HttpResponse(template.render({}, request))

def view_account(request):
    template = loader.get_template('account.html')
    return HttpResponse(template.render({}, request))

def account_authentication(request):
    # TODO: Better validation
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'account_authentication'

    action = request.GET.get('action')
    if action == 'login':
        assert request.method == 'POST'
        response_json['response_data'] = AccountHandler.login(request)
    elif action == 'logout':
        assert request.method == 'GET'
        response_json['response_data'] = AccountHandler.logout(request)

    return JsonResponse(response_json)

def data_course(request):
    # TODO: Better validation
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'data_course'

    assert request.method == 'GET'

    response_json['response_data'] = DataHandler.get_course_data(request)
    
    return JsonResponse(response_json)

def data_program(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'data_program'

    action = request.GET.get('action')
    if action == 'get':
        assert request.method == 'GET'
        response_json['response_data'] = DataHandler.get_program_data(request)

    return JsonResponse(response_json)

def plan_course(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'plan_course'

    action = request.GET.get('action')
    if action == 'add':
        assert request.method == 'GET'
        response_json['response_data'] = PlanHandler.add_course_to_sequence(request)
    elif action == 'remove':
        assert request.method == 'GET'
        response_json['response_data'] = PlanHandler.remove_course_from_sequence(request)
    else:
        response_json['response_data'] = 'unsupported parameters'

    return JsonResponse(response_json)

def plan_program(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'plan_program'

    action = request.GET.get('action')
    if action == 'add':
        response_json['response_data'] = PlanHandler.add_program(request)
    elif action == 'get':
        pass
    elif action == 'remove':
        pass 

    return JsonResponse(response_json)

def plan_sequence(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'plan_sequence'

    response_json['response_data'] = PlanHandler.get_sequence(request)
    return JsonResponse(response_json)

def plan_term(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'plan_term'

    action = request.GET.get('action')
    if action == 'add':
        assert request.method == 'GET'
        PlanHandler.add_term(request)
    elif action == 'remove':
        assert request.method == 'POST'
        PlanHandler.remove_term(request)
    
    return JsonResponse(response_json)

def schedule(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'schedule'

    return JsonResponse(response_json)

def schedule_section(request):
    response_json = JSON_RESPONSE_BASE.copy()
    response_json['method'] = 'schedule_section'

    return JsonResponse(response_json)