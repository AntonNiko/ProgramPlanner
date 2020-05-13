from typing import Dict, Union
from plan.models import Profile, Section, Schedule


class ScheduleHandler:
    """
    This handles requests associated to the user's schedule.
    """
    RESPONSE_BASE = {'success': False, 'message': '', 'data': None}

    @staticmethod
    def add_schedule(request):
        response = ScheduleHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))
        name = request.GET.get('name')
        assert year is not None
        assert term_type is not None

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            schedules = profile.saved_schedules
        else:
            schedules = request.session.get('saved_schedules')

        # TODO: Improve validation
        assert schedules is not None

        # Ensure that no schedules with the same name exist
        if len(schedules.filter(name=name)) > 0:
            response['message'] = 'A schedule with the same name already exists.'
            return response

        schedule_to_add = Schedule(user=request.user, year=year, term_type=term_type, name=name)
        schedule_to_add.save()
        schedules.add(schedule_to_add)
        response['success'] = True

        # Clean-up
        ScheduleHandler.__clean_up(request, profile)
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
            profile = Profile.objects.get(user=request.user)
            schedules = profile.saved_schedules
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
        name = request.GET.get('name')
        assert name is not None

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            schedules = profile.saved_schedules
        else:
            schedules = request.session.get('saved_schedules')

        try:
            schedule = schedules.get(name=name)
            schedules.remove(schedule)
            response['success'] = True
        except Schedule.DoesNotExist:
            response['message'] = 'No schedules with the specified name exist.'
            return response

        # Clean-up
        ScheduleHandler.__clean_up(request, profile)
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
            profile = Profile.objects.get(user=request.user)
            schedules = profile.saved_schedules
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
            # TODO: Finish conflict check
            pass

        # Add section to schedule
        schedule.sections.add(section_to_add)
        response['success'] = True

        # Clean-up
        ScheduleHandler.__clean_up(request, profile)
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
            profile = Profile.objects.get(user=request.user)
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
        ScheduleHandler.__clean_up(request, profile)
        return response

    @staticmethod
    def __clean_up(request, profile):
        """
        Ensures that either the profile is saved or session modified flag is set.
        """

        if request.user.is_authenticated:
            profile.save()
        else:
            request.session.modified = True
