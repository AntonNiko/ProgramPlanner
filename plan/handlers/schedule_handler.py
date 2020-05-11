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
        for schedule in schedules:
            if schedule.name == name:
                response['message'] = 'A schedule with the same name already exists.'
                return response

        schedules.append(Schedule(year=year, term_type=term_type, name=name))
        response['success'] = True

        # Clean-up
        ScheduleHandler.__clean_up(request, profile)
        return response

    @staticmethod
    def get_schedule(request):
        response = ScheduleHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        name = request.GET.get('name')
        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            schedules = profile.saved_schedules
        else:
            schedules = request.session.get('saved_schedules')

        for schedule in schedules:
            if schedule.name == name or (schedule.year == year and schedule.term_type == term_type):
                response['data'] = schedule.to_dict()
                response['success'] = True
                break
        else:
            response['message'] = 'No schedules with the specified parameters exist.'

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

        for schedule in schedules:
            if schedule.name == name:
                schedules.remove(schedule)
                response['success'] = True
                break
        else:
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

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            schedules = profile.saved_schedules
        else:
            schedules = request.session.get('saved_schedules')

        # Fetch the schedule for the specified name
        for schedule in schedules:
            if schedule.name == schedule_name:
                break
        else:
            response['message'] = 'No schedules with the specified name exist.'
            return response

        # Ensure that the section is not already present
        for section in schedule.sections:
            if section.crn == section_to_add.crn:
                response['message'] = 'A section with the same CRN already exists for the specified schedule.'
                return response

        # Evaluate if the section conflicts with currently added sections
        if not ignore_conflicts:
            # TODO: Finish conflict check
            pass

        # Add section to schedule
        schedule.sections.append(section_to_add)
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

        # Fetch the schedule for the specified name
        for schedule in schedules:
            if schedule.name == schedule_name:
                break
        else:
            response['message'] = 'No schedules with the specified name exist.'
            return response

        # Ensure that the section is not already present
        for section in schedule.sections:
            if section.crn == crn:
                schedule.sections.remove(section)
                response['success'] = True
                break
        else:
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
