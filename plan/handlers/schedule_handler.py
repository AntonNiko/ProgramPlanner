#  Copyright (c) 2020. by Anton Nikitenko
#  All rights reserved.

from typing import Dict, Union
from plan.models import ScheduleSection, Section, Schedule, Meeting


class ScheduleHandler:
    """
    This handles requests associated to the user's schedule.
    """
    RESPONSE_BASE = {'success': False, 'message': '', 'data': None}

    @staticmethod
    def add_schedule(request):
        response = ScheduleHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        year = int(request.POST.get('year'))
        term = int(request.POST.get('term'))
        name = request.POST.get('name')
        assert year is not None
        assert term is not None

        if request.user.is_authenticated:
            schedules = Schedule.objects.filter(user=request.user)
        else:
            schedules = request.session.get('saved_schedules')

        # Ensure that no schedules with the same name exist
        if schedules is not None and len(schedules.filter(name=name)) > 0:
            response['message'] = 'A schedule with the same name already exists.'
            return response

        schedule = Schedule.objects.create(user=request.user, year=year, term=term, name=name)
        response['success'] = True

        # Clean-up
        ScheduleHandler.__clean_up(request, None)
        return response

    @staticmethod
    def get_schedule(request):
        """
        Returns a response with the requested schedule data for a specific user profile or
        user session.

        Three options are accepted for the GET parameters, resulting in 3 different responses:
          - `name` is defined, but neither the `year` or `term_type`.
          - `year` and `term_type` are defined, but `name` is undefined.
          - Neither of those

        :param request:
        :return:
        """

        # Type-hinting to avoid PyCharm from complaining
        response: Dict[str, Union[bool, str, list]] = ScheduleHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        name = request.GET.get('name')
        year = int(request.GET.get('year')) if request.GET.get('year') is not None else None
        term_type = int(request.GET.get('term_type')) if request.GET.get('term_type') is not None else None

        if request.user.is_authenticated:
            schedules = Schedule.objects.filter(user=request.user)
        else:
            schedules = request.session.get('saved_schedules')

        if name is not None:
            response['data'] = [schedule.to_dict() for schedule in schedules.filter(name__exact=name)]
            response['success'] = True
        elif year is not None and term_type is not None:
            response['data'] = [schedule.to_dict() for schedule in schedules.filter(year__exact=year).filter(term_type__exact=term_type)]
            response['success'] = True
        elif year is None and term_type is None:
            response['data'] = [schedule.to_dict() for schedule in schedules.all()]
            response['success'] = True
        # Invalid request parameters
        else:
            response['message'] = 'Invalid request parameter values'

        return response

    @staticmethod
    def remove_schedule(request):
        response = ScheduleHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        schedule_id = request.POST.get('schedule-id')
        assert schedule_id is not None

        if request.user.is_authenticated:
            schedules = Schedule.objects.filter(user=request.user)
        else:
            schedules = request.session.get('saved_schedules')

        try:
            schedule = schedules.get(id__exact=schedule_id)
            schedule.delete()
            response['success'] = True
        except Schedule.DoesNotExist:
            response['message'] = 'No schedules with the specified name exist.'
            return response

        # Clean-up
        ScheduleHandler.__clean_up(request, None)
        return response

    @staticmethod
    def add_section(request):
        response = ScheduleHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        schedule_name = request.GET.get('schedule_name')
        crn = int(request.GET.get('crn'))
        ignore_conflicts = True if request.GET.get('ignore_conflicts') == 'true' else False
        assert schedule_name is not None
        assert crn is not None
        assert ignore_conflicts is not None

        # Fetch section to add.
        section_to_add = Section.objects.get(crn=crn)

        # Fetch user's schedules
        if request.user.is_authenticated:
            schedules = Schedule.objects.filter(user=request.user)
        else:
            schedules = request.session.get('saved_schedules')

        try:
            schedule = schedules.get(name=schedule_name)
        except Schedule.DoesNotExist:
            response['message'] = 'No schedules with the specified name exist.'
            return response

        # Ensure that the section is not already present
        if len(schedule.sections.filter(crn=crn)) > 0:
            response['message'] = 'A section with the same CRN already exists for the specified schedule.'
            return response

        # Evaluate if the section conflicts with currently added sections
        if not ignore_conflicts:
            conflict_results = schedule.does_section_conflict(section_to_add)
            if conflict_results['conflicts']:
                response['data'] = conflict_results['data']
                return response

        # Add section to schedule
        schedule.sections.add(section_to_add)
        response['success'] = True

        # Clean-up
        ScheduleHandler.__clean_up(request, None)
        return response

    @staticmethod
    def remove_section(request):
        response = ScheduleHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        schedule_name = request.GET.get('schedule_name')
        crn = int(request.GET.get('crn'))
        assert schedule_name is not None
        assert crn is not None

        if request.user.is_authenticated:
            schedules = Schedule.objects.filter(user=request.user)
            schedules = profile.saved_schedules
        else:
            schedules = request.session.get('saved_schedules')

        # Remove the section from specified schedule
        try:
            schedule = schedules.get(name=schedule_name)
            section = schedule.sections.get(crn=crn)
            schedule.sections.remove(section)
            response['success'] = True

        except Schedule.DoesNotExist:
            response['message'] = 'No schedules with the specified name exist.'
            return response

        except Section.DoesNotExist:
            response['message'] = 'No sections with the specified CRN exist in the specified schedule.'
            return response

        # Clean-up
        ScheduleHandler.__clean_up(request, None)
        return response

    @staticmethod
    def get_section(request):
        """
        Returns the sections associated with the specific user and semester
        :param request:
        :return:
        """

        response = ScheduleHandler.RESPONSE_BASE.copy()

        if not request.user.is_authenticated:
            response['success'] = False
            return response

        schedule_id = int(request.GET.get('id'))
        assert schedule_id is not None

        # At this point, only gets all sections associated with user
        # TODO: Add more parameter specific queries

        # Fetch the schedule associated with the request
        schedule = Schedule.objects.filter(user=request.user).get(id=schedule_id)

        # Fetch all sections associated with the schedule
        sections_references = ScheduleSection.objects.filter(schedule=schedule).values('section')
        sections = []
        for section_reference in sections_references:
            sections.append(Section.objects.get(crn=section_reference["section"]))

        response['data'] = [section.to_dict() for section in sections]
        response['success'] = True

        # Clean-up
        ScheduleHandler.__clean_up(request, None)
        return response

    @staticmethod
    def get_meeting(request):
        """
        At this point, this method only returns all the meetings associated with a CRN

        :param request:
        :return:
        """

        response = ScheduleHandler.RESPONSE_BASE.copy()

        crn = int(request.GET.get('crn'))
        assert crn is not None

        # Fetch the section with the corresponding CRN
        section = Section.objects.get(crn=crn)

        # Query all meetings with foreign key
        meetings = Meeting.objects.filter(section=section)

        response['data'] = [meeting.to_dict() for meeting in meetings]
        response['success'] = True

        ScheduleHandler.__clean_up(request, None)
        return response

    @staticmethod
    def __clean_up(request, profile):
        """
        Ensures that either the profile is saved or session modified flag is set.
        """

        #if request.user.is_authenticated:
        #    profile.save()
        #else:
        #    request.session.modified = True
