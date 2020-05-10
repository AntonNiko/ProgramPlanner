from plan.models import Course, Profile, Program, Term

class PlanHandler:
    """
    This handles requests and manages user-specific information regarding their program plan.

    To handle requests, the user must either have an existing session, or be logged in.
    """

    @staticmethod
    def add_course_to_sequence(request):
        """
        Adds a course to the user's sequence. To correctly add a course, the following parameters
        must be specified:
          - subject: Course subject (e.g 'CSC')
          - number: Course number (e.g '480B')
          - year: Year to add course to
          - term_type: term_type to add course to
        """ 

        subject = request.GET.get('subject')
        number = request.GET.get('number')
        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))

        # Fetch course to add.
        course = Course.objects.filter(course_code={'subject': subject}).filter(course_code={'number': number})[0]

        # Fetch targeted sequence and term
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence = profile.sequence
        else:
            sequence = request.session.get('sequence')

        for term in sequence.terms:
          if term.year == year and term.term_type == term_type:
            break
        else:
          # The term has not been found.
          return

        # Evaluate if requirements are fulfilled for that course
        # TODO: return evaluation_container as statistic
        evaluation_status, evaluation_container = course.evaluate_requirement(sequence) 
        if evaluation_status == False:
            return evaluation_container

        # Add course to term
        term.courses.append(course)

        # Clean-up
        PlanHandler.__clean_up(request, profile)

        return evaluation_container


    @staticmethod
    def remove_course_from_sequence(request):
        """
        Removes a course from the user's sequence. The following parameters
        must be specified:
          - subject: Course subject (e.g 'CSC')
          - number: Course number (e.g '480B')
          - year: Year to remove course from
          - term_type: term_type to remove course from
        """ 

        subject = request.GET.get('subject')
        number = request.GET.get('number')
        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))           

        # Fetch targeted sequence and term
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence = profile.sequence
        else:
            sequence = request.session.get('sequence')

        for term in sequence.terms:
            if term.year == year and term.term_type == term_type:
                break
        else:
            # The term has not been found.
            return

        for course in term.courses:
            if course.course_code.subject == subject and course.course_code.number == number:
                term.courses.remove(course)
                break
        else:
            # The course has not been found.
            return
          
        # Clean-up
        PlanHandler.__clean_up(request, profile)


    @staticmethod
    def add_program(request):
        """
        Adds a program to the list of selected programs that the user's sequence is intended
        to satisfy
        """
        response = {'success': False}

        institution = request.GET.get('institution')
        name = request.GET.get('name')

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence_programs = profile.programs
        else:
            sequence_programs = request.session.get('programs')

        program = Program.objects.filter(institution=institution).filter(name=name)[0]
        sequence_programs.append(program)
        response['success'] = True

        PlanHandler.__clean_up(request, profile)

        return response
        
    @staticmethod
    def get_sequence(request):
        """
        Returns the user's current sequence. Must be either logged in, or if not, returns
        session data
        """

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            result = profile.sequence
            if result != None:
                result = result.to_dict()
        else:
            result = request.session.get('sequence')

        return result


    @staticmethod
    def add_term(request):
        """
        Adds a term for the user, depending on whether they're logged in or not.
        """

        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence = profile.sequence
        else: 
            sequence = request.session.get('sequence')

        # TODO: Improve validation
        assert sequence != None

        # Check that no Term with same year and term_type already exist
        for term in sequence.terms:
          if term.year == year and term.term_type == term_type:
            return

        sequence.terms.append(Term(year=year, term_type=term_type, courses=[]))

        # Clean-up
        PlanHandler.__clean_up(request, profile)


    @staticmethod
    def remove_term(request):
        """
        Removes a term for the user, depending on whether they're logged in or not.
        """

        year = int(request.GET.get('year'))
        term_type = int(request.GET.get('term_type'))

        # Fetching sequence
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            sequence = profile.sequence
        else:
            sequence = request.session.get('sequence')

        # TODO: Improve validation
        assert sequence != None

        for term in sequence.terms:
            if term.year == year and term.term_type == term_type:
                sequence.terms.remove(term)
                break 

        # Clean-up
        PlanHandler.__clean_up(request, profile) 


    @staticmethod
    def __clean_up(request, profile):
        """
        Ensures that either the profile is saved or session modified flag is set.
        """     

        if request.user.is_authenticated:
            profile.save()
        else:
            request.session.modified = True  
              