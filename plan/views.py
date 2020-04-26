from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import render
from handlers import AccountHandler, DataHandler

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

def account_authentication_login(request):
    assert request.method == 'POST'
    # TODO: Better validation

    AccountHandler.login(request)

    return HttpResponse("This will handle the login request.")

def account_authentication_logout(request):
    assert request.method == 'POST'
    # TODO: Better validation

    AccountHandler.logout(request)
    return HttpResponse("This will handle the logout request.")

def data_course_get(request):
    assert request.method == 'GET'
    # TODO: Better validation

    data = DataHandler.get_course_data(request)
    return JsonResponse(data)

def data_program_get(request):
    return HttpResponse("This will get the Program data.")

def plan_course_add(request):
    return HttpResponse("This will add the provided course to the schedule.")

def plan_course_remove(request):
    return HttpResponse("This will remove the provided course from the schedule.")

def plan_program(request):
    return HttpResponse("This will return the current program(s) selected.")

def plan_program_add(request):
    return HttpResponse("This will add the specificed program to the selection list.")

def plan_program_remove(request):
    return HttpResponse("This will remove the specified program from the selection list.")

def plan_sequence(request):
    return HttpResponse("This will get the current sequence.")

def plan_term_add(request):
    return HttpResponse("This will add a term to the sequence")

def plan_term_remove(request):
    return HttpResponse("This will remove a term from the sequence.")

def schedule(request):
    return HttpResponse("Gets the active schedule(s).")

def schedule_section_add(request):
    return HttpResponse("This will add a section to the schedule for a specific term.")

def schedule_section_remove(request):
    return HttpResponse("This will remove a section from the schedule for a specific term.")