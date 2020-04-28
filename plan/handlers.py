from django.contrib.auth import authenticate, login, logout
from plan.models import CourseCode

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
          - 'subject': If set, the result shall only contain courses under the subject
          - 'subjects_only': If set, ignores all other parameters, and returns a list of all subjects
          - 'number': If set, the result shall only contain courses that match the number
          - 'numbers_only': If set, assumes that 'subject' is set, ignores all other parameters
          ....

        Args:
          - request: An `HttpRequest` object.
        Returns:
          - response: A JSON-serializable object with result.
        """

        subject = request.GET.get('subject', None)
        subjects_only = request.GET.get('subjects_only', None)
        number = request.GET.get('number', None)
        numders_only = request.GET.get('numbers_only', None)
        number_min = request.GET.get('number_min', None)
        number_max = request.GET.get('number_max', None)

        #return Course.objects.all()


    @staticmethod
    def get_program_data(request):
        """
        Returns a list of programs as specified by the request parameters provided.

        Args:
          - request: An `HttpRequest` object.
        Returns:
          - response: A JSON-serializable object with result.
        """
        