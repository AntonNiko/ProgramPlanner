from plan.models import Course, Profile, Program, Sequence, Term


# TODO: Refactor class to properly handle anonymous, session-based requests.
# TODO: Refactor class to properly catch any relevant errors or exceptions


class SequenceHandler:
    """
    This handles requests and manages user-specific information regarding their program plan.

    To handle requests, the user must either have an existing session, or be logged in.
    """
    RESPONSE_BASE = {'success': False, 'message': '', 'data': None}

    @staticmethod
    def add_course_to_active_sequence(request):
        """
        Adds a course to the user's sequence. To correctly add a course, the following parameters
        must be specified:
          - subject: Course subject (e.g 'CSC')
          - number: Course number (e.g '480B')
          - year: Year to add course to
          - term_type: term_type to add course to
        """
        response = SequenceHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        subject = request.GET.get('subject')
        number = request.GET.get('number')
        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))
        ignore_requirements = True if request.GET.get('ignore_requirements') == 'true' else False
        assert subject is not None
        assert number is not None
        assert year is not None
        assert term_type is not None
        assert ignore_requirements is not None

        # Fetch course to add.
        course = Course.objects.filter(course_code={'subject': subject}).filter(course_code={'number': number})[0]

        # Fetch sequence
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence = profile.active_sequence
        else:
            sequence = request.session.get('active_sequence')

        # Find term to which to add course to.
        try:
            term = sequence.get(year=year, term_type=term_type)
        except Term.DoesNotExist:
            response['message'] = 'The selected term does not exist.'
            return response

        # Ensure that the course is not already present
        if len(term.courses.filter(course_code={'subject': subject}).filter(course_code={'number': number})) > 0:
            response['message'] = 'The same course already exists for the specified term.'
            return response

        # Evaluate if requirements are fulfilled for that course
        if not ignore_requirements:
            evaluation_status, evaluation_container = course.evaluate_requirement(sequence)
            if not evaluation_status:
                response['message'] = 'The requirements for the course have not been fulfilled.'
                response['data'] = evaluation_container
                return response

        # Add course to term
        term.courses.add(course)
        response['success'] = True

        # Clean-up
        SequenceHandler.__clean_up(request, profile)
        return response

    @staticmethod
    def remove_course_from_active_sequence(request):
        """
        Removes a course from the user's sequence. The following parameters
        must be specified:
          - subject: Course subject (e.g 'CSC')
          - number: Course number (e.g '480B')
          - year: Year to remove course from
          - term_type: term_type to remove course from
        """
        response = SequenceHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        subject = request.GET.get('subject')
        number = request.GET.get('number')
        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))
        assert subject is not None
        assert number is not None
        assert year is not None
        assert term_type is not None

        # Fetch targeted sequence and term
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence = profile.active_sequence
        else:
            sequence = request.session.get('active_sequence')

        # Find term & course and remove it
        try:
            term = sequence.terms.get(year=year, term_type=term_type)
            course = term.courses.filter(course_code__exact={'subject': subject}).filter(
                course_code__exact={'number': number})[0]
            term.courses.remove(course)
            response['success'] = True

        except Term.DoesNotExist:
            response['message'] = 'The selected term does not exist.'
            return response

        except IndexError:
            # TODO: Find a better way to catch this error
            response['message'] = 'The selected course does not exist in the selected term.'
            return response

        # Clean-up
        SequenceHandler.__clean_up(request, profile)
        return response

    @staticmethod
    def add_program(request):
        """
        Adds a program to the list of selected programs that the user's sequence is intended
        to satisfy
        """
        response = SequenceHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        institution = request.GET.get('institution')
        name = request.GET.get('name')
        assert institution is not None
        assert name is not None

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence_programs = profile.programs
        else:
            sequence_programs = request.session.get('programs')

        # Find program to add
        program = Program.objects.filter(institution=institution).filter(name=name)[0]

        # Ensure that the same program currently does not exist
        if len(sequence_programs.filter(institution=institution).filter(name=name)) > 0:
            response['message'] = 'The selected term does not exist.'
            return response

        sequence_programs.add(program)
        response['success'] = True

        # Clean-up
        SequenceHandler.__clean_up(request, profile)
        return response

    @staticmethod
    def evaluate_program(request):
        # TODO complete evaluate_program method
        response = SequenceHandler.RESPONSE_BASE.copy()
        response['message'] = 'This method is currently not implemented.'

        return response

    @staticmethod
    def get_program(request):
        # TODO complete get_program method
        response = SequenceHandler.RESPONSE_BASE.copy()
        response['message'] = 'This method is currently not implemented.'

        return response

    @staticmethod
    def remove_program(request):
        # TODO complete remove_program method
        response = SequenceHandler.RESPONSE_BASE.copy()
        response['message'] = 'This method is currently not implemented.'

        return response

    @staticmethod
    def add_active_sequence(request):
        """
        Adds a new sequence for the specified user profile or session user.

        :param request:
        :return:
        """
        response = SequenceHandler.RESPONSE_BASE.copy()

        # TODO: Improve parameter fetching and handling of required parameters
        # Parameter parsing
        sequence_name = request.GET.get('name')
        assert sequence_name is not None

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            result = profile.active_sequence
            if result is not None:
                response['message'] = 'Could not add sequence, one already exists.'
                return response
            profile.active_sequence = Sequence(user=request.user, name=sequence_name)
            response['success'] = True

        #else:
        #    result = request.session.get('active_sequence')
        #    if result is not None:
        #        response['message'] = 'Could not add sequence, one already exists.'
        #        return response
        #    request.session['active_sequence'] = Sequence(name=sequence_name, terms=[])
        #    response['success'] = True

        # Clean-up
        SequenceHandler.__clean_up(request, profile)
        return response

    @staticmethod
    def get_active_sequence(request):
        """
        Returns the user's current sequence. Must be either logged in, or if not, returns
        session data
        """
        response = SequenceHandler.RESPONSE_BASE.copy()

        if request.user.is_authenticated:
            # TODO: Handle the error case of a profile not being available
            profile = Profile.objects.get(user=request.user)
            result = profile.active_sequence

            if result is not None:
                result = result.to_dict()
                response['data'] = result
                response['success'] = True
            else:
                response['message'] = 'The selected user profile does not have an associated sequence.'

        else:
            result = request.session.get('active_sequence')
            response['data'] = result
            response['success'] = True

        return response

    @staticmethod
    def add_term(request):
        """
        Adds a term for the user, depending on whether they're logged in or not.
        """
        response = SequenceHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))
        assert year is not None
        assert term_type is not None

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence = profile.active_sequence
        else:
            sequence = request.session.get('active_sequence')

        # TODO: Improve validation
        assert sequence is not None

        # Check that no Term with same year and term_type already exist
        if len(sequence.terms.filter(year=year).filter(term_type=term_type)) > 0:
            response['message'] = 'A term with the same year and term type already exists.'
            return response

        sequence.terms.add(Term(user=request.user, year=year, term_type=term_type))
        response['success'] = True

        # Clean-up
        SequenceHandler.__clean_up(request, profile)
        return response

    @staticmethod
    def get_term(request):
        response = SequenceHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence = profile.active_sequence
        else:
            sequence = request.session.get('active_sequence')

        # TODO: Improve validation
        assert sequence is not None

        if year is None and term_type is None:
            response['data'] = [term.to_dict() for term in sequence.terms.all()]
            response['success'] = True

        elif year is not None and term_type is None:
            response['data'] = [term.to_dict() for term in sequence.terms.filter(year=year)]
            response['success'] = True

        elif year is not None and term_type is not None:
            response['data'] = [term.to_dict() for term in sequence.terms.filter(year=year).filter(term_type=term_type)]
            response['success'] = True

        # Invalid request parameters
        else:
            response['message'] = 'Invalid request parameter values'

        return response

    @staticmethod
    def remove_term(request):
        """
        Removes a term for the user, depending on whether they're logged in or not.
        """
        response = SequenceHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))
        assert year is not None
        assert term_type is not None

        # Fetching sequence
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence = profile.active_sequence
        else:
            sequence = request.session.get('active_sequence')

        # TODO: Improve validation
        assert sequence is not None

        try:
            term = sequence.terms.get(year=year, term_type=term_type)
            sequence.terms.remove(term)
            response['success'] = True
        except Term.DoesNotExist:
            response['message'] = 'No terms with the selected year and term type exist.'
            return response

        # Clean-up
        SequenceHandler.__clean_up(request, profile)
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
