from django.contrib.auth import authenticate, login, logout
from plan.models import Course, Profile, Sequence, Term


class AccountHandler():
    """
    Handles requests relating to user accounts, and performs actions to fulfill
    the specified requests.
    """
    
    @staticmethod
    def login(request):
        """
        Attempts to login the user, given the request provided.

        Args:
         - request: An `HttpRequest` object.
        Returns:
         - `True` if the user is successfully logged in, `False` otherwise.
        Raises:
         - `AssertionError`: If the username or password is not present in the request object.
        """

        username = request.POST.get('username', None)
        password = request.POST('password', None)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False

    @staticmethod
    def logout(request):
        """
        Logs the user out.
        """

        logout(request)


class DataHandler():

    @staticmethod
    def get_course_data(request):
        """
        Returns a list of courses corresponding to request parameters 
        provided.

        The following parameters specified by the `request` are supported:
          - 'subject': If set, the result shall only contain courses for that subject
          - 'number': If set, the result shall only contain courses that match the number
        
        If 'subject' is undefined, all of the institution's courses will be returned.
        If 'subject' is defined and 'number' undefined, then all courses for that subject will be returned.

        Args:
          - request: An `HttpRequest` object.
        Returns:
          - response: A JSON-serializable object with result.
        """

        subject = request.GET.get('subject', None)
        number = request.GET.get('number', None)

        print(request.session.items())

        if subject == None and number == None:
            result = [course.to_dict() for course in Course.objects.all()]
        elif subject != None and number == None:
            result = [course.to_dict() for course in Course.objects.filter(course_code__exact={'subject': subject})]
        elif subject != None and number != None:
            result = [course.to_dict() for course in Course.objects.filter(course_code__exact={'subject': subject}).filter(course_code__exact={'number': number})]
        else:
            # TODO: Better error handling
            result = []
        return result


    @staticmethod
    def get_program_data(request):
        """
        Returns a list of programs as specified by the request parameters provided.

        Args:
          - request: An `HttpRequest` object.
        Returns:
          - response: A JSON-serializable object with result.
        """


class PlanHandler():
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
        #expression_result = course.evaluate_requirement(sequence) 

        # Add course to term
        term.courses.append(course)

        # Clean-up
        PlanHandler.__clean_up(request, profile)


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
              