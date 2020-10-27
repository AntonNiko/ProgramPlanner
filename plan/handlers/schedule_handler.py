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

        Currently, only two options are supported:
            1) If id parameter is defined, attempt to return the schedule with that ID,
               provided it belongs to the logged in user
            2) If id parameter not defined, returns all the logged in user's schedules.

        :param request:
        :return:
        """

        # Type-hinting to avoid PyCharm from complaining
        response: Dict[str, Union[bool, str, list]] = ScheduleHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        schedule_id = request.GET.get('id')

        if not request.user.is_authenticated:
            response['success'] = False
            response['message'] = 'Error: user must be authenticated to process this request.'
            return response

        if schedule_id is None:
            schedules = Schedule.objects.filter(user=request.user)
            response['data'] = [schedule.to_dict() for schedule in schedules]
        else:
            schedule = Schedule.objects.get(id=int(schedule_id))
            response['data'] = schedule.to_dict()

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
        Returns the sections associated with the specific user and semester including
        meetings
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
        # TODO: Add more parameter-specific queries

        # Fetch the schedule associated with the request
        schedule = Schedule.objects.filter(user=request.user).get(id=schedule_id)

        # Fetch all sections associated with the schedule
        sections_references = ScheduleSection.objects.filter(schedule=schedule).values('section')
        sections = []
        for section_reference in sections_references:
            sections.append(Section.objects.get(crn=section_reference["section"]))

        # Fetch the associated course offering and meetings
        for i in range(len(sections)):
            section_dict = sections[i].to_dict()
            section_dict.update(sections[i].course_offering.to_dict())
            section_dict["meetings"] = [meeting.to_dict() for meeting in Meeting.objects.filter(section=sections[i])]
            sections[i] = section_dict

        response['data'] = sections
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
