from django.contrib.auth import authenticate, login, logout
from plan.models import Profile, Term


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

        if subject == None and number == None:
          result = [course.to_dict() for course in Course.objects.all()]
        elif subject != None and number == None:
          result = [course.to_dict() for course in Course.objects.filter(course_code__exact={'subject': subject})]
        elif subject != None and number != None:
          print("yes")
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
    def add_term(request):
        """
        Adds a term for the user, depending on whether they're logged in or not.
        """

        year = int(request.GET.get('year'))
        term_type = request.GET.get('term_type')

        if request.user.is_authenticated():
          sequence = Profile.objects.get(user=request.user).sequence
          sequence.append(Term(year=year, term_type=term_type))
          sequence.save()


    @staticmethod
    def get_sequence(request):
        """
        Returns the user's current sequence. Must be either logged in, or if not, returns
        session data
        """

        if request.user.is_authenticated():
          result = Profile.objects.get(user=request.user).sequence
        else:
          result = request.session.get('sequence', {})

        return result




